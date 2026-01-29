# Precise Definitions for Switch Bound Conjecture

**Date**: 2026-01-29
**Related**: SWITCH-BOUND.md

This document pins down the precise definitions used in the switch bound conjecture.

---

## Core Types

### Truth (Belnap Four-Valued)

```typescript
type Truth = { supportsIn: boolean; supportsOut: boolean };

Neither = { supportsIn: false, supportsOut: false }  // No information
In      = { supportsIn: true,  supportsOut: false }  // Positive only
Out     = { supportsIn: false, supportsOut: true  }  // Negative only
Both    = { supportsIn: true,  supportsOut: true  }  // Conflict
```

Agda encoding (`Mechanics.Primitive`):
```agda
record Truth : Set where
  constructor mkTruth
  field supportsIn supportsOut : Bool
```

### Side

```typescript
type Resolved = 'Res' | 'Unres';
type Side = { truth: Truth; resolved: Resolved };
```

Key values:
- `sideIn = { truth: In, resolved: 'Res' }`
- `sideOut = { truth: Out, resolved: 'Res' }`
- `sideBoth = { truth: Both, resolved: 'Res' }`
- `sideNeither = { truth: Neither, resolved: 'Res' }`
- `sideRem = { truth: Neither, resolved: 'Unres' }` (Remainder/pressure)

### Cut

A function from element index to Side:
```typescript
type Cut = (index: number) => Side;
```

### Context

A list of cuts:
```typescript
type Context = Cut[];
```

---

## Aggregate Operations

### aggregateAt(ctx, index)

Computes the aggregated Side at element `index` by joining all cuts pointwise.

```typescript
function aggregateAt(ctx: Context, index: number): Side {
  if (ctx.length === 0) {
    return { truth: Neither, resolved: 'Res' };  // Identity element
  }
  return ctx.reduce((acc, cut) => joinSide(acc, cut(index)),
                    { truth: Neither, resolved: 'Res' });
}
```

From Agda (`Context.agda:116-118`):
```agda
joinAllRes [] = mkSide Neither Res
joinAllRes (s ∷ ss) = s ⊔ˢ joinAllRes ss
```

### aggregateCut(ctx)

Returns the full aggregate cut:
```typescript
function aggregateCut(ctx: Context): Cut {
  return (index) => aggregateAt(ctx, index);
}
```

---

## Conflict Detection

### isBoth(truth)

```typescript
function isBoth(t: Truth): boolean {
  return t.supportsIn && t.supportsOut;
}
```

From Agda:
```agda
isBoth : Truth → Bool
isBoth (mkTruth true true) = true
isBoth _ = false
```

### hasConflict(side)

```typescript
function hasConflict(s: Side): boolean {
  return isBoth(s.truth);
}
```

Location: `symbolics-dsl/src/runtime/side.ts:133-135`

### bothCount(state)

The number of elements in the domain with `Both` truth in the aggregate:

```typescript
function bothCount(state: RuntimeState): number {
  let count = 0;
  for (let i = 0; i < domainSize(state); i++) {
    const side = aggregateAt(state.context, i);
    if (isBoth(side.truth)) count++;
  }
  return count;
}
```

Location: `symbolics-dsl/src/runtime/state.ts:79-90`

### conflictOn(state)

**Definition**: `conflictOn(s) = bothCount(s) > 0`

A state has conflict if ANY element has Both truth value.

```typescript
function conflictOn(state: RuntimeState): boolean {
  return bothCount(state) > 0;
}
```

---

## Switch Detection

### switch(t)

A switch occurs at step t when conflict changes between steps:

**Definition**: `switch(t) = conflictOn(s_t) XOR conflictOn(s_{t+1})`

```typescript
function isSwitch(before: RuntimeState, after: RuntimeState): boolean {
  return conflictOn(before) !== conflictOn(after);
}
```

### switches(trajectory)

**Definition**: `switches(τ) = Σ_{t=0}^{T-1} switch(t)`

Total number of conflict toggles in the trajectory.

```typescript
function countSwitches(trajectory: RuntimeState[]): number {
  let count = 0;
  for (let i = 0; i < trajectory.length - 1; i++) {
    if (isSwitch(trajectory[i], trajectory[i + 1])) {
      count++;
    }
  }
  return count;
}
```

---

## Policy Action Selection

### Pressure

**Definition**: `pressure(s) = unresCount(s)` = number of elements with `resolved === 'Unres'`

```typescript
function pressureCount(state: RuntimeState): number {
  let count = 0;
  for (let i = 0; i < domainSize(state); i++) {
    const side = aggregateAt(state.context, i);
    if (side.resolved === 'Unres') count++;
  }
  return count;
}
```

Location: `symbolics-dsl/src/runtime/state.ts:248-255`

### Homeostatic Policy Decision

Given state `s` with pressure `p = pressureCount(s)` and regime thresholds `(lo, hi)`:

| Condition | Action |
|-----------|--------|
| `p > hi` | DoStabilize |
| `p < lo` | DoExplore |
| `lo ≤ p ≤ hi` | DoDecay |

```typescript
function homeostaticDecision(state: RuntimeState, regime: Regime): PolicyAction {
  const p = pressureCount(state);
  if (p > regime.hi) return 'DoStabilize';
  if (p < regime.lo) return 'DoExplore';
  return 'DoDecay';
}
```

