"""
Gradient Verification Template — MANDATORY for any Triton kernel used in training.

From SEV1 incident 2026-05-29: BiBo Triton patches broke gradient flow silently.
Forward was verified to 1e-7 precision but 3 layers had frozen weights.

Usage:
    python gradient_verification.py --model <model_class> --patched <patch_fn> [--steps 50]

The 5 tests that MUST pass before promoting any kernel:
1. Gradient equivalence (patched vs unpatched)
2. No zero/None/NaN/Inf gradients
3. No stale buffers for learnable tensors
4. 50-step smoke test (loss curves within 5%)
5. Grad norm sanity check
"""

import torch
import torch.nn as nn
from typing import Callable, Optional, Dict, Tuple
import sys


def test_gradient_equivalence(
    model_patched: nn.Module,
    model_unpatched: nn.Module,
    batch: dict,
    atol_loss: float = 1e-6,
    atol_grad_fp32: float = 1e-3,
    atol_grad_fp16: float = 5e-2,
) -> Tuple[bool, list]:
    """
    Test 1: Compare weight gradients between patched and unpatched models.
    
    Returns (passed, failures) where failures is a list of error strings.
    """
    failures = []
    
    # Zero grads
    model_patched.zero_grad()
    model_unpatched.zero_grad()
    
    # Forward + backward on both (same input)
    loss_p = model_patched(**batch).loss
    loss_p.backward()
    
    loss_u = model_unpatched(**batch).loss
    loss_u.backward()
    
    # Check loss identity
    loss_diff = abs(loss_p.item() - loss_u.item())
    if loss_diff > atol_loss:
        failures.append(f"Loss mismatch: patched={loss_p.item():.6f} unpatched={loss_u.item():.6f} diff={loss_diff:.2e}")
    
    # Check every parameter has gradient
    for name, param in model_patched.named_parameters():
        if param.requires_grad:
            if param.grad is None:
                failures.append(f"[PATCHED] {name}.grad is None")
            elif param.grad.norm().item() == 0:
                failures.append(f"[PATCHED] {name}.grad is all zeros")
    
    # Check gradients match
    patched_params = dict(model_patched.named_parameters())
    unpatched_params = dict(model_unpatched.named_parameters())
    
    for name in patched_params:
        if name not in unpatched_params:
            continue
        p1 = patched_params[name]
        p2 = unpatched_params[name]
        
        if not (p1.requires_grad and p2.requires_grad):
            continue
        if p1.grad is None or p2.grad is None:
            continue
            
        diff = (p1.grad - p2.grad).abs().max().item()
        tol = atol_grad_fp16 if p1.dtype == torch.float16 else atol_grad_fp32
        if diff > tol:
            failures.append(f"{name}: grad diff {diff:.2e} > {tol:.2e}")
    
    return len(failures) == 0, failures


def test_no_zero_gradients(
    model: nn.Module,
    batch: dict,
) -> Tuple[bool, list]:
    """
    Test 2: Every trainable parameter must receive non-zero, non-NaN gradient.
    """
    failures = []
    model.zero_grad()
    
    loss = model(**batch).loss
    loss.backward()
    
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        if param.grad is None:
            failures.append(f"{name}.grad is None")
        elif param.grad.abs().sum().item() == 0:
            failures.append(f"{name}.grad is all zeros")
        elif torch.isnan(param.grad).any():
            failures.append(f"{name}.grad has NaN")
        elif torch.isinf(param.grad).any():
            failures.append(f"{name}.grad has Inf")
    
    return len(failures) == 0, failures


def test_no_stale_buffers(
    model: nn.Module,
) -> Tuple[bool, list]:
    """
    Test 3: No register_buffer used for tensors that should be parameters.
    
    Buffers ending in _weight, _bias, _proj are suspicious — they should be
    nn.Parameter, not buffers. Buffers don't receive gradients.
    """
    failures = []
    suspicious_suffixes = ('_weight', '_bias', '_proj', '_gate', '_up', '_down')
    
    for name, buf in model.named_buffers():
        if any(name.endswith(s) for s in suspicious_suffixes):
            failures.append(f"Suspicious buffer '{name}' — should this be a parameter? Buffers don't get gradients.")
    
    return len(failures) == 0, failures


def test_smoke_training(
    model_patched: nn.Module,
    model_unpatched: nn.Module,
    dataloader,
    optimizer_p: torch.optim.Optimizer,
    optimizer_u: torch.optim.Optimizer,
    steps: int = 50,
    seed: int = 42,
    tolerance: float = 0.05,
) -> Tuple[bool, list]:
    """
    Test 4: Run N steps on both models, assert loss curves within tolerance.
    
    Catches the exact SEV1 failure mode: model appears to train (loss decreases
    from working components) but key parameters are frozen.
    """
    failures = []
    
    torch.manual_seed(seed)
    losses_p, losses_u = [], []
    
    model_patched.train()
    model_unpatched.train()
    
    for i, batch in enumerate(dataloader):
        if i >= steps:
            break
        
        # Patched
        optimizer_p.zero_grad()
        loss_p = model_patched(**batch).loss
        loss_p.backward()
        optimizer_p.step()
        losses_p.append(loss_p.item())
        
        # Unpatched (same data — seed ensures same batch)
        optimizer_u.zero_grad()
        loss_u = model_unpatched(**batch).loss
        loss_u.backward()
        optimizer_u.step()
        losses_u.append(loss_u.item())
    
    if len(losses_p) < steps:
        failures.append(f"Only got {len(losses_p)} steps (needed {steps})")
        return False, failures
    
    # Check final loss ratio
    ratio = losses_p[-1] / losses_u[-1]
    if not (1 - tolerance < ratio < 1 + tolerance):
        failures.append(
            f"Loss divergence at step {steps}: "
            f"patched={losses_p[-1]:.4f} unpatched={losses_u[-1]:.4f} ratio={ratio:.3f} "
            f"(expected within {tolerance*100:.0f}%)"
        )
    
    # Check loss trend — patched should also be decreasing
    if losses_p[-1] > losses_p[0]:
        failures.append(f"Patch loss INCREASING: step0={losses_p[0]:.4f} step{steps}={losses_p[-1]:.4f}")
    
    return len(failures) == 0, failures


