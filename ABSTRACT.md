# Research Summary

**Project**: Symbolics — Formal Foundations for Paraconsistent Symbolic Dynamics
**Date**: 2026-01-29
**Status**: Phase 3B Complete

---

## Overview

We define a canonical folding dynamics over Belnap-style four-valued truth
(Neither, In, Out, Both) with a two-channel Side structure (truth × resolvedness).
The system models symbolic agents that process contradictory information without
explosion, maintaining truth commitments through fold/unfold operations.

---

## Results

### Phase 3A: Truth-Invariance Under Canonical Operations

In the conservative system (no truth removal), the truth component of the
aggregate is invariant under DoStabilize, DoExplore, and decay_absorb.

**Theorem (SB-1)**: `switches(τ) = 0` for all trajectories under canonical semantics.

**Status**: Proven in Agda (`--safe --without-K`)

**Key lemmas**:
- L8: Aggregate idempotence
- L9: Unfold preserves truthOf
- L10: Decay preserves aggregate
- Truth homomorphism: `truthOf(a ⊔ˢ b) = truthOf(a) ⊔ᵗ truthOf(b)`

### Phase 3B.2: Additive Evidence Bound

Introducing exogenous evidence (external truth injection) breaks truth-invariance
but remains monotone. Truth support can only increase under additive evidence.

**Proposition**: `switches(τ) ≤ 1` under additive evidence with no truth-removal.

**Status**: Empirically verified (TypeScript property tests, 100% pass rate)

### Phase 3B.3: TTL Enables Non-Monotone Dynamics

TTL-based forgetting (evidence expires after k steps) introduces non-monotone
truth dynamics. Truth support can now decrease when evidence expires.

**Result**: `switches > 1` is achievable with finite TTL.

**Status**: Demonstrated (unit tests confirm switches up to 23)

### Phase 3B.4: Phase Diagram Characterization

A preregistered phase diagram sweep mapped the (n, k, λ) parameter space:
- n ∈ {5, 10, 20} (domain size)
- k ∈ {3, 5, 10, 20, ∞} (TTL / memory horizon)
- λ ∈ {0.25, 0.5, 0.75, 1.0} (evidence rate)
- 20 seeds per cell, 1200 total runs

**Key findings**:

| k   | Max Switches | % Sustained (≥4) | Regime          |
|-----|--------------|------------------|-----------------|
| 3   | 23           | 38.8%            | Robust cycling  |
| 5   | 5            | 6.3%             | Marginal        |
| 10  | 2            | 0%               | No cycling      |
| 20  | 2            | 0%               | No cycling      |
| ∞   | 1            | 0%               | Monotone bound  |

**Best configuration**: n=5, k=3, λ=0.75 → 86.3% sustained cycling

---

## Theoretical Contribution

### Proposition: Monotonicity Necessity

If truth support is monotone non-decreasing over time, then `switches ≤ 1`.

**Contrapositive**: `switches > 1` requires non-monotone truth dynamics.

**Interpretation**: "Metabolism requires forgetting" — sustained cycling is only
possible when truth support can be removed, not just added.

### Non-Monotone ≠ Sustained Cycling

Non-monotonicity is *necessary but not sufficient*. Even with TTL:
- k=10: non-monotone but no sustained cycling
- k=3: non-monotone AND robust sustained cycling

The memory horizon must be short enough for contradictory evidence to
repeatedly overlap and separate.

---

## Conclusion

Sustained cycling ("metabolism") requires:
1. **External novelty**: Evidence injection (breaks truth-invariance)
2. **Forgetting**: TTL-based expiration (breaks monotonicity)
3. **Short memory horizon**: k ≈ 3 (enables repeated conflict cycles)

Without forgetting, the system monotonically accumulates truth and stabilizes.
With forgetting, the system can exhibit ongoing conflict dynamics — the
operational signature of a "living" symbolic agent.

---

## Artifacts

### Agda Proofs
- `symbolics-core/src/Mechanics/SwitchBound.agda`
- Truth-invariance theorem (SB-1) with supporting lemmas

### TypeScript Implementation
- `symbolics-dsl/src/runtime/` — Full runtime with evidence and TTL
- `symbolics-dsl/test/` — 167 tests (all passing)

### Experiments
- `symbolics-dsl/experiments/phase-diagram/` — Phase diagram sweep
- `symbolics-dsl/experiments/additive-evidence/` — Baseline verification
- `symbolics-dsl/experiments/ttl-cycling/` — TTL demonstration

### Documentation
- `symbolics-audit/conjectures/` — Formal propositions
- `symbolics-audit/spec/` — Specifications
