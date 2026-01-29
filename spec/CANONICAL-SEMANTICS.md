# Canonical Semantics Fragment (Phase 2)

**Status**: Authoritative specification for TypeScript implementation
**Date**: 2026-01-29
**Sources**: Mechanics.Primitive, Mechanics.CutOps, Mechanics.Context, Mechanics.Finite, Mechanics.Dynamics

This document defines the precise semantics for the finite domain fragment.
The TypeScript runtime MUST implement exactly this.

---

## 1. Domain

```
U is finite: represented as a list of distinct elements (strings in TS)
|U| ≤ 1000 (practical bound for testing)
```

In TypeScript: `elements: string[]`

---

## 2. Truth (Belnap Four-Valued)

From `Mechanics.Primitive`:

```agda
record Truth : Set where
  constructor mkTruth
  field
    supportsIn  : Bool  -- evidence for inclusion
    supportsOut : Bool  -- evidence for exclusion

pattern Neither = mkTruth false false  -- no information (bottom)
pattern In      = mkTruth true  false  -- included / positive
pattern Out     = mkTruth false true   -- excluded / negative
pattern Both    = mkTruth true  true   -- contradiction (top)
```

### Truth Lattice (Knowledge Order)

```
        Both (top)
       /    \
     In      Out   (incomparable)
       \    /
      Neither (bottom)
```

### Truth Operations (from CutOps.agda)

**Join (⊔ᵗ)**: Bitwise OR
```agda
_⊔ᵗ_ : Truth → Truth → Truth
t1 ⊔ᵗ t2 = mkTruth (supportsIn t1 ∨ supportsIn t2) (supportsOut t1 ∨ supportsOut t2)
```

**Meet (⊓ᵗ)**: Bitwise AND
```agda
_⊓ᵗ_ : Truth → Truth → Truth
t1 ⊓ᵗ t2 = mkTruth (supportsIn t1 ∧ supportsIn t2) (supportsOut t1 ∧ supportsOut t2)
```

**Key Properties (VERIFIED)**:
- `Neither ⊔ᵗ t = t` (Neither is identity for join)
- `Both ⊔ᵗ t = Both` (Both is absorbing for join)
- `In ⊔ᵗ Out = Both` (conflict preserved, not collapsed)
- Join is associative, commutative, idempotent

---

## 3. Resolved

From `Mechanics.Primitive`:

```agda
data Resolved : Set where
  Res   : Resolved  -- settled / no pressure
  Unres : Resolved  -- pressured / has remainder
```

### Resolved Operations (from CutOps.agda)

**Join (⊔ᵘ)**: Unres dominates (pressure is sticky)
```agda
_⊔ᵘ_ : Resolved → Resolved → Resolved
Res   ⊔ᵘ Res   = Res
Res   ⊔ᵘ Unres = Unres
Unres ⊔ᵘ _     = Unres
```

**Meet (⊓ᵘ)**: Res dominates
```agda
_⊓ᵘ_ : Resolved → Resolved → Resolved
Res   ⊓ᵘ _     = Res
Unres ⊓ᵘ Res   = Res
Unres ⊓ᵘ Unres = Unres
```

---

## 4. Side = Truth × Resolved

From `Mechanics.Primitive`:

```agda
record Side : Set where
  constructor mkSide
  field
    truth    : Truth
    resolved : Resolved

pattern sideOut  = mkSide Out     Res
pattern sideIn   = mkSide In      Res
pattern sideBoth = mkSide Both    Res
pattern sideRem  = mkSide Neither Unres  -- CRITICAL: Neither, not Out!
```

### Side Operations (from CutOps.agda)

**Join (⊔ˢ)**: Component-wise
```agda
_⊔ˢ_ : Side → Side → Side
s1 ⊔ˢ s2 = mkSide (truth s1 ⊔ᵗ truth s2) (resolved s1 ⊔ᵘ resolved s2)
```

**Identity Element**: `mkSide Neither Res`
- Empty aggregation returns this value

---

## 5. Side Order (Resolution Order)

From `Mechanics.Finite`:

