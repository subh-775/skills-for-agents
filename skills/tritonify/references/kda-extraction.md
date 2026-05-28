# MIT Kernel Design Agents — Complete Extraction

Extracted from https://github.com/mit-han-lab/kernel-design-agents (commit HEAD).
Date: 2026-05-28

---

## 1. COMPLETE AGENT WORKFLOW (from docs/agent-flow.md + CLAUDE.md + prompts/basic-flow.md)

### Principle
Keep the reusable workflow separate from the task workspace. The KDA repo explains the flow. The task workspace owns code, tests, datasets, benchmark scripts, private rules, and generated artifacts.

### Minimal Loop (9 steps)
1. Define the task contract
2. Let the agent inspect the local workspace
3. Make the agent write `docs/draft.md`
4. Convert the draft into an executable plan
5. Implement the first candidate
6. Validate correctness
7. Measure the target metric when applicable
8. Record evidence and decide whether to keep, revise, or reject the candidate
9. Repeat until the promotion criteria are met or the remaining blockers are explicit

### Full Expected Agent Workflow (from CLAUDE.md)
1. Create or enter a separate implementation workspace
2. Define the task objective, constraints, validation command, and promotion criteria
3. Use `prompts/basic-flow.md` as the starter prompt
4. Read local task code and documentation before proposing implementation changes
5. Write the initial plan draft to `docs/draft.md` inside the task workspace
6. Convert the draft into an executable plan
7. Implement in small iterations, validating each meaningful candidate
8. Record candidate relationships, evaluation results, and profiling evidence when applicable
9. Keep the repository focused on the reusable flow

### Repository Rules
- Use English for all repo-facing files
- Keep task-specific prompts/datasets/validators out of the main repo
- Put generated outputs in `runs/`, `outputs/`, or `profile/` (gitignored)
- Prefer documenting reusable workflow mechanics over one task's private details

---

## 2. TASK CONTRACT TEMPLATE (from prompts/basic-flow.md)

```
## Task Contract

- Task name: `<fill in>`
- Objective: `<fill in the user-facing goal>`
- Correctness requirements: `<fill in required behavior, tolerances, or invariants>`
- Performance or quality target: `<fill in measurable target if any>`
- Allowed implementation approaches: `<fill in languages, libraries, APIs, or constraints>`
- Validation command: `<fill in the command that proves correctness>`
- Evaluation command: `<fill in the command that measures the target, if different>`
- Promotion criteria: `<fill in what must be true before a candidate is accepted>`
```

### Workflow Steps (in the prompt)
1. Read the repository structure, existing implementation, tests, and task documentation
2. Identify the baseline behavior and the validation path
3. Research only the references needed for this task
4. Write an implementation-plan draft to `docs/draft.md`
5. Turn the draft into an executable plan before editing code
6. Implement one candidate at a time
7. Run validation after each meaningful candidate
8. Record candidate results, parent relationships, and evidence in the workspace
9. Keep the final change scoped to the task contract

### Plan Draft Requirements (docs/draft.md must contain)
- The current baseline and how it is validated
- The main risks and unknowns
- Candidate implementation directions ranked by expected value and risk
- The first concrete implementation steps
- The exact validation and evaluation commands to run
- The evidence required to promote, revise, or reject a candidate

---

## 3. NCU-REPORT-SKILL DIAGNOSIS PLAYBOOK — ALL 14 PATTERNS

From reference/06-diagnosis-playbook.md:

### Pattern A — Small grid / SM idle
- **Signals:** `launch__waves_per_multiprocessor < 0.5`, grid_size < SM count
- **Why:** fewer CTAs than SMs, some SMs completely idle
- **First-line fix:** increase grid size — add split-K, split across heads, grid-stride loops
- **Deeper:** persistent kernel, fuse adjacent kernels
- **Exceptions:** LLM decode (batch=1), final reduction stages

