# Design Decisions

**Date**: 2026-01-29
**Context**: Post-Phase 2.5 Research Fork

This document captures pending and resolved architectural decisions for the Symbolics project.

---

## DD-001: Research Direction After Ablation Study

**Status**: PENDING

**Context**: The ablation study (Phase 2.5) showed that the "metabolic tension" phenomenon was an artifact of placeholder semantics. Under canonical Agda semantics:

- Maximum switches: 2 (not 3+)
- Runs with ≥3 switches: 0% (not 22.5%)
- The system is conservative and reaches stable termination

**Decision Required**: What is the research direction for Phase 3?

### Option A: Accept Stability as the Result

**Summary**: The formal system is conservative. Document what it actually does.

**Implications**:
- The "metabolism" metaphor may not apply to this system
- The research contribution is the rigorous formalization, not emergent dynamics
- Focus shifts to what the stable states represent

**Deliverables**:
- Complete documentation of system behavior
- Formal proof of 2-switch bound (if achievable)
- Paper on conservative paraconsistent aggregation

**Risk**: Limited novelty if stability was expected

### Option B: Add Legitimate Novelty Source

**Summary**: Design an evidence interface or unfold operator that introduces new information in a principled way.

**Implications**:
- Must be formally specified in Agda
- Must satisfy conservativity constraints
- Cannot be a hidden forcing function (the placeholder was effectively this)

**Candidate Mechanisms**:

1. **Evidence Interface**
   - External observations that introduce new cuts
   - Example: sensor readings, user inputs, external events
   - Constraint: Must not create information from nothing

2. **Unfold Operator**
   - Currently a stub in TypeScript
   - Would expand compressed representations into explicit cuts
   - Agda has spec but no implementation

3. **Stochastic Perturbation**
   - Random noise injection with formal bounds
   - Would need probability monad in Agda
   - Risk: May just be a dressed-up forcing function

**Deliverables**:
- Formal specification of novelty source
- Proof of conservativity properties
- Experiments showing emergent dynamics (if they exist)

**Risk**: May discover that any legitimate novelty source still converges

### Option C: Explore Different Configurations

**Summary**: The current configuration (aggregate + drop-persistent-conflict + homeostatic) may be conservative by design. Test alternatives.

**Configurations to Test**:

| Component | Current | Alternative |
|-----------|---------|-------------|
| Fold | aggregate | consensus, weighted |
| Decay | drop-persistent-conflict | probabilistic, threshold |
| Policy | homeostatic | crystalline, random |

**Implications**:
- Systematic parameter search
- May find configurations with richer dynamics
- Does not require new formal machinery

**Deliverables**:
- Sweep across configuration space
- Identify configurations with different behaviors
- Characterize which configurations are conservative

**Risk**: May find all configurations are conservative (structural property)

### Recommendation

Start with **Option C** (low cost, informs A/B choice), then:
- If rich dynamics found → investigate formally
- If all conservative → either Option A (document) or Option B (add novelty)

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

## Pending Decisions Summary

| ID | Topic | Status | Blocking |
|----|-------|--------|----------|
| DD-001 | Research Direction | PENDING | Phase 3 |
| DD-002 | Unfold Semantics | PENDING | DD-001 |
| DD-003 | Decay Mechanisms | PENDING | DD-001 |

## Resolved Decisions Summary

| ID | Topic | Decision |
|----|-------|----------|
| DD-004 | Subsumption Order | Resolution order (≤ʳ) |
| DD-005 | Empty Aggregate | Neither/Res |
| DD-006 | Update Semantics | Add + remove subsumed |
| DD-007 | Test Oracle | Three-layer validation |
| DD-008 | Domain Size | |U|=15 default |

---

## See Also

- `PROJECT-STATUS.md` - Current project state
- `RESEARCH-QUESTIONS.md` - Open and resolved questions
- `LIMITATIONS.md` - Known gaps and their status
- `experiments/canonical-tension/RESULTS.md` - Ablation study data