```agda
_≤ʳ?_ : Side → Side → Bool
sideOut ≤ʳ? _   = true                    -- Out is bottom
sideRem ≤ʳ? sideOut = false
sideRem ≤ʳ? sideRem = true
sideRem ≤ʳ? sideIn  = true
sideRem ≤ʳ? sideBoth = true
sideIn  ≤ʳ? sideOut = false
sideIn  ≤ʳ? sideRem = false
sideIn  ≤ʳ? sideIn  = true
sideIn  ≤ʳ? sideBoth = true
sideBoth ≤ʳ? sideBoth = true
sideBoth ≤ʳ? _ = false
_ ≤ʳ? _ = false
```

**Order Diagram**:
```
      sideBoth (top)
        /   \
    sideIn  sideRem
        \   /
       sideOut (bottom)
```

Note: This is NOT the same as the knowledge order! This is the "resolution order".

---

## 6. Cut

From `Mechanics.Primitive`:

```agda
record Cut {ℓ : Level} (U : Set ℓ) : Set ℓ where
  field
    apply : U → Side
```

In TypeScript for finite domains, represent as:
```typescript
type Cut = Map<string, Side>;  // or (element: string) => Side
```

---

## 7. Context

From `Mechanics.Context`:

```agda
Context : {ℓ : Level} (U : Set ℓ) → Set ℓ
Context U = List (Cut U)
```

In TypeScript:
```typescript
type Context = Cut[];
```

---

## 8. Aggregate

From `Mechanics.Context`:

```agda
-- Fold a list of Sides using Side join
joinAllRes : List Side → Side
joinAllRes []       = mkSide Neither Res  -- Identity element!
joinAllRes (s ∷ ss) = s ⊔ˢ joinAllRes ss

-- Aggregate: Combine all Cuts pointwise
aggregate : AggPolicy → Context U → Cut U
aggregate Resolution ctx = record {
  apply = λ u → joinAllRes (map (λ c → apply c u) ctx)
}
```

### TypeScript Implementation

```typescript
function aggregate(context: Cut[], elements: string[]): Cut {
  const result = new Map<string, Side>();
  for (const u of elements) {
    // Start with identity element
    let joined: Side = { truth: Neither, resolved: 'Res' };
    for (const cut of context) {
      joined = joinSide(joined, cut.get(u)!);
    }
    result.set(u, joined);
  }
  return result;
}
```

**Critical**: Empty context aggregates to `mkSide Neither Res` at every element.

---

## 9. Subsumption

From `Mechanics.Finite`:

A Cut `d` is **subsumed** by Cut `c` if:
```
∀ u ∈ elements, d(u) ≤ʳ c(u)
```

```agda
isSubsumed : FiniteSystem U → Cut U → Cut U → Bool
isSubsumed sys d c =
  let elemList = elements sys
      checks = map (λ u → apply d u ≤ʳ? apply c u) elemList
  in allTrue checks
```

### TypeScript Implementation

```typescript
function isSubsumed(d: Cut, c: Cut, elements: string[]): boolean {
  return elements.every(u => sideLeq(d.get(u)!, c.get(u)!));
}

function sideLeq(a: Side, b: Side): boolean {
  // Resolution order from Finite.agda
  if (sideEqual(a, sideOut)) return true;  // Out ≤ anything
  if (sideEqual(a, b)) return true;         // reflexivity
  if (sideEqual(a, sideRem)) {
    return sideEqual(b, sideIn) || sideEqual(b, sideRem) || sideEqual(b, sideBoth);
  }
  if (sideEqual(a, sideIn)) {
    return sideEqual(b, sideIn) || sideEqual(b, sideBoth);
  }
  if (sideEqual(a, sideBoth)) {
    return sideEqual(b, sideBoth);
  }
  return false;
}
```

---

## 10. Update (Decay)

### IMPORTANT: Two Different Definitions Exist!

**Context.agda Definition** (removes cuts subsumed by AGGREGATE):
```agda
update : Context U → Cut U → Context U
update ctx c =
  let ctx' = add c ctx
      agg = aggregate Resolution ctx'
  in removeSubsumed agg ctx'
```

**Finite.agda Definition** (removes cuts subsumed by NEW CUT):
```agda
updateFinite : FiniteSystem U → Context U → Cut U → Context U
updateFinite sys ctx c =
  c ∷ removeSubsumedBy sys c ctx
```

### DESIGN DECISION REQUIRED

