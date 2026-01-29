# Operation Semantics (Precise)

**Date**: 2026-01-29
**Related**: SWITCH-BOUND.md, DEFINITIONS.md

This document precisely defines what each operation does to the context and aggregate.

---

## Fold Operations

### aggregate (Stabilize default)

**Implementation** (`fold-expr.ts:197-201`):
```typescript
case 'aggregate':
  return aggregateCut(state.context);
```

**Semantics**: Returns the pointwise join of all cuts in context.

**Properties**:
- `Agg([aggregateCut(C), ...C]) = Agg(C)` (idempotent via join idempotence)
- Does NOT change `truthOf(Agg(C))` (truth values preserved)
- Does NOT change `resolvedOf(Agg(C))` (resolved values preserved)

**Consequence**: Adding aggregate cut cannot change conflictOn.

### unfold (Explore default)

**Implementation** (`fold-expr.ts:209-212`):
```typescript
case 'unfold':
  return uniformCut(sideRem);  // sideRem = Neither/Unres
```

**Semantics**: Returns a cut with Neither/Unres at every element.

**Properties**:
- `truthOf(Agg([sideRem, ...C])) = truthOf(Agg(C))` ✓
  - Because: Neither is identity for truth join
  - `In ⊔ᵗ Neither = In`, `Out ⊔ᵗ Neither = Out`, `Both ⊔ᵗ Neither = Both`
- `resolvedOf(Agg([sideRem, ...C])) ≠ resolvedOf(Agg(C))` possibly
  - Because: Unres dominates in resolved join
  - `Res ⊔ᵘ Unres = Unres`

**Consequence**:
- unfold cannot change conflictOn (truth-dependent)
- unfold CAN change pressureCount (resolved-dependent)

### identity

**Implementation** (`fold-expr.ts:193-195`):
```typescript
case 'identity':
  return uniformCut(sideNeither);  // sideNeither = Neither/Res
```

**Semantics**: Returns a cut with Neither/Res at every element.

**Properties**:
- `Agg([sideNeither, ...C]) = Agg(C)` (complete identity)
- Neither/Res is the identity element for Side join

**Consequence**: Adding identity cut changes nothing.

---

## Decay Mechanisms

### decay_absorb (Canonical Subsumption)

**Implementation** (`context.ts:149-158`):
```typescript
export function updateContext(ctx, newCut, domainSize): Context {
  const surviving = ctx.filter(cut => !isSubsumed(cut, newCut, domainSize));
  return [newCut, ...surviving];
}
```

Where `isSubsumed` uses absorption order (`context.ts:114-121`):
```typescript
export function isSubsumed(d, c, domainSize): boolean {
  for (let i = 0; i < domainSize; i++) {
    if (!sideAbsorbedBy(d(i), c(i))) return false;
  }
  return true;
}
```

**Semantics**: Add new cut, remove cuts absorbed by it.

**Property**: `Agg(updateContext(C, newCut)) = Agg([newCut, ...C])`
- Verified exhaustively: 100% pass (15625 tests)
- Because: If `d` absorbed by `newCut`, then `join(d, newCut) = newCut`
- So removing `d` doesn't change the aggregate

**Consequence**: Subsumption-based decay preserves aggregate.

### decay_dropConflict (Drop-Persistent-Conflict)

**Implementation** (`interpreter.ts:159-246`):
```typescript
function applyDropPersistentConflict(state, params): RuntimeState {
  // ... track conflict persistence per element ...

  if (history[i] >= persistThreshold) {
    // Resolve conflict at element i
    if (targetTruth === 'neither') {
      return { truth: Neither, resolved: emitPressure ? 'Unres' : aggregated.resolved };
    }
    // ... or keep one side ...
  }

  // REPLACE context with single resolved cut
  return { ...state, context: [resolvedCut] };
}
```

**Semantics**: After `persistThreshold` steps of conflict, modify the context to resolve it.

**Property**: `Agg(decay_dropConflict(C)) ≠ Agg(C)` (intentionally)
- Converts Both → Neither/Unres or Both → In or Both → Out
- Replaces entire context with a single "resolved" cut

**Consequence**: Can change conflictOn (Both → not Both).

---

## Summary: What Changes What

| Operation | Changes truthOf(Agg)? | Changes resolvedOf(Agg)? | Changes conflictOn? |
|-----------|:---------------------:|:------------------------:|:-------------------:|
| aggregate | NO | NO | NO |
| unfold | NO | YES (adds Unres) | NO |
| identity | NO | NO | NO |
| decay_absorb | NO | NO | NO |
| decay_dropConflict | YES | YES | YES |

---

## Implications for Switch Bound

### Canonical System (decay_absorb only)

All operations preserve `truthOf(Agg)`:
- aggregate: idempotent
- unfold: Neither is truth-identity
- identity: complete identity
- decay_absorb: aggregate-preserving

**Therefore**: `conflictOn` never changes → `switches = 0`

### Drop-Conflict System (decay_dropConflict enabled)

Only decay_dropConflict can change `truthOf(Agg)`:
- It can only DECREASE conflict (Both → not Both)
- No operation can INCREASE conflict (not Both → Both)
  - Would require adding cuts with divergent In/Out at same element
  - aggregate returns existing info (can't create new divergence)
  - unfold returns Neither (can't create In or Out)

**Therefore**: `conflictOn` can only go `true → false` → `switches ≤ 1`

---

## Verification Status

| Property | Status | Evidence |
|----------|--------|----------|
| `Agg(decay_absorb(C)) = Agg(C)` | ✓ VERIFIED | Exhaustive test (15625/15625) |
| `truthOf(Agg([aggregate, ...C])) = truthOf(Agg(C))` | ✓ VERIFIED | Join idempotence |
| `truthOf(Agg([unfold, ...C])) = truthOf(Agg(C))` | ✓ VERIFIED | Neither is truth-identity |
| `truthOf(Agg([identity, ...C])) = truthOf(Agg(C))` | ✓ VERIFIED | Complete identity |
| decay_dropConflict only decreases conflict | ⚠ TO VERIFY | Code inspection suggests yes |

---

## See Also

- `SWITCH-BOUND.md` - Switch bound theorems
- `DEFINITIONS.md` - Precise type definitions
- `fold-expr.ts` - Fold implementations
- `context.ts` - Subsumption and update
- `interpreter.ts` - Decay implementations
