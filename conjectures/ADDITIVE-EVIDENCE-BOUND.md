# Proposition: Additive Evidence Switch Bound

**Date**: 2026-01-29
**Status**: EMPIRICALLY VERIFIED (TypeScript property tests)
**Related**: SWITCH-BOUND.md, EVIDENCE-INTERFACE.md

---

## Statement

Under additive evidence with monotone join and no truth-removal/forgetting:
- `conflictOn` can switch at most once (false → true)
- Conflict mass is non-decreasing over time
- `switches(τ) ≤ 1` for all trajectories

---

## Intuition

1. **Join is monotone in the truth lattice**:
   - `Neither ≤ In, Out ≤ Both`
   - `a ⊔ b ≥ a` and `a ⊔ b ≥ b`

2. **Evidence only adds truth support**:
   - DoIngest adds a cut to context
   - Aggregate joins all cuts
   - Truth can only increase in the lattice

3. **Both is absorbing**:
   - Once `truthOf(Agg)(u) = Both`, it stays Both
   - No operation can reduce truth below Both
   - `Both ⊔ anything = Both`

4. **Consequence for conflictOn**:
   - `conflictOn = ∃u. truthOf(Agg)(u) = Both`
   - Once any element reaches Both, conflictOn = true
   - Cannot return to false without truth-removal

---

## Formal Statement

**Proposition (Additive Evidence Bound)**

Let τ be a trajectory under:
- Canonical operations (DoStabilize, DoExplore, decay_absorb)
- Plus DoIngest (adds evidence cut to context)
- Evidence cuts can contain In, Out, Both, Neither at each element
- No truth-removal mechanism (no TTL, no forgetting)

Then:
1. `switches(τ) ≤ 1`
2. If `conflictOn(s_t) = true`, then `conflictOn(s_{t'}) = true` for all `t' > t`
3. `conflictMass(s_t) ≤ conflictMass(s_{t+1})` (non-decreasing)

---

## Proof Sketch

### Lemma: Truth aggregate is monotone under DoIngest

For any evidence e and context C:
```
truthOf(Agg(C))(u) ≤ᵗ truthOf(Agg(e.cut :: C))(u)
```

**Proof**:
1. `Agg(e.cut :: C)(u) = e.cut(u) ⊔ˢ Agg(C)(u)` (fold lemma)
2. `truthOf(a ⊔ˢ b) = truthOf(a) ⊔ᵗ truthOf(b)` (truth homomorphism)
3. `a ⊔ᵗ b ≥ᵗ b` (join is upper bound)
4. Therefore `truthOf(Agg(e.cut :: C))(u) ≥ᵗ truthOf(Agg(C))(u)` ∎

### Corollary: Conflict mass is non-decreasing

Since truth at each element can only increase (or stay same), and Both is the maximum:
- Elements with Both stay at Both
- Elements below Both can reach Both but not leave it
- Count of Both elements is non-decreasing ∎

### Corollary: switches ≤ 1

- `conflictOn = ∃u. truthOf(Agg)(u) = Both`
- Once true, cannot become false (would require truth decrease)
- Boolean that can only go false→true has at most 1 switch ∎

---

## Comparison to Canonical Semantics

| System | switches bound | Proof |
|--------|---------------|-------|
| Canonical (no evidence) | 0 | SB-1 (proven) |
| Canonical + evidence (additive) | ≤ 1 | This proposition |
| Canonical + evidence + TTL | ? | Phase 3B.3 |

---

## Implication

**Additive evidence alone does not produce metabolic cycling.**

To achieve cycling (switches > 1), the system needs a mechanism to:
1. Create conflict (evidence provides this)
2. Remove conflict (requires truth-removal/forgetting)

This motivates Phase 3B.3: Evidence TTL (Time-To-Live).

---

## Verification Plan

### Empirical (TypeScript) - COMPLETE
- [x] Property test: conflict mass non-decreasing
- [x] Property test: conflictOn only goes false→true
- [x] Property test: switches ≤ 1
- [x] Baseline experiment with parameter sweep (8 seeds × 30 items)

Results: `experiments/additive-evidence/RESULTS.md`

### Formal (Agda, optional)
- [ ] truth-agg-monotone-ingest lemma
- [ ] conflictOn-monotone corollary

---

## See Also

- `SWITCH-BOUND.md` - Canonical semantics bounds (SB-1, SB-2)
- `EVIDENCE-INTERFACE.md` - Evidence specification
- `METABOLISM-IMPOSSIBILITY.md` - Why novelty is needed
