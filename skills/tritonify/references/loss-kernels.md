# Fused Loss Function Kernels Reference

## Key Paper: Cut Cross-Entropy (Apple)
- arXiv:2411.09009 — Computes CE without materializing BT×V logits
- Gemma 2B: 24GB → 1MB memory for loss computation
- Technique: matmul + log-sum-exp reduction in SRAM

## Production Kernels (Liger-Kernel)

### 1. Fused Cross-Entropy (`ops/cross_entropy.py`)

**Algorithm: Online Softmax (2-pass)**
```
Pass 1: Find max + sum
  m = -inf; d = 0.0
  for each BLOCK of logits:
      block_max = tl.max(X_block)
      m_new = max(m, block_max)
      d = d * exp(m - m_new) + sum(exp(X_block - m_new))
      m = m_new
  lse = m + log(d)

Pass 2: Compute gradients in-place (stores into logits buffer)
  softmax_x = exp(X_block - m) / d
  dx = softmax_x - eps  # label smoothing
  dx[target] -= (1 - label_smoothing)
  dx /= n_non_ignore

  loss = lse - X[target]
```

**Features**: Label smoothing, z-loss, softcapping, class weights, ignore_index

**Key trick**: Forward writes gradients directly into logits buffer — backward just scales by grad_output. Saves memory (no logits stored for backward).

### 2. Fused Linear+CE (`ops/fused_linear_cross_entropy.py`)

**Chunked approach — avoids BT×V logit materialization:**
```python
chunk_size = next_power_of_2(cdiv(BT, cdiv(V, H)))
for chunk_id in range(num_chunks):
    logits_chunk = input_chunk @ weight.T  # small chunk
    # CE kernel computes loss AND gradient in-place
    ce_kernel(logits_chunk, target_chunk)
    grad_logits_chunk = logits_chunk  # now contains gradients!
    grad_input[start:end] = grad_logits_chunk @ weight
    grad_weight += grad_logits_chunk.T @ input_chunk
```

**Saves**: ~2GB for BT=16384, V=32000, H=4096

### 3. Chunked CE for Large Vocab (Unsloth pattern)

**LogSumExp decomposition for vocab > 65536:**
```python
# Split vocab into chunks of BLOCK_SIZE
# Each chunk computes partial logsumexp
# Final: logsumexp = logsumexp([lse_1, lse_2, ..., lse_N])
# Loss = logsumexp - x_target
```

### 4. Other Loss Kernels (Liger-Kernel)

| Loss | File | Key Pattern |
|------|------|-------------|
| KL Divergence | `ops/kl_div.py` | `loss = y_true * (log(y_true) - log(y))` |
| JSD | `ops/jsd.py` | Generalized Jensen-Shannon, supports fwd/rev KL |
| TVD | `ops/tvd.py` | `loss = 0.5 * abs(p - q)` |
| Sparsemax | `ops/sparsemax.py` | Sorted input + cumsum for O(n) simplex projection |
| Softmax | `ops/softmax.py` | Single-block (small vocab) + multi-block online (large) |
| GRPO Loss | `ops/grpo_loss.py` | 1004-line kernel: selective log-softmax, PPO clipping, KL penalty |
| DPO/SimPO/CPO/ORPO | `chunked_loss/` | torch.compile with chunked processing |
| Fused Linear+JSD | `ops/fused_linear_jsd.py` | Same chunked pattern as Linear+CE |

## Design Patterns

### Pattern 1: Online Softmax
```
Track running max m and sum d:
  m_new = max(m, block_max)
  d = d * exp(m - m_new) + sum(exp(block - m_new))
```
Reference: arXiv:1805.02867

### Pattern 2: In-Place Gradient Storage
Forward overwrites logits with gradients. Backward just multiplies by grad_output.

### Pattern 3: Chunked Linear+Loss Fusion
Avoid materializing BT×V: chunk tokens, compute matmul+CE per chunk.

### Pattern 4: LogSumExp Decomposition
`logsumexp_total = logsumexp([lse_chunk_1, ..., lse_chunk_N])`
Enables vocab > 65536 with BLOCK_SIZE=65536.

### Pattern 5: Numerical Stability
- Always compute in float32
- Max-subtraction prevents overflow
- Loss = lse - x_y is stable (sum >= 1)
- Softcapping: `cap * tanh(x/cap)` prevents extreme logits

## Kernel Parameters
- One program per row (token): `program_id(0)` = token index
- BLOCK_SIZE = min(32768, next_power_of_2(vocab_size))
- num_warps: 32 NVIDIA, 16 AMD (CDNA)
- All intermediate computation in float32

## Missing Kernels
- **Focal Loss**: No production Triton kernel. Would need: `-α(1-p)^γ * log(p)` modulation.
- **CCE (Apple)**: Not publicly available. Conceptually similar to Liger's fused_linear_CE.

## References
- Cut Cross-Entropy: arXiv:2411.09009
- Online Softmax: arXiv:1805.02867
- Focal Loss: arXiv:1708.02002
- Liger-Kernel: github.com/linkedin/Liger-Kernel
- Unsloth: github.com/unslothai/unsloth