### Pattern B — Tail effect (variable-length inputs)
- **Signals:** `max_seq_len / avg_seq_len > 3`, per-SM active cycles span 5-100x, PM timeline shows long gradual tail
- **Why:** variable-size inner loops, a few long-sequence CTAs keep running after others finish
- **First-line fix:** packed batching/sorting by length, split long sequences across more CTAs
- **Deeper:** chunkwise kernel, classify-and-dispatch (short vs long paths)

### Pattern C — Uncoalesced global loads
- **Signals:** sectors/request > 5 (ideal is 4), NCU rule about uncoalesced accesses
- **Why:** lanes in warp access non-contiguous addresses
- **First-line fix:** rework thread↔data mapping, AoS→SoA
- **Deeper:** shared memory transposer, vectorize with float2/float4

### Pattern D — Sparse writes (low store efficiency)
- **Signals:** `sass_average_data_bytes_per_sector_mem_global_op_st.ratio < 16` (ideal 32)
- **Why:** only subset of warp lanes write, L1 store buffer flushes half-empty sectors
- **First-line fix:** pack writes — shuffle/shared mem reduction then contiguous lanes write
- **Deeper:** write to shared memory first, then coalesced global store

### Pattern E — Latency-bound (long-scoreboard-dominated)
- **Signals:** `long_scoreboard` > 40% of samples, DRAM throughput < 10%
- **Why:** warps issue load then stall waiting; low occupancy or insufficient ILP
- **First-line fix:** unroll load loop, add more warps (raise occupancy), use cp.async/TMA/tcgen05.cp
- **Deeper:** software pipelining, move reused data to shared memory

### Pattern F — Compute-bound but not on tensor cores
- **Signals:** FMA pipe > 50%, tensor pipe = 0%, workload is matmul-ish
- **Why:** kernel uses scalar FMA instead of tensor cores (16x less throughput on B200)
- **First-line fix:** use WMMA/wgmma/tcgen05.mma, or CUTLASS 4.x / cuBLAS
- **Deeper:** restructure data layout for MMA tile shapes

### Pattern G — Atomics contention
- **Signals:** long_scoreboard on ATOM/RED instructions, large `lts__t_sectors_op_atom.sum`
- **Why:** many threads atomically updating few locations → serialization
- **First-line fix:** hierarchical reduction (warp shuffle → shared mem → single atomic)
- **Deeper:** shared-memory histogram, bucketing

### Pattern H — Shared-memory bank conflicts
- **Signals:** high wavefronts for shared-mem ops, short_scoreboard on shared-mem loads
- **Why:** 32 banks, same-bank accesses serialize
- **First-line fix:** padding (`tile[32][33]` instead of `[32][32]`)
- **Deeper:** swizzle (XOR-scramble indices), restructure data layout

### Pattern I — Synchronization overhead
- **Signals:** `barrier` stall > 20%, hotspot on BAR.SYNC
- **Why:** `__syncthreads()` waits for slowest warp
- **First-line fix:** replace block-level syncs with warp-level primitives, reduce sync count
- **Deeper:** warp-specialized execution with mbarrier

### Pattern J — Low achieved vs theoretical occupancy
- **Signals:** theoretical occupancy high but achieved << that
- **Why:** stalls, imbalance, or short kernel (warmup dominates)
- **First-line fix:** find the stall reason causing the gap (Patterns E, H, I, B)

### Pattern K — Register spill
- **Signals:** `local_ld/local_st > 0`, `registers_per_thread > 128`
- **Why:** compiler couldn't fit live variables in registers, spilled to DRAM-backed local memory
- **First-line fix:** `__launch_bounds__(maxThreadsPerBlock, minBlocksPerMultiprocessor)`
- **Deeper:** reduce live values, split kernel, move arrays to shared memory

### Pattern L — FP64 used unintentionally
- **Signals:** `sm__pipe_fp64_cycles_active > 0` in "should be FP32" kernel
- **Why:** C/C++ literals default to double (`1.0` not `1.0f`)
- **First-line fix:** add `f` suffix to all literals, use `__expf/__logf/__sinf`

