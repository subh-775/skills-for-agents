# Fused Loss Function Kernels for LLMs - Research Summary

## Key Paper: Cut Cross-Entropy (CCE)
- **Paper**: "Cut Your Losses in Large-Vocabulary Language Models" (arXiv: 2411.09009)
- **Authors**: Erik Wijmans, Brody Huval, Alexander Hertzberg, Vladlen Koltun, Philipp Krähenbühl (Apple)
- **Key Idea**: Computes cross-entropy loss WITHOUT materializing full logits tensor (BT x V) into global memory. Only computes logit for correct token and evaluates log-sum-exp on the fly.
- **Impact**: Gemma 2 (2B): loss computation memory reduced from 24 GB to 1 MB
- **Technique**: Custom kernel performing matmul + log-sum-exp reduction over vocabulary in flash/SRAM memory. Leverages softmax sparsity to skip negligible gradient contributions.

---

## GitHub Repos with Production Triton/CUDA Loss Kernels

### 1. Liger-Kernel (LinkedIn) — PRIMARY SOURCE
**Repo**: https://github.com/linkedin/Liger-Kernel
**Architecture**: `src/liger_kernel/ops/` (Triton kernels) + `src/liger_kernel/transformers/` (nn.Module wrappers) + `src/liger_kernel/chunked_loss/` (preference/distillation losses)

#### A. Fused Cross-Entropy Kernel (`ops/cross_entropy.py`)
**Key file**: `src/liger_kernel/ops/cross_entropy.py` — `liger_cross_entropy_kernel`

**Core Algorithm (Online Softmax, 2-pass)**:
```
# Pass 1: Find max + sum (online softmax, Algorithm 3 from arxiv:1805.02867)
m = -inf  # max value
d = 0.0   # sum
for each BLOCK of logits X:
    block_max = tl.max(X_block)
    m_new = tl.maximum(m, block_max)
    d = d * tl.exp(m - m_new) + tl.sum(tl.exp(X_block - m_new))
    m = m_new
lse = m + tl.log(d)  # log-sum-exp

# Pass 2: Compute gradients in-place (stores into X_ptr to save memory)
softmax_x = tl.exp(X_block - m) / d
dx = softmax_x - eps  # label smoothing term
dx[y] -= (1 - label_smoothing)  # special case for target
dx /= n_non_ignore  # mean reduction

# Loss computation
loss = lse - X_y  # log-sum-exp minus target logit
```

**Features supported**:
- Label smoothing (fused, `label_smoothing` param)
- Z-loss (PaLM-style, `lse_square_scale` param)
- Logit softcapping (Gemma 2 style, `softcap` param)
- Class weights (`ce_weight`)
- Token accuracy & predicted tokens (computed without materializing full logits)
- ignore_index handling
- mean/sum/none reduction

**Numerical Stability Techniques**:
- Online softmax (single-pass max tracking with running correction)
- All softmax computation in float32 regardless of input dtype
- Loss = lse - X_y guarantees no overflow since sum(e^(X-max(X))) >= 1
- Gradient stored in-place in X_ptr (trick: overwrites logits with gradients)

**Gradient computation (backward stores in forward!)**:
```python
# Forward already computed gradients in-place in X_ptr
# Backward just scales by grad_output
element_mul_kernel[(n_rows,)](grad_input, stride, grad_output, V, ...)
```

#### B. Fused Linear + Cross-Entropy Kernel (`ops/fused_linear_cross_entropy.py`)
**Key class**: `LigerFusedLinearCrossEntropyFunction`

**Core Technique — Chunked Forward with In-Place Gradient**:
```python
# Chunk tokens to avoid materializing BT x V logits
inc_factor = cdiv(V, H)
chunk_size = next_power_of_2(cdiv(BT, inc_factor))
num_chunks = cdiv(BT, chunk_size)

for chunk_id in range(num_chunks):
    logits_chunk = _input_chunk @ weight.t()  # chunk_size x V
    # CE kernel computes loss AND gradient in-place (writes grad into logits_chunk)
    liger_cross_entropy_kernel[...](logits_chunk, target_chunk, ...)
    grad_logits_chunk = logits_chunk  # now contains gradients!
    grad_input[start:end] = grad_logits_chunk @ weight
    grad_weight += grad_logits_chunk.t() @ _input_chunk
```

**Memory savings**: Avoids BT x V logit matrix. For BT=16384, V=32000, H=4096: saves ~2GB.

#### C. Chunked Cross-Entropy for Large Vocabularies (Unsloth pattern)
**File**: `unsloth/kernels/cross_entropy_loss.py`

