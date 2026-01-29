# Design Decisions

**Date**: 2026-01-29
**Context**: Post-Phase 2.5 Research Fork

This document captures pending and resolved architectural decisions for the Symbolics project.

---

## DD-001: Research Direction After Ablation Study

**Status**: DECIDED

**Decision**: Phase 3A - Prove a switch bound under canonical semantics

**Context**: The ablation study (Phase 2.5) showed that the "metabolic tension" phenomenon was an artifact of placeholder semantics. Under canonical Agda semantics:

- Maximum switches: 2 (not 3+)
- Runs with ≥3 switches: 0% (not 22.5%)
- The system is conservative and reaches stable termination

**Rationale**:
1. Empirical pattern (max switches ≤ 2) suggests a theorem exists
2. Proving any bound is a strong result independent of "metabolism" narrative
3. If proven, "metabolism" becomes an earned property requiring additional structure
4. This is the shortest path to a theory+proof contribution

**Consequences**:
- Focus Agda work on convergence/monotonicity for canonical semantics
- Defer novelty sources (evidence interface, unfold) until bound is understood
- If bound is proven, metabolism requires explicit justification for any novelty source

**Test Obligations**:
- Formalize the conjecture in Agda (see `conjectures/SWITCH-BOUND.md`)
- Either prove or find counterexample
- If counterexample found, characterize when bound holds vs fails

**Outcome Interpretation**:

If switch bound is **proven**:
> "Under canonical semantics, the system provably stabilizes with at most K conflict transitions. Metabolism (sustained cycling) only appears when we add [evidence stream / unfold / non-monotone policy]; otherwise the system converges."

If switch bound is **disproven**:
> "The switch bound fails under [specific conditions]. This characterizes when cycling is possible without external novelty."

Either way, we win.

### Options Considered (for reference)

**Option A: Accept Stability**
- Document conservative behavior as the result
- Risk: Limited novelty if stability was expected

**Option B: Add Novelty Source**
- Design evidence interface or unfold operator
- Risk: May still converge; requires new formal machinery

**Option C: Explore Configurations**
- Test alternative folds, decays, policies
- Risk: May find all configurations are conservative

**Why Phase 3A chosen**: Proving a bound is the minimal path to a strong result. It transforms "the system is stable" into "the system is provably stable", which is substantial. Options B/C can follow if the bound is proven

---

## DD-002: Unfold Operator Semantics

**Status**: PENDING (blocked by DD-001)

**Context**: The unfold operator is currently a stub that returns identity. The Agda spec exists but implementation is missing.

**Question**: What should unfold actually do?

### Current State

TypeScript (`fold-expr.ts`):
```typescript
case 'unfold':
  return state.context[0] ?? uniformCut(sideNeither);  // Stub
```

Agda (`FoldLibrary.agda`):
```agda
unfold : Ctx → Ctx
unfold = ?  -- Not implemented
```

### Option U1: Conservative Unfold

**Definition**: Unfold expands a cut into its constituent "reasons" without adding information.

**Example**: If `cut(a) = Both`, unfold produces two cuts:
- `cut₁(a) = In, cut₁(b) = Neither`
- `cut₂(a) = Out, cut₂(b) = Neither`

**Property**: `aggregate(unfold(c)) ⊑ c` (unfold is information-preserving)

**Use Case**: Debugging, explanation, attribution

### Option U2: Generative Unfold

**Definition**: Unfold uses structure to generate new cuts that extend beyond the input.

**Example**: If `cut(a) = In` and `a R b` (some relation), unfold might infer:
- `cut'(b) = In` (propagation along relation)

**Property**: `aggregate(unfold(c)) ⊒ c` (unfold adds information)

**Use Case**: Inference, exploration, discovery

**Risk**: This is where hidden forcing functions live

### Option U3: Stochastic Unfold

**Definition**: Unfold samples from a distribution over consistent extensions.

**Property**: Probabilistic guarantees rather than deterministic

**Use Case**: Exploration under uncertainty

**Risk**: Requires probability monad, harder to verify

### Recommendation

Defer until DD-001 is resolved. If Option A chosen, unfold is not needed. If Option B chosen, unfold is the primary candidate for novelty source.

---

## DD-003: Decay Mechanism Design

**Status**: PENDING

**Context**: Current decay (`drop-persistent-conflict`) drops one side of persistent conflicts. This may be too aggressive.

**Question**: What decay mechanisms should be supported?

### Current Mechanism

```typescript
// drop-persistent-conflict
if (persistCount >= threshold) {
  // Drop sideOut, emit pressure
  return { ...side, truth: { supportsIn: side.truth.supportsIn, supportsOut: false } };
}
```

### Alternative Mechanisms

| Mechanism | Description | Conservativity |
|-----------|-------------|----------------|
| `none` | No decay | Trivially conservative |
| `drop-persistent-conflict` | Drop one side after N steps | Conservative |
| `probabilistic-decay` | Random chance to resolve | Stochastic |
| `threshold-decay` | Decay only above pressure threshold | Conservative |
| `forget-stale` | Remove old cuts entirely | Not conservative |

