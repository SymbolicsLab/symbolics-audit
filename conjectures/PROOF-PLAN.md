# Proof Plan for Switch Bound Theorems

**Date**: 2026-01-29 (updated)
**Status**: Phase 3A.4 - Agda Formalization (SwitchBound.agda created, L12 proven)
**Related**: SWITCH-BOUND.md, OPERATIONS.md

---

## Foundation Lemmas (Lattice Algebra)

### L1: Truth Join Associativity
```agda
⊔ᵗ-assoc : ∀ a b c → (a ⊔ᵗ b) ⊔ᵗ c ≡ a ⊔ᵗ (b ⊔ᵗ c)
```
**Status**: ✓ PROVEN
**Location**: `Mechanics/CutOps.agda:229-231`

### L2: Truth Join Commutativity
```agda
⊔ᵗ-comm : ∀ a b → a ⊔ᵗ b ≡ b ⊔ᵗ a
```
**Status**: ✓ PROVEN
**Location**: `Mechanics/CutOps.agda:218-220`

### L3: Truth Join Idempotence
```agda
⊔ᵗ-idem : ∀ a → a ⊔ᵗ a ≡ a
```
**Status**: ✓ PROVEN
**Location**: `Mechanics/CutOps.agda:224-225`

### L4: Neither is Truth Join Identity
```agda
⊔ᵗ-identityˡ : ∀ t → Neither ⊔ᵗ t ≡ t
⊔ᵗ-identityʳ : ∀ t → t ⊔ᵗ Neither ≡ t
```
**Status**: ✓ PROVEN
**Location**: `Mechanics/CutOps.agda:241-245`

### L5: Side Join Associativity
```agda
⊔ˢ-assoc : ∀ s1 s2 s3 → (s1 ⊔ˢ s2) ⊔ˢ s3 ≡ s1 ⊔ˢ (s2 ⊔ˢ s3)
```
**Status**: ✓ PROVEN
**Location**: `Mechanics/CutOps.agda:327-329`

### L6: Cut Join Idempotence
```agda
⊔ᶜ-idem : {U : Set} (c : Cut U) → (c ⊔ᶜ c) ≈ c
```
**Status**: ✓ PROVEN
**Location**: `Mechanics/CutOps.agda:456-457`

---

## Core Lemmas (Aggregate Preservation)

### L7: Empty Aggregate Identity
```agda
empty-agg-identity : joinAllRes [] ≡ mkSide Neither Res
```
**Status**: ✓ PROVEN
**Location**: `Mechanics/Context.agda:122-123`

### L8: Aggregate Idempotence (Lemma 2)
```
∀ u C → Agg(Agg(C) :: C)(u) ≡ Agg(C)(u)
```
**Status**: ⚠ VERIFIED EXHAUSTIVELY (TypeScript), TO PROVE in Agda

**Proof sketch**:
1. `Agg(Agg(C) :: C)(u) = Agg(C)(u) ⊔ˢ Agg(C)(u)` by definition
2. `= Agg(C)(u)` by L6 (Side join idempotence)

**Agda stub**:
```agda
agg-idem : {U : Set} (ctx : Context U) (u : U)
         → apply (aggregate Resolution (add (aggregate Resolution ctx) ctx)) u
           ≡ apply (aggregate Resolution ctx) u
agg-idem ctx u = ?  -- Use ⊔ˢ-idem
```

### L9: Unfold Preserves Truth (Lemma 3)
```
∀ u C → truthOf(Agg(unfold :: C)(u)) ≡ truthOf(Agg(C)(u))
```
**Status**: ⚠ VERIFIED EXHAUSTIVELY (TypeScript), TO PROVE in Agda

**Proof sketch**:
1. `unfold = trivial-Rem` which applies `sideRem = mkSide Neither Unres` at all u
2. `truth sideRem = Neither` (the identity for truth join)
3. `Agg(unfold :: C)(u) = sideRem ⊔ˢ Agg(C)(u)`
4. `truth (sideRem ⊔ˢ s) = Neither ⊔ᵗ truth s = truth s` by L4

**Agda stub**:
```agda
unfold-preserves-truth : {U : Set} (ctx : Context U) (u : U)
                       → truth (apply (aggregate Resolution (add trivial-Rem ctx)) u)
                         ≡ truth (apply (aggregate Resolution ctx) u)
unfold-preserves-truth ctx u = ?  -- Use ⊔ᵗ-identityˡ
```