**Key idea — LogSumExp decomposition across chunks**:
```python
# For vocab > 65536 (e.g., Gemma 256K):
# Split vocab into N_CHUNKS of BLOCK_SIZE each
# Each chunk computes partial logsumexp
# Final: logsumexp = logsumexp(partial_logsumexp)
# Loss = logsumexp - x_target

_chunked_cross_entropy_forward[grid](logits, loss, logsumexp, labels, ...)
# grid = (n_rows, n_chunks)  — 2D launch
# chunk_idx=0 also loads target logit and stores -x
# All chunks store partial logsumexp
# Python-side: logsumexp = torch.logsumexp(logsumexp, dim=1)
# losses += logsumexp  # adds LSE term
```

**Math**:
```
logsumexp_total = log[sum(exp(a)) + ... + sum(exp(z))]
                = log[exp(logsumexp(a)) + ... + exp(logsumexp(z))]
                = logsumexp([logsumexp(a), ..., logsumexp(z)])
```

#### D. Fused Linear + JSD Kernel (`ops/fused_linear_jsd.py`)
- Same chunked linear+loss pattern as fused_linear_cross_entropy
- Uses `_jsd_kernel` for generalized Jensen-Shannon Divergence
- Supports forward/reverse KL as special cases (beta=0, beta=1)
- FP32 computation for numerical stability

#### E. KL Divergence Kernel (`ops/kl_div.py`)
```python
@triton.jit
def _kldiv_kernel_forward(y_ptr, gt_ptr, loss_ptr, n_cols, eps, ...):
    # KL(y_true || y) = y_true * (log(y_true) - log(y))
    # With log_target=True: loss = exp(y_true) * (y_true - y)
    loss = y_true * (tl.log(tl.maximum(y_true, eps)) - y)
```

#### F. Total Variation Distance Kernel (`ops/tvd.py`)
```python
@triton.jit
def _tv_distance_kernel(p_ptr, q_ptr, loss_ptr, grads_ptr, ...):
    tv_loss = 0.5 * tl.abs(p - q)
    grad_res = tl.where(p > q, 0.5 * scale, -0.5 * scale)
```

#### G. Sparsemax Kernel (`ops/sparsemax.py`)
```python
@triton.jit
def _sparsemax_forward_kernel(x_ptr, sorted_x_ptr, o_ptr, n_cols, ...):
    # Uses sorted input + cumsum for O(n) projection onto simplex
    cssv = tl.cumsum(z_valid, 0)
    t_vec = (cssv - 1.0) / r
    support = (z_sorted_block > t_vec) & mask
    tau = (s - 1.0) / k
    y = tl.maximum(x_block - tau, 0.0)
```

#### H. Softmax Kernel (`ops/softmax.py`)
```python
# Single-block (small vocab):
m = tl.max(x)
e = tl.exp(x - m)
d = tl.sum(e)
y = e / d

# Multi-block (large vocab, online softmax):
m = -inf; d = 0.0
for each block:
    blk_max = tl.max(xblk)
    new_m = tl.max(m, blk_max)
    d = d * tl.exp(m - new_m) + tl.sum(tl.exp(xblk - new_m))
    m = new_m
```

#### I. GRPO Loss Kernel (`ops/grpo_loss.py`)
**1004-line Triton kernel** implementing:
- `_selective_log_softmax_kernel`: Computes log(softmax(logits)[target]) without full softmax
- `_grpo_loss_fwd_kernel`: Full GRPO/DAPO/BNPO/CISPO/SAPO/VESPO forward
- Online softmax pattern for log-sum-exp computation
- PPO-style clipping with advantages
- KL penalty computation

#### J. Chunked Preference Losses (`chunked_loss/`)
- `fused_linear_preference.py`: Base class for DPO/SimPO/CPO/ORPO
  - Uses `torch.func.grad_and_value` for fused fwd+bwd per chunk
  - Chunks both chosen and rejected inputs
  - `torch.compile` compatible
- `fused_linear_distillation.py`: Base class for JSD distillation
  - Chunks student+teacher inputs together
  - Hard loss (CE) + soft loss (KL/JSD) fusion
- `dpo_loss.py`: Sigmoid, Hinge, IPO, EXO-pair, NCA, Robust, DiscoPOP variants
- `grpo_loss.py`: GRPO with VESPO gamma weighting, SAPO, CISPO

### 2. Unsloth
**Repo**: https://github.com/unslothai/unsloth
**Key file**: `unsloth/kernels/cross_entropy_loss.py`