### Design Criteria

1. **Formal Specification**: Must be expressible in Agda
2. **Conservativity Proof**: Should not create information
3. **Behavior Diversity**: Should enable different dynamics
4. **Composability**: Should work with different policies

### Recommendation

Keep current mechanism as default. Add `probabilistic-decay` as experimental option if DD-001 → Option B.

---

## DD-004: Subsumption Semantics Clarification

**Status**: RESOLVED

**Decision**: Use resolution order (≤ʳ) from Finite.agda, not knowledge order.

**Rationale**: Resolution order tracks "commitment" where:
- `sideOut` is bottom (no commitment)
- `sideBoth` is top (conflicting commitment)

This differs from knowledge order where `Both` represents maximum information.

**Implementation**: `sideLeq` in `side.ts` implements resolution order.

**Documentation**: CANONICAL-SEMANTICS.md Section 4.3

---

## DD-005: Empty Aggregate Identity

**Status**: RESOLVED

**Decision**: Empty aggregate returns `mkSide Neither Res`, not `sideOut`.

**Rationale**: From Agda Context.agda:
```agda
joinAllRes [] = mkSide Neither Res
```

`Neither` means "no information" while `Out` would mean "negative information".

**Implementation**: `aggregateCut` in `context.ts`

**Tests**: Agda grounding test case 1, semantic equivalence tests

---

## DD-006: Update Semantics (Add vs Replace)

**Status**: RESOLVED

**Decision**: Use Finite.agda semantics (add + remove subsumed).

**Rationale**: Context.agda has two update patterns:
1. `addCut` (no removal) - used for building contexts
2. `updateWithDecay` in Finite.agda - adds new, removes subsumed

The latter matches the simulation semantics.

**Implementation**: `updateContext` in `context.ts`

---

## DD-007: Test Oracle Strategy

**Status**: RESOLVED

**Decision**: Three-layer validation (reference evaluator + Agda grounding + semantic equivalence).

**Rationale**: Reduces shared-bug risk by having:
1. Minimal reference implementation
2. Values computed directly from Agda definitions
3. Cross-validation between runtime and reference

**Implementation**:
- `src/reference/evaluator.ts` - Reference implementation
- `test/agda-grounding.test.ts` - Agda-derived test cases
- `test/semantic-equivalence.test.ts` - Runtime vs reference

---

## DD-008: Domain Size for Experiments

**Status**: RESOLVED

**Decision**: Use |U|=15 as default, with scaling tests at 5, 10, 30.

**Rationale**:
- |U|=15 provides enough elements for diverse initialization
- Not so large that experiments are slow
- Scaling tests confirm behavior is invariant to domain size

**Evidence**: All domain sizes show max=2 switches, confirming structural bound.

---

## DD-009: Subsumption Order for Decay

**Status**: RESOLVED

**Decision**: Use absorption order (`a ≤ b ⟺ join(a,b) = b`) for decay subsumption.

**Context**: Resolution order (DD-004) was found to NOT preserve aggregate during decay.
Testing showed only 70% of cases preserved aggregate under resolution order.

**Rationale**:
- Resolution order says `Rem ≤ In`, but `join(Rem, In) = In/Unres ≠ In`
- Removing "subsumed" cuts could lose the `Unres` contribution
- Absorption order guarantees: if `d ≤ c`, then `join(d, c) = c`
- This makes decay semantics-preserving by construction

**Consequence**:
- **100% of exhaustive tests pass** (was 70%)
- Decay provably preserves aggregate
- Switch bound proof is now feasible

**Implementation**:
- `sideAbsorbedBy(a, b)`: checks `join(a,b) = b`
- `isSubsumed` now uses `sideAbsorbedBy`
- `sideLeq` remains for policy decisions (resolution order)

---

## Pending Decisions Summary

| ID | Topic | Status | Blocking |
|----|-------|--------|----------|
| DD-002 | Unfold Semantics | PENDING | Switch bound result |
| DD-003 | Decay Mechanisms | PENDING | Switch bound result |

## Resolved Decisions Summary

| ID | Topic | Decision |
|----|-------|----------|
| DD-001 | Research Direction | Phase 3A: Prove switch bound |
| DD-004 | Subsumption Order (Policy) | Resolution order (≤ʳ) |
| DD-005 | Empty Aggregate | Neither/Res |
| DD-006 | Update Semantics | Add + remove subsumed |
| DD-007 | Test Oracle | Three-layer validation |
| DD-008 | Domain Size | |U|=15 default |
| DD-009 | Subsumption Order (Decay) | Absorption order (≤ⱼ) |

---

## See Also

- `PROJECT-STATUS.md` - Current project state
- `RESEARCH-QUESTIONS.md` - Open and resolved questions
- `LIMITATIONS.md` - Known gaps and their status
- `experiments/canonical-tension/RESULTS.md` - Ablation study data
