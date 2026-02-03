# Session 4 Log — FDE-Fold Contradiction-Preservation Proof

**Date**: 2026-02-01
**Duration**: ~45 minutes
**Agent**: Claude Code
**Focus**: Proving contradiction-preservation for FDE World-Indexed fold

---

## Objectives (from state.yaml next_actions)

1. Complete FDE-fold contradiction-preservation proof
2. ⚠️ Complete idempotence proof (deferred — requires bucket stability lemmas)

---

## Main Achievement: Contradiction-Preservation Proven

**Theorem**: `fold-contradiction : ∀ {w} (a : Atom w) (Φ : Config w) → a ∈ posAtoms Φ → a ∈ negAtoms Φ → (a ∈ posAtoms (fold Φ)) ×' (a ∈ negAtoms (fold Φ))`

This proves that fold preserves contradictions — if an atom appears in both the positive and negative lists of a configuration, it will appear in both lists of the folded configuration.

---

## Files Modified

### FDE/WorldIndexed/Properties.agda (~350 lines total, +150 new)

**Key new definitions:**

1. **<Fin-trans** — Transitivity for the strict ordering on Fin
   ```agda
   <Fin-trans : ∀ {n} {x y z : Fin n} → x <Fin y → y <Fin z → x <Fin z
   ```

2. **lookup-insert-neq** — Insert doesn't affect lookup for different atoms
   ```agda
   lookup-insert-neq : ∀ {w} (a b : Atom w) (v : FOUR) (bucket : Bucket w)
                     → (a ≡ b → ⊥)
                     → lookupBucket a (insertBucket b v bucket) ≡ lookupBucket a bucket
   ```
   This required careful case analysis on `compareFin b c`, `compareFin a b`, and `compareFin a c` with transitivity to rule out impossible orderings.

3. **lookupBucket-insertNeg-hasF** — After inserting negAtoms, the atom has F or B
   ```agda
   lookupBucket-insertNeg-hasF : ∀ {w} (a : Atom w) (ns : List (Atom w))
                               → a ∈ ns
                               → (lookupBucket a (insertNeg ns []) ≡ F)
                               ⊎ (lookupBucket a (insertNeg ns []) ≡ B)
   ```

4. **insertPos-preserves-F** — F stays F or upgrades to B through insertPos
   ```agda
   insertPos-preserves-F : ∀ {w} (a : Atom w) (ps : List (Atom w)) (bs : Bucket w)
                         → lookupBucket a bs ≡ F
                         → (lookupBucket a (insertPos ps bs) ≡ F)
                         ⊎ (lookupBucket a (insertPos ps bs) ≡ B)
   ```

5. **insertPos-preserves-B** — B stays B through insertPos
   ```agda
   insertPos-preserves-B : ∀ {w} (a : Atom w) (ps : List (Atom w)) (bs : Bucket w)
                         → lookupBucket a bs ≡ B
                         → lookupBucket a (insertPos ps bs) ≡ B
   ```

6. **lookupBucket-insertPos-getsB** — If bucket has F/B and we insert T (a ∈ ps), result is B
   ```agda
   lookupBucket-insertPos-getsB : ∀ {w} (a : Atom w) (ps : List (Atom w)) (bs : Bucket w)
                                → a ∈ ps
                                → (lookupBucket a bs ≡ F) ⊎ (lookupBucket a bs ≡ B)
                                → lookupBucket a (insertPos ps bs) ≡ B
   ```

7. **fromBucket-B-pos / fromBucket-B-neg** — If bucket has B for an atom, it appears in both polarity lists
   ```agda
   fromBucket-B-pos : ∀ {w} (a : Atom w) (bs : Bucket w)
                    → lookupBucket a bs ≡ B
                    → a ∈ posAtoms (fromBucket bs)
   fromBucket-B-neg : ∀ {w} (a : Atom w) (bs : Bucket w)
                    → lookupBucket a bs ≡ B
                    → a ∈ negAtoms (fromBucket bs)
   ```

8. **fold-contradiction** — The main theorem

### FDE/WorldIndexed/All.agda

- Added exports for new lemmas
- Updated summary to reflect contradiction-preservation is now PROVEN

---

## Proof Strategy

The contradiction-preservation proof follows this chain:

1. **Track through insertNeg**: If `a ∈ negAtoms Φ`, then `lookupBucket a (insertNeg (negAtoms Φ) [])` is `F` or `B`

2. **Track through insertPos with F/B preservation**: The key insight is that inserting `T` for atoms doesn't destroy the `F`-ness from the negative atoms. If the bucket has `F`, it either stays `F` (if `a ∉ ps`) or becomes `B` (if `a ∈ ps` and we merge `F` with `T`).

3. **Combine to get B**: If `a ∈ posAtoms Φ` and the bucket from step 1 has `F` or `B` for `a`, then after `insertPos (posAtoms Φ)`, the bucket has `B` for `a`.

4. **Extract from B**: The lemmas `fromBucket-B-pos` and `fromBucket-B-neg` show that if `lookupBucket a bucket = B`, then `a` appears in both `posAtoms (fromBucket bucket)` and `negAtoms (fromBucket bucket)`.

---

## Technical Challenges

### 1. lookup-insert-neq Case Analysis

The `lookup-insert-neq` lemma required careful handling of the trichotomy orderings. When we split on `compareFin b c` (how b inserts) and `compareFin a b` (where a is relative to b), some combinations like `a < b < c` with `a > c` are impossible. We use `<Fin-trans` and `<Fin-asym` to derive contradictions for these cases.

### 2. Pattern Naming Conflicts

The variable name `eq` conflicts with the `eq` constructor of `Tri`. All proof term variables were renamed to `prf` to avoid this.

### 3. F-Preservation Through insertPos

The key insight was that we need two separate lemmas:
- `insertPos-preserves-F`: If bucket has F for a, insertPos gives F or B
- `insertPos-preserves-B`: If bucket has B for a, insertPos keeps B

These let us show that the F from insertNeg persists (possibly upgraded to B) through insertPos.

---

## Property Status Summary

| Property | Status | Notes |
|----------|--------|-------|
| Conservativity | PROVEN | Session 3 |
| Contradiction-preservation | PROVEN | Session 4 |
| Idempotence | Statement only | Needs bucket stability: toBucket produces Normalized, fromBucket∘toBucket stable |

---

## Compilation Status

All modules compile with `--safe --without-K`:
```bash
agda --safe --without-K FDE/WorldIndexed/All.agda
# Checking FDE.WorldIndexed.All
```

---

## Code Statistics

- **New lines**: ~150 (Properties.agda additions)
- **Total FDE/WorldIndexed**: ~900 lines across 5 files
- **Compilation time**: ~12 seconds

---

## Reflection

Session 4 achieved the second of three target proofs. The contradiction-preservation proof required more infrastructure than conservativity because we needed to track FOUR values through the bucket operations, not just membership.

The remaining proof (idempotence) is structurally different — it requires showing that `toBucket` produces normalized buckets and that `fromBucket ∘ toBucket` is stable on normalized buckets. This is more about bucket invariants than value tracking.

---

## Next Session Suggestions

1. **Idempotence**: Prove `fold (fold Φ) ≈ fold Φ` via bucket stability
   - Show `toBucket` produces `Sorted` buckets
   - Show `toBucket` produces `AllNonN` buckets
   - Show `fromBucket ∘ toBucket = id` on `Normalized` buckets

2. **Alternative**: Move on to unfold specification now that 2/3 properties are proven

3. **Documentation**: Update completeness-map.md with new proofs

---

**Ready for next task as user directs.**