These are **different semantics**:
- Context.agda: Subsumed by aggregate = more aggressive pruning
- Finite.agda: Subsumed by new cut only = more conservative

**Recommendation**: Use the Finite.agda definition for TypeScript because:
1. It has an actual implementation (not placeholder)
2. It's more predictable (new cut is known)
3. Aggregate-based pruning could remove the new cut itself

### TypeScript Implementation (Finite.agda semantics)

```typescript
function update(context: Cut[], newCut: Cut, elements: string[]): Cut[] {
  // Keep only cuts NOT subsumed by the new cut
  const surviving = context.filter(c => !isSubsumed(c, newCut, elements));
  // Add new cut at front
  return [newCut, ...surviving];
}
```

---

## 11. Aggregate Fold (for DSL)

The "aggregate" fold operation replaces the context with a single cut
containing the aggregate of all cuts:

```typescript
function applyAggregateFold(context: Cut[], elements: string[]): Cut[] {
  const agg = aggregate(context, elements);
  return [agg];
}
```

This is what the DSL's "aggregate" fold should do.

---

## 12. Unfold (Deferred)

The "unfold" operation is not fully specified in Agda.

From the existing TypeScript placeholder:
```typescript
case 'unfold':
  return uniformCut(sideRem);
```

This adds `sideRem` (Neither/Unres) at every element, creating pressure.

**TODO**: Document the intended Agda semantics when available.

---

## 13. Invariants

### Aggregate Invariants (VERIFIED in Agda)
- Aggregate of empty context = identity cut (Neither/Res everywhere)
- Aggregate is idempotent: Agg([Agg(C)]) = Agg(C)
- Join is associative, commutative, idempotent

### Subsumption Invariants
- Reflexive: c ⊑ c
- Transitive: if a ⊑ b and b ⊑ c then a ⊑ c
- Anti-symmetric: if a ⊑ b and b ⊑ a then a = b (extensionally)

### Update Invariants
- Update never increases context size unboundedly (subsumed cuts removed)
- New cut is always present after update

---

## 14. Test Cases

### Aggregate Tests
```typescript
// Empty context
aggregate([], ['A', 'B']) === { A: Neither/Res, B: Neither/Res }

// Single cut
aggregate([{ A: In/Res, B: Out/Res }], ['A', 'B']) === { A: In/Res, B: Out/Res }

// Conflict creation
aggregate([{ A: In/Res }, { A: Out/Res }], ['A']) === { A: Both/Res }

// Pressure preservation
aggregate([{ A: In/Res }, { A: Neither/Unres }], ['A']) === { A: In/Unres }
```

### Subsumption Tests
```typescript
// Out is bottom
isSubsumed({ A: Out/Res }, { A: In/Res }, ['A']) === true

// Reflexivity
isSubsumed({ A: In/Res }, { A: In/Res }, ['A']) === true

// Non-subsumption
isSubsumed({ A: In/Res }, { A: Out/Res }, ['A']) === false
```

### Update Tests
```typescript
// Subsumed cut removed
update([{ A: Out/Res }], { A: In/Res }, ['A']) === [{ A: In/Res }]

// Non-subsumed cut kept
update([{ A: In/Res }], { A: Out/Res }, ['A']) === [{ A: Out/Res }, { A: In/Res }]
```

---

## 15. Open Questions

1. **Aggregate vs new-cut subsumption**: Which is canonical? (See Section 10)
2. **Unfold semantics**: What should unfold actually do? (See Section 12)
3. **Canonicalization**: Should contexts be sorted/deduped?
4. **Edge cases**: Empty domain, single element, all-Both initialization

---

## Appendix: Source File References

| Concept | File | Line |
|---------|------|------|
| Truth type | Mechanics/Primitive.agda | 66-78 |
| Side type | Mechanics/Primitive.agda | 189-195 |
| Side join | Mechanics/CutOps.agda | 187-190 |
| Side order | Mechanics/Finite.agda | 188-201 |
| Aggregate | Mechanics/Context.agda | 116-138 |
| Subsumption | Mechanics/Finite.agda | 203-215 |
| Update (Context) | Mechanics/Context.agda | 190-194 |
| Update (Finite) | Mechanics/Finite.agda | 236-239 |
