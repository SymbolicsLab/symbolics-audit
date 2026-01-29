# Truth-Invariance Theorem (Metabolism Impossibility)

**Date**: 2026-01-29 (updated Phase 3A.5)
**Status**: ✓ PROVEN (Agda, `--safe --without-K`)
**Related**: conjectures/SWITCH-BOUND.md, conjectures/OPERATIONS.md, conjectures/PROOF-PLAN.md

---

## Main Result

Under canonical semantics (absorption-based decay, aggregate-preserving operations),
**truth conflict cannot be created or destroyed**. It can only be present or absent
from the initial conditions.

---

## Formal Statement

### Theorem SB-1 (Canonical System)

For all trajectories τ under canonical semantics:
```
switches(τ) = 0
```

### Corollary

"Metabolic cycling" (sustained oscillation in truth conflict) is **impossible**
without adding an operator that changes truth values.

---

## Why This Happens

### The Channel Separation

The system has two orthogonal channels:
1. **Truth channel**: In/Out/Both/Neither (support for propositions)
2. **Resolution channel**: Res/Unres (commitment status, "pressure")

Under canonical semantics:

| Operation | Changes Truth? | Changes Resolution? |
|-----------|:-------------:|:------------------:|
| DoStabilize (aggregate) | NO | NO |
| DoExplore (unfold) | NO | YES (adds Unres) |
| DoDecay (absorb) | NO | NO |

**No operation changes truth**, so truth conflict is invariant.

### The Algebraic Explanation

1. **aggregate** adds the join of existing cuts
   - `Agg(Agg(C) :: C) = Agg(C)` (idempotent via join idempotence)
   - Cannot introduce new truth values

2. **unfold** adds `sideRem = mkSide Neither Unres`
   - `Neither ⊔ᵗ t = t` (Neither is identity for truth join)
   - Can only add pressure (Unres), not truth content

3. **decay_absorb** removes absorbed cuts
   - `Agg(decay_absorb(C)) = Agg(C)` (removes only redundant cuts)
   - Preserves aggregate exactly

---

## What "Metabolism" Would Require

For sustained conflict cycling, the system needs an operator that:
1. Can CREATE truth conflict (Both) from non-conflict, AND
2. Can DESTROY truth conflict

Under canonical semantics, **neither exists**.

### The Placeholder Accident

The earlier observed "metabolic tension" (22.5% with 3+ switches) was caused by
a placeholder fold implementation:

```typescript
// PLACEHOLDER (wrong):
case 'aggregate':
  return uniformCut(sideIn);  // Injected In everywhere!
```

This accidentally created an operator that:
- Injected `In` at every element
- Combined with existing `Out` to create `Both` (conflict)
- Was a hidden "novelty source" that didn't exist in the formal spec

Removing the placeholder removed the oscillation, confirming the diagnosis.

---

## The Drop-Persistent-Conflict Variant

If we add `decay_dropConflict` (which intentionally changes truth):

### Theorem SB-2 (Drop-Conflict System)
```
switches(τ) ≤ 1
```

This decay can:
- Resolve conflict (Both → Neither/Unres)
- Cause one switch: conflict → no conflict

But no operation can **re-create** conflict after resolution:
- aggregate adds aggregate (which has no conflict after resolution)
- unfold adds Neither (can't create In or Out)

So conflict can only disappear, not return.

---

## Implications

### For the Project

1. The initial "metabolic tension" result was an **artifact** of placeholders
2. Canonical semantics is **truth-inert** by construction
3. **Genuine metabolism requires explicit design** of a novelty operator

### For Future Work

To achieve metabolic cycling, one must add:
- An **evidence interface** that injects truth support (In/Out)
- An **unfold operator** that generates In/Out (not just Neither)
- A **non-conservative transformation** that flips truth values

This is now a **design choice**, not an emergent property.

---

## Proven Lemmas (Agda)

| Lemma | Statement | Status | Location |
|-------|-----------|--------|----------|
| L8 | Aggregate idempotence | ✓ PROVEN | `SwitchBound.agda:129-130` |
| L9 | Unfold preserves truth | ✓ PROVEN | `SwitchBound.agda:175-192` |
| L10-core | Absorbed cuts don't contribute | ✓ PROVEN | `SwitchBound.agda:223-225` |
| L12 | Neither can't create conflict | ✓ PROVEN | `SwitchBound.agda:70-71` |
| T1-stabilize | DoStabilize preserves truthOfAgg | ✓ PROVEN | `SwitchBound.agda:250` |
| T1-explore | DoExplore preserves truthOfAgg | ✓ PROVEN | `SwitchBound.agda:254` |

All proofs compile with `agda --safe --without-K`.

---

## The Posture

You can now credibly say:

> **Theorem (Truth-Invariance)**: Under canonical semantics—where aggregate is
> pointwise join, decay removes only absorbed cuts, stabilize adds the aggregate,
> and explore adds identity cuts—the truth component of the aggregate is invariant.
>
> **Corollary (SB-1)**: `switches(τ) = 0` for all trajectories.
>
> **Proof**: Agda, `--safe --without-K`. See `symbolics-core/src/Mechanics/SwitchBound.agda`.

Consequently, "metabolic cycling" (sustained oscillation in truth conflict)
is structurally impossible without adding an explicit novelty operator.

The earlier observed oscillation was caused by a placeholder implementation
that accidentally injected truth support. Removing the placeholder removed
the oscillation, confirming the structural diagnosis.

This is a clean, honest, **machine-verified** result. It explains both what the
system does (stabilize) and what it cannot do (cycle) without external intervention.

---

## See Also

- `conjectures/SWITCH-BOUND.md` - Formal theorem statements
- `conjectures/OPERATIONS.md` - Operation semantics
- `conjectures/PROOF-PLAN.md` - Agda formalization plan
- `experiments/canonical-tension/RESULTS.md` - Empirical evidence
- `DESIGN-DECISIONS.md` DD-010 - Canonical vs variant decay
