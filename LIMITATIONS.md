# Known Limitations and Gaps

**Last Updated**: 2026-01-29

This document lists known gaps between claims and implementation/proof in the Symbolics project. It is intended to ensure epistemic honesty and guide future work.

---

## Implementation Gaps

### TypeScript Folds (CRITICAL)

**Location**: `symbolics-dsl/src/runtime/interpreter.ts:72-99`

**Status**: Placeholder implementations that return uniform cuts

```typescript
case 'aggregate':
  return uniformCut(sideIn);  // Does NOT actually aggregate existing cuts
case 'unfold':
  return uniformCut(sideRem); // Just adds uniform Rem, doesn't "unfold" anything
case 'consensus':
  return uniformCut(sideIn);  // Placeholder
```

**What should happen**:
- `aggregate` should compute the join of all existing cuts in context
- `unfold` should expand articulation capacity based on existing distinctions
- `consensus` should only commit where there's agreement

**Impact**:
- DSL runtime does NOT implement Agda semantics
- All experiment results reflect placeholder behavior
- "Agda-TS equivalence" is not established

**Priority**: CRITICAL - Fix before any further experiments

---

### Subsumption Check (CRITICAL)

**Location**: `symbolics-core/Mechanics/Context.agda:163-164`

**Status**: Always returns `true` (placeholder)

```agda
checkAll : ∀ {ℓ} (U : Set ℓ) → Cut U → Cut U → Bool
checkAll U d c = true  -- Placeholder: always assume not subsumed
```

**What should happen**: Check if cut `d` is subsumed by `c` (i.e., `c` provides all of `d`'s information)

**Impact**:
- `update` function cannot garbage-collect redundant cuts
- Claims about bounded context growth are unfounded
- Decay dynamics do not work as intended

**Why it's hard**: "We can't actually check all u : U in general (U might be infinite)"

**Suggested fix**: Implement for finite domains via the existing `FiniteSystem` structure

**Priority**: CRITICAL - Required for decay to work correctly

---

### Agda-TS Semantic Equivalence

**Status**: Not established

**What exists**:
- Agda types and operations
- TypeScript types and operations that mirror the surface API
- Golden tests that check TypeScript output format

**What's missing**:
- No test that compares Agda evaluation to TypeScript evaluation
- No proof or evidence that they compute the same results
- TypeScript uses placeholders, so they definitely diverge

**Impact**: Any claim of "equivalence" or "matching semantics" is unfounded

**Priority**: HIGH - Establish after fixing placeholder implementations

---

## Proof Gaps

### Lyapunov / Potential Framework (MAJOR)

**Location**: `symbolics-core/Mechanics/Potential/Conjectures.agda`

**Status**: 7 unproven postulates (file cannot compile with `--safe`)

```agda
postulate
  potential-zero-iff-in-window-forward : ...
  in-window-implies-zero-potential : ...
  stabilize-reduces-potential-above : ...
  explore-maintains-potential-below : ...
  adaptive-step-bounds-potential : ...
  convergence-to-equilibrium : ...
  potential-is-lyapunov : ...  -- THE MASTER CONJECTURE
```

**What these claim**:
- There exists a potential function that decreases under adaptive steps
- The system converges to an equilibrium (the homeostatic window)
- The dynamics are Lyapunov-stable

**Impact**: All claims about convergence and stability in the "metabolism" model are **unproven assertions**

**Priority**: HIGH - Either prove these or mark all downstream claims as conjecture

---

### Fold Idempotence (SPEC-FOLD-002)

**Status**: Conjecture in registry

**Claim**: `fold(fold(c)) ≈ fold(c)` (applying fold twice is same as once)

**What exists**: No Agda proof. Registry notes "may require preconditions on canonical fold implementation"

**Impact**: Without idempotence, we can't guarantee that repeated stabilization converges

---

### Fold Conservativity (SPEC-FOLD-003)

**Status**: Conjecture in registry

**Claim**: Fold doesn't "fabricate" information not already in context

**What exists**: No Agda proof

**Impact**: Without conservativity, folds might add spurious data

---

## Experiment Limitations

### Metabolic Tension Results (Phase 11d) - **INVALIDATED**

**Location**: `symbolics-dsl/experiments/metabolic-tension/`

**Status**: **ARTIFACT OF PLACEHOLDER IMPLEMENTATION**

Phase 2.5 ablation study demonstrated that the "metabolic tension" results were artifacts:

| Finding | Placeholder | Canonical |
|---------|-------------|-----------|
| Max switches | 3 | **2** |
| Mean switches | 1.90 | **1.16** |
| "Tension zone" (≥3) | 22.5% | **0.0%** |

**The "metabolic cycling" phenomenon does not occur under canonical Agda semantics.**

See `symbolics-dsl/experiments/canonical-tension/RESULTS.md` for the ablation analysis.

### What Was Artifact

1. **Placeholder `aggregate`**: Returned `uniformCut(sideIn)` instead of actual join
2. This injected positive evidence everywhere
3. Mixed with Out values to create artificial conflicts
4. Decay + explore created oscillation not present in real semantics

### Canonical Semantics Results

With real Agda semantics (Phase 2):
- **Maximum switches**: 2 (conflict can appear, resolve, return once)
- **No sustained cycling**: After one return, conflicts resolve permanently
- **96.7% reach stability**: System converges, doesn't oscillate

---

## Conceptual Gaps

### Why Belnap?

**Status**: Choice not formally justified

**Question**: Why four-valued (Neither, In, Out, Both) rather than three-valued (false, unknown, true) or other paraconsistent logics?

**What's needed**: Property-driven argument showing what specifically requires Both ≠ Neither

---

### Agent Agency

**Status**: "Agent" is a misnomer

**Reality**: The AgentSpec defines a policy executor, not an agent with:
- Goals or preferences
- Utility function
- Decisions under uncertainty
- Learning or adaptation

**The "agent" just applies fixed policy rules**: if pressure > hi, stabilize; if pressure < lo, explore

---

### "Healthy" Circularity

**Status**: Circular definition risk

**Problem**:
- "Healthy" = homeostatic regime (pressure in [lo, hi])
- Thresholds lo and hi are chosen to produce "healthy" behavior
- This risks circularity: we define healthy as what we configured the system to do

---

## Edge Cases Not Handled

| Edge Case | Status | Risk |
|-----------|--------|------|
| Empty domain | Returns early in analyze(), untested in run() | Unknown behavior |
| lo = hi | Triggers DoDecay forever | Infinite loop possible |
| All Both from start | Not tested | May be irrecoverable (monotonic join) |
| maxSteps = 1 | Not tested | Stability tracking meaningless |
| Single element domain | Not tested | Degenerate behavior likely |

---

## Tracking

### To Fix (Priority Order)

1. [ ] Implement real fold aggregation in TypeScript
2. [ ] Implement subsumption check for finite domains
3. [ ] Add Agda-TS equivalence tests
4. [ ] Prove or downgrade Lyapunov conjectures
5. [ ] Run sensitivity analysis on tension zone thresholds
6. [ ] Test across domain sizes
7. [ ] Justify Belnap choice

### Tracked In

- This file (LIMITATIONS.md) - overview
- Individual CLAUDE.md files - per-repository details
- symbolics-audit/spec/registry.yaml - per-spec status