### Pattern M — Pipeline bubbles (no compute/memory overlap)
- **Signals:** PM timeline sawtooth (compute ↔ DRAM alternating), long_scoreboard high + DRAM high
- **Why:** single-buffered: load tile → compute → load next
- **First-line fix:** double-buffer with two shared-memory tiles
- **Deeper:** multi-stage pipeline (3-4 stages on Blackwell), use cp.async/TMA

### Pattern N — Warp divergence
- **Signals:** `thread_inst_executed_per_inst_executed.ratio < 32`, low branch efficiency
- **Why:** lanes take different paths at branch, hardware serializes
- **First-line fix:** rearrange data so all lanes take same branch, convert to branchless mask
- **Exceptions:** tree reductions, boundary handling

### Ranking Template for Final Report
```
Priority 1: <pattern> — <concrete fix>
  Evidence: <metric value(s)>
  NCU Est. Speedup: X%
  Effort: <low / medium / high>
  Why now: <reason this is the highest-leverage fix>
```
Rule of thumb: at most 3-5 priorities. More dilutes signal.

---

## 4. SIX ANALYSIS DIMENSIONS (from reference/05-analysis-dimensions.md)

### Dimension 1 — SM occupancy & launch geometry
- Key metrics: grid_size, block_size, waves_per_multiprocessor, registers_per_thread, occupancy_limit_*
- Wave math: `wave_size = blocks_per_sm * num_sms`, `num_waves = ceil(total_blocks / wave_size)`
- Waves < 1 = grid too small; waves 1-2 = tail wave; waves > 4 = plenty

### Dimension 2 — Thread-block balance (tail effect)
- Use PM sampling time series + per-SM active cycle distribution
- Timeline shapes: flat high→clean drop (ideal), flat high→gradual tail (tail effect), sawtooth (pipeline bubbles)
- Always inspect input distribution for variable-length work

### Dimension 3 — Stall reason breakdown + per-line hotspots
- Key stall reasons: long_scoreboard (memory latency), short_scoreboard (shared mem/compute), wait (SFU/tensor), barrier (syncthreads), math_pipe_throttle (FMA saturated), mio_throttle/lg_throttle (LSU saturated)
- long_scoreboard > 40% = memory-latency-bound
- short_scoreboard > 30% = long dep chains or heavy shared-mem
- barrier > 20% = too much sync or divergence before barrier