Location: `symbolics-dsl/src/runtime/policy.ts:40-50`

---

## Action Effects

### DoStabilize

1. Apply stabilize fold expression (typically `aggregate`)
2. Fold expression produces a new cut
3. New cut is added to context using `updateContext` (add + prune subsumed)
4. Step counter increments

**Can change conflict?** POSSIBLY
- Aggregate fold returns `aggregateCut(context)`
- Adding this cut to context may cause subsumption pruning
- Pruning could theoretically affect aggregate (but see Lemma 1)

### DoExplore

1. Apply explore fold expression (typically `unfold`)
2. Fold expression produces a new cut
3. New cut is added to context using `updateContext`
4. Step counter increments

**Can change conflict?** YES
- Unfold (when non-trivial) can introduce new cuts
- New cuts can create conflict: if new cut has `In` where existing has `Out`

### DoDecay

1. Apply decay function (e.g., `drop-persistent-conflict`)
2. May modify existing cuts (not add new ones)
3. Step counter increments

**Can change conflict?** YES
- `drop-persistent-conflict` drops one side of persistent conflicts
- This converts `Both` → `In` or `Both` → `Out`
- So decay can resolve conflicts (turn conflict OFF)

---

## Subsumption and Update

### sideLeq(a, b) - Resolution Order

**Definition**: `a ≤ b` in resolution order

```typescript
function sideLeq(a: Side, b: Side): boolean {
  if (sideEqual(a, sideOut)) return true;  // sideOut is bottom
  if (sideEqual(a, b)) return true;        // Reflexive
  if (sideEqual(a, sideBoth)) return sideEqual(b, sideBoth);  // sideBoth is top
  // ... other cases from Finite.agda:189-201
}
```

Key ordering:
- `sideOut ≤ anything` (bottom)
- `sideBoth ≤ only sideBoth` (top)
- `sideRem ≤ sideIn` but `sideIn ⊈ sideRem`

### isSubsumed(d, c, domainSize)

**Definition**: Cut `d` is subsumed by `c` if `d(i) ≤ c(i)` for all elements `i`.

```typescript
function isSubsumed(d: Cut, c: Cut, domainSize: number): boolean {
  for (let i = 0; i < domainSize; i++) {
    if (!sideLeq(d(i), c(i))) return false;
  }
  return true;
}
```

Location: `symbolics-dsl/src/runtime/context.ts`

### updateContext(ctx, newCut, domainSize)

**Definition**: Add newCut, remove all cuts subsumed by it.

```typescript
function updateContext(ctx: Context, newCut: Cut, domainSize: number): Context {
  const surviving = ctx.filter(cut => !isSubsumed(cut, newCut, domainSize));
  return [newCut, ...surviving];
}
```

Location: `symbolics-dsl/src/runtime/context.ts`

---

## Conjecture Statement (Precise)

For all trajectories τ under:
1. Finite domain U with |U| = n
2. Canonical aggregate: `aggregateCut` computes pointwise join via `joinAllRes`
3. Subsumption-based update: `updateContext` adds new cut, removes subsumed
4. Homeostatic policy: `homeostaticDecision` as defined above
5. No evidence injection: No external cuts added between steps
6. No unfold (or conservative unfold): `unfold` returns identity or aggregate

We have: `switches(τ) ≤ K` for some fixed K.

**Empirically observed**: K = 2

---

## Key Lemmas

### Lemma 1: Decay Preserves Aggregate

**Statement**: For all contexts C and domain sizes n,
```
aggregateCut(updateContext(C, newCut, n)) = aggregateCut([newCut, ...C])
```

**STATUS: FALSE**

The lemma fails because the resolution order ≠ join order. See SWITCH-BOUND.md for details.

Exhaustive test (2-element domain): only 70% of cases preserve aggregate.

**Why it fails**: The resolution order says `Rem ≤ In`, but `join(Rem, In) = In/Unres ≠ In/Res`.
When a cut with `Unres` is removed as "subsumed", its `Unres` contribution is lost.

### Lemma 2: Aggregate is Idempotent

**Statement**: Adding the aggregate cut to a context doesn't change the aggregate.
```
let agg = aggregateCut(C)
aggregateCut([agg, ...C]) = agg
```

**Status**: This should follow from join idempotence.

### Lemma 3: Conflict Creation Requires Divergent Cuts

**Statement**: For conflict to appear at element u:
```
aggregateCut(C)(u) = Both  →  ∃ c₁, c₂ ∈ C. c₁(u).truth = In ∧ c₂(u).truth = Out
```

**Intuition**: `Both = In ⊔ᵗ Out` requires both In and Out support from somewhere.

### Lemma 4: No Spontaneous Conflict

**Statement**: If conflict is absent and we only apply aggregate/decay (no evidence injection), conflict cannot appear.

**This is the key lemma for the switch bound.**

---

## See Also

- `SWITCH-BOUND.md` - Full conjecture with proof strategy
- `symbolics-dsl/src/runtime/policy.ts` - Policy implementation
- `symbolics-dsl/src/runtime/context.ts` - Context operations
- `symbolics-core/src/Mechanics/CutOps.agda` - Agda join operations