### L10: Decay Preserves Aggregate (Lemma 1)
```
∀ u C → Agg(decay_absorb(C))(u) ≡ Agg(C)(u)
```
**Status**: ⚠ VERIFIED EXHAUSTIVELY (TypeScript), TO PROVE in Agda

**Note**: This requires proving that absorption-based subsumption only removes
cuts whose contribution is already present in the aggregate.

**Agda approach**: Prove that for any cut d absorbed by aggregate agg:
`d ⊔ᶜ agg ≈ agg`, so removing d doesn't change the aggregate.

---

## Conflict Lemmas

### L11: Conflict Creation Requires Both
```agda
conflict-join : In ⊔ᵗ Out ≡ Both
```
**Status**: ✓ PROVEN
**Location**: `Mechanics/CutOps.agda:268`

### L12: Neither Cannot Create Conflict
```
∀ t → isBoth(Neither ⊔ᵗ t) → isBoth(t)
```
**Status**: ✓ PROVEN
**Location**: `Mechanics/SwitchBound.agda:73-74`

**Proof**: Follows from L4 (`Neither ⊔ᵗ t = t`).
```agda
Neither-cannot-create-conflict : ∀ t → isBoth (Neither ⊔ᵗ t) ≡ true → isBoth t ≡ true
Neither-cannot-create-conflict t p = trans (cong isBoth (sym (⊔ᵗ-identityˡ t))) p
```

---

## Invariant Theorem

### T1: truthOf(Agg) is Invariant Under Canonical Operations
```
∀ C C' → C →canonicalStep C' → truthOf(Agg(C))(u) ≡ truthOf(Agg(C'))(u)
```
**Status**: ⚠ TO PROVE (requires defining canonical step)

**Proof sketch**: Case split on step type:
- DoStabilize: uses L8 (aggregate idempotence)
- DoExplore: uses L9 (unfold preserves truth)
- DoDecay (absorb): uses L10 (decay preserves aggregate)

---

## Main Theorems

### SB-1: Canonical System Switches = 0
```
∀ τ → switches(τ) = 0
```
**Status**: ⚠ TO PROVE (requires T1 and switch count definition)

**Proof**:
1. By T1, `truthOf(Agg)` is invariant
2. `conflictOn = isBoth(truthOf(Agg(u)))` for some u
3. Invariant truth → invariant conflictOn
4. Invariant boolean has 0 switches ∎

### SB-2: Drop-Conflict System Switches ≤ 1
```
∀ τ → switches(τ) ≤ 1
```
**Status**: ⚠ TO PROVE (requires additional machinery)

**Proof sketch**:
1. `decay_dropConflict` can only decrease conflict (Both → not Both)
2. By L8-L10, no canonical operation can increase conflict
3. Conflict is monotonically non-increasing
4. Boolean monotone sequence has ≤ 1 switch ∎

---

## Summary

| ID | Lemma | Status | Priority |
|----|-------|--------|----------|
| L1-L6 | Lattice algebra | ✓ PROVEN | — |
| L7 | Empty aggregate | ✓ PROVEN | — |
| L8 | Aggregate idempotence | VERIFIED, TO PROVE | HIGH |
| L9 | Unfold preserves truth | VERIFIED, TO PROVE | HIGH |
| L10 | Decay preserves aggregate | VERIFIED, TO PROVE | MEDIUM |
| L11 | Conflict creation | ✓ PROVEN | — |
| L12 | Neither can't create conflict | ✓ PROVEN | — |
| T1 | Truth invariant | TO PROVE | HIGH |
| SB-1 | Canonical switches = 0 | TO PROVE | GOAL |
| SB-2 | Drop-conflict switches ≤ 1 | TO PROVE | GOAL |

---

## Next Steps

1. ~~**Create SwitchBound.agda**: Start with L8, L9, L12~~ ✓ DONE (2026-01-29)
2. **Prove L8**: Aggregate idempotence in Agda
3. **Prove L9**: Unfold preserves truth in Agda
4. **Define canonical step**: Formalize the step relation
3. **Prove T1**: Truth invariant theorem
4. **Define switchCount**: Formalize the switch counting function
5. **Prove SB-1**: Main canonical system theorem

---

## See Also

- `Mechanics/CutOps.agda` - Proven lattice lemmas
- `Mechanics/Context.agda` - Aggregate and context definitions
- `SWITCH-BOUND.md` - Theorem statements
- `OPERATIONS.md` - Operation semantics