### Dimension 4 — Tensor Core utilization
- Key metric: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed`
- 0% on matmul-ish = missed optimization; < 50% = underutilized; > 50% = good
- B200 uses tcgen05.mma + TMEM accumulators

### Dimension 5 — SM utilization timeline
- PM sampling time-series shapes: flat high (ideal), flat low (grid too small), sawtooth (no overlap), gradual tail (tail effect)

### Dimension 6 — Memory access pattern
- Sectors/request (ideal = 4 for 128B coalesced), L1/L2 hit rates, DRAM throughput
- Store efficiency (`bytes_per_sector_st.ratio`, ideal = 32)
- Register spill detection via `local_ld/local_st > 0`

---

## 5. KERNELWIKI DOMAIN KNOWLEDGE

### Three-Layer Architecture
- **Layer 1: Sources** — Raw data (PRs, contests, docs, blogs) with YAML frontmatter
- **Layer 2: Wiki** — Synthesized knowledge pages (hardware, techniques, patterns, kernels, languages, migration)
- **Layer 3: Queries** — Auto-generated cross-referenced indices

### Contents (knowledge cutoff: 2026-04-27)
- 2265 total markdown pages (2179 PR refs + 48 wiki synthesis + 20 blogs + 11 docs + 7 contests)
- 6 candidate ledgers with 4,222 merged PRs classified
- 89 verbatim/extracted/derived asset bundles
- 80+ controlled vocabulary tags

### Wiki Page Categories
- **wiki/hardware/** — tcgen05-mma, TMEM, TMA, mbarrier, CLC, NVFP4, PDL/GDC, 2SM-cooperative
- **wiki/techniques/** — warp-specialization, persistent-kernels, pipeline-stages, double-buffering, swizzling, tile-scheduling, register-budgeting, software-exp, ping-pong-scheduling, epilogue-fusion, fine-grained-quantization, kernel-fusion, vectorized-loads, cache-policy, chunk-parallelism
- **wiki/patterns/** — register-pressure, tail-effect, moe-load-imbalance, pipeline-stalls, low-sm-utilization, memory-bound, compute-bound
- **wiki/kernels/** — flash-attention-4, deepgemm, flashmla, fused-moe, grouped-gemm, nsa, gated-delta-net, gated-dual-gemm, nvfp4-gemm, nvfp4-gemv, sparse-mla, fp8-block-scale-gemm
- **wiki/languages/** — triton-blackwell, cute-dsl, ptx-sm100, cuda-cpp
- **wiki/migration/** — wgmma-to-tcgen05, register-to-tmem

### Key Technique Details

#### Warp Specialization on Blackwell
- 16-warps (512 threads) per CTA
- Warp 0 = TMA Producer, Warp 1 = MMA Consumer, Warps 2-15 = Epilogue
- Single-thread tcgen05.mma dispatch (vs Hopper's 4-warp warpgroup)
- Accumulators in TMEM (not registers) — reduces register pressure
- mbarrier pairs for producer-consumer sync (data_ready + buffer_free)

#### Persistent Kernels with CLC
- CLC (Cluster Launch Control) hardware replaces software tile scheduling
- Each CTA queries CLC for next tile, uses `try_cancel` to exit
- Eliminates tail effect dynamically — fast CTAs absorb extra work
- 57% improvement (940 → 1476 TFLOPS) from persistence alone
- CUTLASS provides `PersistentTileSchedulerSm100`

#### Software Pipelining (3-5 stages)
- 3-stage pipeline: 35% improvement (695 → 940 TFLOPS)
- mbarrier-based producer-consumer sync (not __syncthreads)
- TMA hardware signals mbarrier autonomously
- 3 stages standard on Blackwell, 4-5 for high memory latency
- SMEM budget: 228 KB per SM on B200

#### Double Buffering
- TMEM double-buffering: ping-pong between two 128x256 accumulator regions (256 of 512 columns each)
- SMEM multi-stage buffering: 3-stage circular buffer for TMA loads
- Combined: epilogue of tile 0 overlaps MMA of tile 1 (different TMEM buffers)

#### Swizzling
- 128-byte swizzling mandatory for Blackwell tcgen05 inputs
- XOR bits [4:6] of byte offset with row index
- Without swizzle: 255 TFLOPS (17%); with swizzle: 695 TFLOPS (46%) — 2.7x improvement
- TMA descriptor encodes swizzle mode (SWIZZLE_128B for BF16/FP16 MMA operands)

---

## 6. CANDIDATE TRACKING SYSTEM

### Evidence Records (from docs/agent-flow.md)
- `docs/draft.md` — first plan draft
- `docs/plan.md` — executable plan
- `benchmark.csv` — tabular log for measurable results
- `candidates.jsonl` — candidate names, parent links, and status
- `profile/` — profiler output or report summaries
- `runs/` or `outputs/` — generated artifacts

### Promotion Rule
Promote a candidate only when it satisfies the task contract AND has evidence that it improves or preserves the target metric. If rejected, record the reason (never silently discard).

### KernelWiki Candidate Ledgers
- 6 candidate ledgers in `candidates/` (vllm, sglang, pytorch, flashinfer, deepgemm, cutlass)
- 4,222 merged PRs classified as include/defer/exclude
- Each PR has inclusion_reason and status: merged

---

## 7. WORKSPACE STRUCTURE

### Main KDA Repo
```
kernel-design-agents/
├── CLAUDE.md                    ← agent instructions
├── prompts/basic-flow.md        ← starter prompt with task contract template
├── docs/agent-flow.md           ← workflow documentation
├── skills/
│   ├── ncu-report-skill/        ← CUDA profiling skill (submodule)
│   └── KernelWiki/              ← domain knowledge wiki (submodule)
├── runs/                        ← generated artifacts (gitignored)
├── outputs/                     ← generated artifacts (gitignored)
└── profile/                     ← profiling artifacts (gitignored)
```

### Profile Run Directory Structure
```
profile/<run_name>/
├── REPORT.md                    ← final report
├── harness/
│   ├── <kernel>_harness.cu      ← exact source compiled
│   ├── <kernel>_harness         ← compiled binary (with -lineinfo)
│   └── build_command.sh
├── reports/
│   ├── full_<tag>.ncu-rep       ← ncu --set full output
│   └── source_<tag>.ncu-rep     ← ncu --set source output
└── analysis/
    ├── metrics_all_<tag>.json   ← 2000+ metrics archive
    ├── metrics_key_<tag>.txt    ← curated key metrics
    ├── compare_<a>_vs_<b>.txt   ← side-by-side comparison
    ├── stall_hotspots_<tag>.txt ← per-line stall aggregation
    ├── pm_timeline_plots.txt    ← ASCII time-series
    └── details_<tag>.txt        ← ncu --page details dump
