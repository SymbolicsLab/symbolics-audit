# Session 2 Log — FDE-Fold World-Indexed Implementation

**Date**: 2026-02-02
**Duration**: ~2 hours
**Agent**: Claude Code
**Focus**: Agda implementation of FDE-fold with world-indexed types

---

## Objectives (from session-002-prep.md)

1. ✅ Define FDE values: `data FOUR = Neither | In | Out | Both`
2. ✅ Define Config as world-indexed: `Config w = (pos : List (Atom w), neg : List (Atom w))`
3. ✅ Define FDE consequence relation
4. ✅ Build Setoid on configurations (equivalence, not equality)
5. ✅ Define fold via bucket normalization
6. ⚠️ Re-prove properties for Setoid (statements defined, full proofs pending)

---

## Files Created

### FDE/WorldIndexed/Base.agda
- **World**: `World = ℕ` (tracks accumulated cuts)
- **Atom**: `Atom w = Fin w` (world-indexed propositional handles)
- **cutW**: `cutW = suc` (domain extension)
- **embed**: `Atom w → Atom (cutW w)` (old atoms persist)
- **fresh**: `Atom (cutW w)` (new atom from cut)
- **FOUR**: `data FOUR = N | T | F | B` (Belnap four values)
- **merge**: Information lattice join operation
- **Config**: `record { posAtoms : List (Atom w); negAtoms : List (Atom w) }`
- **lookup**: `Atom w → Config w → FOUR`

### FDE/WorldIndexed/Consequence.agda
- **⊤, ⊥**: Unit and empty types
- **designated**: `FOUR → Set` (T and B are designated)
- **≤ₖ**: Information ordering on FOUR
- **⊆-list**: Subset relation on atom lists
- **_⊧_**: FDE consequence on configs (mutual subset)
- **_≈_**: FDE equivalence (mutual consequence)
- **Setoid**: Generic setoid structure
- **ConfigSetoid**: Setoid for Config w with ≈ equivalence

### FDE/WorldIndexed/Fold.agda
- **<Fin**: Strict ordering on Fin
- **Tri**: Trichotomy type for comparisons
- **compareFin**: Decidable trichotomy
- **Bucket**: Sorted list of (Atom, FOUR) pairs
- **insertBucket**: Insert maintaining sorted order
- **toBucket**: Config → Bucket (normalization)
- **fromBucket**: Bucket → Config (reconstruction)
- **fold**: Config → Config (`fromBucket ∘ toBucket`)
- **lookupBucket**: Lookup value in bucket
- **Normalized**: Predicate for sorted, non-N buckets
- **Property statements**: idempotence, conservativity, contradiction-preservation

### FDE/WorldIndexed/All.agda
- Public entry point re-exporting all components

---

## What Compiles

All four modules compile with `--safe --without-K`:
```bash
agda --safe --without-K FDE/WorldIndexed/All.agda
# ✓ Checking FDE.WorldIndexed.All
```

---

## Property Status

### Idempotence: `fold (fold Φ) ≈ fold Φ`
- **Statement**: Defined as `fold-idempotent-statement`
- **Proof**: Requires bucket stability lemmas (structure defined, proof pending)
- **Key insight**: Same approach as LP fold — `toBucket ∘ fromBucket = id` on normalized buckets

### Conservativity: `support (fold Φ) ⊆ support Φ`
- **Statement**: Defined as `fold-conservative-statement`
- **Proof**: Follows from fold only reorganizing existing atoms
- **Structure**: Ready for proof via membership tracking

### Contradiction-preservation: `+a,-a ∈ Φ → +a,-a ∈ fold Φ`
- **Statement**: Defined as `fold-contradiction-statement`
- **Proof**: Follows from merge operation (T ⊔ F = B)
- **Key lemma**: `lookup-insert-eq` proven

---

## Architectural Observations

### What Works
1. **World-indexing**: `Atom n = Fin n` is a clean, simple implementation
2. **Bucket approach**: Extends naturally from the LP implementation
3. **Setoid structure**: Cleanly separates "same content" from "same representation"
4. **Modular design**: Base/Consequence/Fold separation allows incremental development

### Where It Could Break (per session-002-prep.md goals)
1. **World-indexing**: No problems encountered. Fin n works perfectly.
2. **--without-K**: Setoid approach handles this cleanly. No quotient issues.
3. **Conservativity meaning**: With Option A (implicit Neither), conservativity means "atoms in support don't increase"

### Relation to ADR-001/ADR-002
- **Option A implemented**: Config as pair of lists, Neither implicit
- **Setoid implemented**: Equivalence relation, not canonical representatives
- **Level 2+ only**: This formalizes stabilization over distinguished atoms, not distinction itself
- **Central open question unchanged**: What is `Opaque : World → Set`?

---

## What's Next

### Immediate (can do now)
1. Complete the idempotence proof (bucket stability lemma)
2. Prove conservativity and contradiction-preservation
3. Add more comprehensive tests

### Future (per ADR-001 migration path)
1. **Phase 2**: Migrate to Option A′ (explicit Domain component)
2. **Phase 3**: Investigate dialogical extension if needed

### Deferred (per session-002-prep.md)
- What is Opaque?
- How does remainder formalize?
- What does unfold do?
- How does this connect to DSL?

---

## Success Criteria Assessment

From session-002-prep.md:

| Criterion | Status |
|-----------|--------|
| Compiling Agda code for FDE values and configurations | ✅ Complete |
| At least one fold property re-proven for Setoid | ⚠️ Statement defined, proof structure ready |
| Identified where design breaks (if anywhere) | ✅ No breaks found |
| NOT spent time on more theory | ✅ Pure implementation session |

---

## Code Statistics

- **Lines of Agda**: ~550 total across 4 files
- **Compilation time**: ~5 seconds
- **No postulates**: All code is `--safe`
- **No K axiom**: All code is `--without-K`

---

## Reflection

Session 2 achieved its primary goal: the FDE-fold architecture for world-indexed types is established and compiles. The property proofs are partially complete (statements + some lemmas), with the full proofs being structurally similar to the existing LP proofs.

The world-indexed approach is working well. The `Fin n` implementation for atoms is simple and sufficient for current needs. The Setoid approach cleanly avoids quotient issues.

The central open question from Session 1 remains unchanged: What is `Opaque : World → Set`? The FDE-fold work operates on the "output side" (Config) while Opaque is the "input side." This formalization confirms that the output side is tractable; the hard theoretical work is on the input side.

---

**Ready for property proof completion or new direction as user requests.**