**Unique contributions**:
- Chunked cross-entropy for vocabs > 65536 (Gemma 256K)
- Logit softcapping (Gemma 2: `t * tanh(x/t)`)
- Logit scaling (Cohere: `t * x`)
- Separate forward/backward kernels (vs Liger's combined approach)
- `calculate_settings()` for automatic BLOCK_SIZE/warp tuning
- `is_cdna()` detection for AMD GPU optimizations
- `patch_loss_functions()` for monkey-patching HF Transformers

### 3. Flash-Attention
**Repo**: https://github.com/Dao-AILab/flash-attention
- Primarily attention kernels, not loss functions
- The online softmax algorithm from flash-attention paper (arXiv:2205.14135) is the foundation used in all the loss kernels above
- Key insight: online max tracking + running sum correction

### 4. xformers
**Repo**: https://github.com/facebookresearch/xformers
- Mostly attention/memory-efficient ops
- Not a primary source for loss function kernels

---

## Key Patterns & Design Principles

### Pattern 1: Online Softmax (2-pass, used in CE kernel)
```
Pass 1 (forward): Track running max m and sum d
  m_new = max(m, block_max)
  d = d * exp(m - m_new) + sum(exp(block - m_new))

Pass 2 (gradient): Use stable softmax = exp(x - m) / d
```
Reference: arXiv:1805.02867 (Online normalizer calculation for softmax)

### Pattern 2: In-Place Gradient Storage
Forward pass writes gradients directly into the logits buffer:
```python
# In forward: kernel overwrites X_ptr with gradient values
# In backward: just multiply by grad_output scalar
```
Saves memory: no need to store logits for backward.

### Pattern 3: Chunked Linear + Loss Fusion
Avoid materializing BT x V logits:
```python
for chunk in chunks:
    logits = input_chunk @ weight.T  # small chunk
    loss_chunk, grad_logits = fused_ce_kernel(logits, target_chunk)
    grad_input += grad_logits @ weight
    grad_weight += grad_logits.T @ input_chunk
```

### Pattern 4: LogSumExp Decomposition for Large Vocab
```
logsumexp_total = logsumexp([logsumexp(chunk_1), ..., logsumexp(chunk_N)])
```
Enables vocab sizes > 65536 with BLOCK_SIZE = 65536.

### Pattern 5: Numerical Stability
- Always compute softmax in float32
- Use max-subtraction: exp(x - max(x)) prevents overflow
- Loss = lse - x_y is guaranteed stable (sum >= 1)
- Softcapping: cap * tanh(x/cap) prevents extreme logits

### Pattern 6: Triton Kernel Design
- One program per row (token): `program_id(0)` = token index
- BLOCK_SIZE = min(MAX_FUSED_SIZE, next_power_of_2(vocab_size))
- MAX_FUSED_SIZE = 32768 (conservative) or 65536 (aggressive)
- num_warps: 32 for NVIDIA, 16 for AMD (CDNA)
- `.cast(tl.float32)` for all intermediate computations

---

## Loss Functions Available in Liger-Kernel

| Loss | Kernel File | Type |
|------|------------|------|
| Cross-Entropy | `ops/cross_entropy.py` | Triton |
| Fused Linear+CE | `ops/fused_linear_cross_entropy.py` | Triton |
| KL Divergence | `ops/kl_div.py` | Triton |
| JSD | `ops/jsd.py` | Triton |
| Fused Linear+JSD | `ops/fused_linear_jsd.py` | Triton |
| TVD | `ops/tvd.py` | Triton |
| Sparsemax | `ops/sparsemax.py` | Triton |
| Softmax | `ops/softmax.py` | Triton |
| GRPO Loss | `ops/grpo_loss.py` | Triton |
| DPO/SimPO/CPO/ORPO | `chunked_loss/*.py` | torch.compile |
| JSD Distillation | `chunked_loss/jsd_loss.py` | torch.compile |
| KTO | `chunked_loss/kto_loss.py` | torch.compile |

---

## Not Found / Gaps

- **Fused Focal Loss**: No production Triton kernel found. Focal loss (Lin et al., 2017) = -α(1-p)^γ * log(p). Would need custom kernel modulating CE by (1-softmax)^gamma.
- **Fused Label Smoothing**: Already integrated into Liger's CE kernel (not a separate kernel).
- **Dedicated "numerically stable loss" kernel**: Stability is baked into all kernels above via online softmax pattern.
- **Cut Cross-Entropy (CCE) implementation**: The Apple paper's kernel is not publicly available in a repo (as of research date). The technique is conceptually similar to Liger's fused_linear_cross_entropy.

---

## References

1. Cut Cross-Entropy: arXiv:2411.09009
2. Online Softmax: arXiv:1805.02867
3. Flash-Attention: arXiv:2205.14135
4. Focal Loss: arXiv:1708.02002
5. Label Smoothing: arXiv:1512.00567
6. PaLM Z-loss: JMLR v24/22-1144
7. DPO: arXiv:2305.18290
8. Liger-Kernel: https://github.com/linkedin/Liger-Kernel
9. Unsloth: https://github.com/unslothai/unsloth
10. mgmalek/efficient_cross_entropy: Reference for fused linear+CE pattern