```

### KernelWiki Structure
```
KernelWiki/
├── SKILL.md                     ← skill entry point
├── CLAUDE.md                    ← schema documentation
├── wiki/                        ← synthesized knowledge
│   ├── hardware/                ← tcgen05, TMEM, TMA, mbarrier, CLC, etc.
│   ├── techniques/              ← 15 optimization techniques
│   ├── patterns/                ← 7 problem→solution patterns
│   ├── kernels/                 ← 12 kernel case studies
│   ├── languages/               ← 4 DSL/language guides
│   └── migration/               ← 2 Hopper→Blackwell patterns
├── sources/prs/                 ← 2179 PR references
├── queries/                     ← auto-generated cross-references
├── candidates/                  ← 6 PR classification ledgers
├── artifacts/                   ← verbatim code bundles with PROVENANCE.yaml
├── data/                        ← tags, aliases, schemas, version-claims
└── scripts/                     ← query.py, get_page.py, grep_wiki.py, validate.py, etc.
```

---

## 8. B200/BLACKWELL-SPECIFIC OPTIMIZATIONS

### Architecture Key Parameters
- 148 SMs (2 die × 74 SM), CC 10.0, sm_100a
- 64 warps per SM, 64K registers per SM
- 228 KB shared memory per SM (configurable)
- **256 KB TMEM per SM** (512 columns × 128 lane × 32-bit) — NEW
- 126 MB L2 cache (vs 50 MB on H100)
- 192 GB HBM3e at 8 TB/s (vs 80 GB HBM3 at 3.35 TB/s on H100)
- NVLink 5 at 1.8 TB/s

### Tensor Core Throughput
| Format | Dense | Sparse | vs FP16 |
|--------|-------|--------|---------|
| NVFP4 | 9 PFLOPS | 18 PFLOPS | 4x |
| MXFP4 | 9 PFLOPS | 18 PFLOPS | 4x |
| FP8 | 4.5 PFLOPS | 9 PFLOPS | 2x |
| FP16/BF16 | 2.25 PFLOPS | 4.5 PFLOPS | 1x |
| TF32 | 1.13 PFLOPS | 2.25 PFLOPS | 0.5x |

### 5th Gen Tensor Core (tcgen05) — Key Changes
- **Single-thread MMA dispatch** (vs Hopper's 4-warp warpgroup) — 3-11x lower latency
- **Accumulators in TMEM** (not registers) — frees register file
- **TMEM read bandwidth ~16 TB/s/SM**, write ~8 TB/s/SM
- PTX: tcgen05.alloc, tcgen05.mma, tcgen05.ld, tcgen05.dealloc
- A matrix: Shared Memory or TMEM; B matrix: Shared Memory; D (accumulator): always TMEM

### CTA Pair (2CTA) — Dual SM Cooperative
- Two SMs in same TPC cooperate on MMA via `cta_group::2`
- Shared input operands → half shared memory bandwidth per CTA
- Effective MMA M dimension doubles (M=128 → M=256)
- Required for 100% Tensor Core utilization (single SM = ~50% peak)

### CLC (Cluster Launch Control)
- Hardware tile scheduling replaces software loops
- Persistent kernels: launch exactly as many CTAs as SMs
- `try_cancel` pattern for dynamic termination
- Eliminates tail effect, reduces launch overhead, improves L2 locality

### Low Precision Data Types
- NVFP4: E2M1 + block-16 E4M3 scale + per-tensor FP32 scale (best precision)
- MXFP4: E2M1 + block-32 E8M0 scale (OCP standard)
- FP4 and FP8 share physical circuits; FP4 gets 2x throughput from double elements
- LLM inference: NVFP4 (W4A4) or FP8 (W8A8)
- Training: BF16 + FP8 mixed

### Hardware Decompression Engine
- LZ4, Snappy, Zstandard, GZIP, Bitcomp, ANS at ~539 GB/s
- Runs in parallel with SM, no compute resource usage
- Useful for compressed weight storage in HBM

### Key Performance Principle Adjustments vs Hopper
1. **Register pressure more relaxed** — TMEM holds accumulators, freeing registers
2. **Shared memory bandwidth pressure lower** — 2CTA halves per-SM bandwidth need
3. **Pipeline design more critical** — 2x Tensor Core throughput but same SMEM → need 3-4 stage pipelines
4. **L2 cache 126 MB** — more working set fits in L2, use L2 persistence for hot data (KV cache)

### B200 Metric Name Differences (from reference/08-b200-metric-names.md)
- `smsp__inst_executed_op_global_ld.sum` → `smsp__sass_inst_executed_op_global_ld.sum`
- `smsp__inst_executed_op_local_ld.sum` → `smsp__sass_inst_executed_op_local_ld.sum`
- `smsp__inst_executed_op_shared_ld.sum` → `smsp__sass_inst_executed_op_shared_ld.sum`
- `l1tex__average_t_sectors_per_request*.ratio` → compute manually from sectors/requests
- `dram__bytes.sum` → compute from `dram__bytes_read.sum + dram__bytes_write.sum`
- Stall metrics: add `average_` prefix, use `.ratio` suffix instead of `.pct`
- `sm__inst_executed_pipe_fmaheavy.*` not present — use `sm__inst_executed_pipe_fma.*`

### Triton on Blackwell (Triton 3.6+)
- Native tcgen05 + TMEM lowering (since 3.6.0, released 2026-01-21)
- Verified: descriptor/TMA + `tl.range(warp_specialize=True)` + `tl.dot`
- Verified: `tl.dot_scaled` for block-scaled matmul (NVFP4/MXFP)
- Verified: Gluon front-end + `gl.warp_specialize` + `num_ctas` (initial 2-CTA)
- Caveat: not every `tl.dot` shape automatically emits tcgen05.mma on every Blackwell SKU
- Peak performance: CUTLASS/CuTe-DSL still leads for compute-bound matmul (~27% faster than Triton)

### Pre-3.6 Historical Context (now obsolete)
- No direct tcgen05 access (compiler generated wgmma)
- No TMEM (accumulators in registers)
- CPU launch overhead impacted small-batch decode

### NCU Profiling Golden Rule
**Profile → Diagnose → Plan, in that order. Never guess.**

Critical lessons:
1. Stock metric names don't all work on B200 — use sm_100 names
2. Always compile with `-lineinfo`
3. PM sampling is the only way to see tail effects
4. Load-imbalance on variable-length inputs is often #1 bottleneck
5. NCU's rule engine (`--page details`) already does half the work
6. Don't delegate understanding — cite specific metric values