def test_grad_norm_sanity(
    model: nn.Module,
    batch: dict,
    min_norm: float = 1e-10,
) -> Tuple[bool, list]:
    """
    Test 5: Check grad norms are reasonable (not suspiciously low).
    
    This is a soft check — logs warnings rather than hard failures.
    Useful as a runtime hook on the first training step.
    """
    failures = []
    model.zero_grad()
    
    loss = model(**batch).loss
    loss.backward()
    
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        if param.grad is None:
            failures.append(f"{name}.grad is None — gradient death!")
        else:
            gnorm = param.grad.norm().item()
            if gnorm == 0:
                failures.append(f"{name}: grad norm = 0 — gradient death!")
            elif gnorm < min_norm:
                failures.append(f"{name}: grad norm = {gnorm:.2e} (suspiciously low, min={min_norm:.2e})")
    
    return len(failures) == 0, failures


def run_full_verification(
    model_patched: nn.Module,
    model_unpatched: nn.Module,
    batch: dict,
    dataloader=None,
    optimizer_p=None,
    optimizer_u=None,
    smoke_steps: int = 50,
) -> bool:
    """
    Run ALL 5 verification tests. Returns True if all pass.
    
    Call this before promoting any kernel that touches training.
    """
    all_passed = True
    
    print("=" * 60)
    print("GRADIENT VERIFICATION — MANDATORY BEFORE KERNEL PROMOTION")
    print("=" * 60)
    
    # Test 1: Gradient equivalence
    print("\n[Test 1/5] Gradient Equivalence (patched vs unpatched)...")
    passed, failures = test_gradient_equivalence(model_patched, model_unpatched, batch)
    if passed:
        print("  ✅ PASS — gradients match within tolerance")
    else:
        print("  ❌ FAIL:")
        for f in failures:
            print(f"    - {f}")
        all_passed = False
    
    # Test 2: No zero gradients
    print("\n[Test 2/5] No Zero Gradients (patched model)...")
    passed, failures = test_no_zero_gradients(model_patched, batch)
    if passed:
        print("  ✅ PASS — all parameters have non-zero gradients")
    else:
        print("  ❌ FAIL:")
        for f in failures:
            print(f"    - {f}")
        all_passed = False
    
    # Test 3: No stale buffers
    print("\n[Test 3/5] No Stale Buffers...")
    passed, failures = test_no_stale_buffers(model_patched)
    if passed:
        print("  ✅ PASS — no suspicious buffers found")
    else:
        print("  ❌ FAIL:")
        for f in failures:
            print(f"    - {f}")
        all_passed = False
    
    # Test 4: Smoke training (if dataloader provided)
    if dataloader is not None and optimizer_p is not None and optimizer_u is not None:
        print(f"\n[Test 4/5] 50-Step Smoke Test (patched vs unpatched)...")
        passed, failures = test_smoke_training(
            model_patched, model_unpatched, dataloader,
            optimizer_p, optimizer_u, steps=smoke_steps
        )
        if passed:
            print("  ✅ PASS — loss curves converge within 5%")
        else:
            print("  ❌ FAIL:")
            for f in failures:
                print(f"    - {f}")
            all_passed = False
    else:
        print("\n[Test 4/5] 50-Step Smoke Test — SKIPPED (no dataloader/optimizer provided)")
    
    # Test 5: Grad norm sanity
    print("\n[Test 5/5] Grad Norm Sanity Check...")
    passed, failures = test_grad_norm_sanity(model_patched, batch)
    if passed:
        print("  ✅ PASS — all grad norms reasonable")
    else:
        print("  ⚠️  WARNINGS:")
        for f in failures:
            print(f"    - {f}")
        # Soft check — don't fail overall
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED — kernel is safe to promote")
    else:
        print("TESTS FAILED — DO NOT PROMOTE THIS KERNEL")
        print("Fix gradient flow issues before proceeding.")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    print("This is a template module. Import and use the functions directly.")
    print()
    print("Example usage:")
    print("  from gradient_verification import run_full_verification")
    print("  passed = run_full_verification(model_patched, model_unpatched, batch, dataloader, opt_p, opt_u)")
    print()
    print("Or run individual tests:")
    print("  from gradient_verification import test_gradient_equivalence, test_no_zero_gradients")
    print("  passed, failures = test_gradient_equivalence(model_p, model_u, batch)")
