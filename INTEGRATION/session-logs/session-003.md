# Session 3 Log — FDE-Fold Conservativity Proof

**Date**: 2026-02-01
**Duration**: ~1.5 hours
**Agent**: Claude Code
**Focus**: Proving conservativity for FDE World-Indexed fold

---

## Objectives (from state.yaml next_actions)

1. ✅ Complete FDE-fold property proofs (conservativity)
2. ⚠️ Prove contradiction-preservation (structure developed, needs completion)
3. ⚠️ Prove idempotence (statement only)

---

## Main Achievement: Conservativity Proven

**Theorem**: `fold-conservative : ∀ {w} (Φ : Config w) → support (fold Φ) ⊆-list support Φ`

This proves that fold never introduces new atoms — all atoms in the output were present in the input.

---

## Files Created/Modified

### New: FDE/WorldIndexed/Properties.agda (~200 lines)

**Key definitions:**
- `InBucket` — Data type for tracking atom presence in bucket
- `fromBucket-pos-inv` — If a ∈ posAtoms (fromBucket bs), then InBucket a bs
- `fromBucket-neg-inv` — Same for negAtoms
- `inBucket-insert-same` — insertBucket puts the atom in the bucket
- `inBucket-insert-inv` — Inverse: if a ∈ insertBucket b v bs and a ≢ b, then a ∈ bs
- `inBucket-insertPos` — Membership tracking through insertPos
- `inBucket-insertNeg` — Membership tracking through insertNeg
- `inBucket-toBucket` — If a ∈ toBucket Φ, then a ∈ support Φ
- `fold-pos-from-support` — If a ∈ posAtoms (fold Φ), then a ∈ support Φ
- `fold-neg-from-support` — If a ∈ negAtoms (fold Φ), then a ∈ support Φ
- **`fold-conservative`** — The main theorem

**Auxiliary:**
- `_⊎_` — Sum type for disjunctive results
- `∈-++ˡ`, `∈-++ʳ`, `∈-++-split` — Concatenation membership lemmas

### Modified: FDE/WorldIndexed/All.agda

- Added Properties.agda exports
- Updated summary comments to reflect conservativity is now PROVEN

---

## Proof Strategy

The conservativity proof follows this structure:

1. **Track membership through fromBucket**: If an atom appears in `posAtoms (fromBucket bs)`, we can show it was in the bucket (via `fromBucket-pos-inv`).

2. **Track membership through insert operations**: The lemmas `inBucket-insert-same` and `inBucket-insert-inv` establish that insert either adds the specific atom or preserves existing atoms.

3. **Track membership through insertPos/insertNeg**: Building on the insert lemmas, we show that atoms in `insertPos as bs` came from either `as` or `bs` (similarly for `insertNeg`).

4. **Combine via inBucket-toBucket**: For `toBucket Φ = insertPos (posAtoms Φ) (insertNeg (negAtoms Φ) [])`, any atom in the result came from either `posAtoms Φ` or `negAtoms Φ`.

5. **Final proof**: `fold-conservative` uses the above to show that every atom in `support (fold Φ)` was in `support Φ`.

---

## Property Status Summary

| Property | Status | Notes |
|----------|--------|-------|
| Conservativity | ✅ PROVEN | `fold-conservative` in Properties.agda |
| Idempotence | ⚠️ Statement only | Needs bucket stability: `toBucket ∘ fromBucket = id` on normalized |
| Contradiction-preservation | ⚠️ Structure developed | Needs `lookup-insert-eq` tracking through reconstruction |

---

## What's Needed for Remaining Proofs

### Idempotence

The key insight: `fold (fold Φ) ≈ fold Φ` because `toBucket` produces normalized buckets (sorted, non-N), and `fromBucket ∘ toBucket` is the identity on normalized buckets.

Needs:
1. Proof that `toBucket` produces `Normalized` buckets
2. Proof that `fromBucket ∘ toBucket = id` on `Normalized` buckets
3. Bridge to `≈` equivalence

### Contradiction-preservation

If `a ∈ posAtoms Φ` and `a ∈ negAtoms Φ`, then in `toBucket Φ` the atom `a` gets value `B` (via merge of `T` and `F`), and `fromBucket` with value `B` puts `a` in both lists.

Needs:
1. `lookupBucket-insertPos-T`: If a ∈ ps, then lookupBucket a (insertPos ps bs) has T or B
2. `lookupBucket-insertNeg-F`: If a ∈ ns, then lookupBucket a (insertNeg ns bs) has F or B
3. `fromBucket-B-pos/neg`: If lookupBucket a bs = B, then a ∈ posAtoms/negAtoms (fromBucket bs)

The lemma `lookup-insert-eq` in Fold.agda is a key building block.

---

## Compilation Status

All modules compile with `--safe --without-K`:
```bash
agda --safe --without-K FDE/WorldIndexed/All.agda
# ✓ Checking FDE.WorldIndexed.All
```

---

## Code Statistics

- **New lines**: ~200 (Properties.agda)
- **Total FDE/WorldIndexed**: ~750 lines across 5 files
- **Compilation time**: ~10 seconds

---

## Reflection

Session 3 achieved one of the three target proofs (conservativity). The proof structure is clean and follows naturally from tracking membership through the bucket operations.

The remaining proofs (idempotence and contradiction-preservation) are more involved because they require:
- For idempotence: proving bucket stability (that normalized buckets are fixed points)
- For contradiction-preservation: tracking FOUR values through the bucket operations

Both are structurally similar to the existing LP proofs but require adaptation for the parametric Atom type and the Setoid equivalence.

---

## Next Session Suggestions

1. **Contradiction-preservation first**: This is closer to complete — the `lookup-insert-eq` lemma exists, and the main structure is sketched.

2. **Idempotence later**: This requires more infrastructure (proving `Normalized` is preserved by `toBucket`).

3. **Alternative**: Add comprehensive test cases to validate the existing implementation before completing the proofs.

---

**Ready for next task as user directs.**
