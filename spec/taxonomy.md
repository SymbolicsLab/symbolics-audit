# Fold and Decay Taxonomy

**Spec Reference:** SPEC-DSL-008

This document defines the classification system for folds and decays in the DSL.
Categories enable the analyzer to warn about misconfigurations.

## Fold Categories

### Stabilizers
**Effect:** Reduce Unres (pressure) or make commitments explicit.

| Property | Value |
|----------|-------|
| Pressure tendency | Decreases |
| Risk | Crystallization if overused |
| Use case | High-pressure response |

**Current stabilizers:**
- `consensus` - Commits when agreement threshold met

### Consolidators
**Effect:** Combine cuts without significantly changing pressure.

| Property | Value |
|----------|-------|
| Pressure tendency | Roughly constant |
| Risk | None (neutral operations) |
| Use case | Information aggregation |

**Current consolidators:**
- `identity` - No-op, returns unchanged
- `aggregate` - Joins all cuts via Resolution

### Resolvers
**Effect:** Turn specific patterns into settled states (Res).

| Property | Value |
|----------|-------|
| Pressure tendency | Decreases locally |
| Risk | Premature resolution |
| Use case | Settling unpolarized ambiguity |

**Current resolvers:**
- `resolve-stable` - Neither/Unres → Neither/Res

### Expanders
**Effect:** Increase articulation capacity or introduce new pressure.

| Property | Value |
|----------|-------|
| Pressure tendency | Increases |
| Risk | Dissolution if overused |
| Use case | Low-pressure response |

**Current expanders:**
- `unfold` - Adds sideRem to introduce pressure

## Decay Categories

### None
**Effect:** No decay applied.

Context unchanged during homeostatic window. Growth is unchecked.

**Current:** `none`

### Pruning
**Effect:** Reduce redundancy in context structure.

| Property | Value |
|----------|-------|
| Structure | Context becomes smaller |
| Information | Preserved (only redundancy removed) |
| Pressure | May decrease slightly |

**Current:** `priority` - Keeps highest-priority cuts

### Forgetting
**Effect:** Drop stale or inactive commitments.

| Property | Value |
|----------|-------|
| Structure | Old information removed |
| Information | May be lost |
| Pressure | May change unpredictably |

**Current:** `forget-stale` - Removes cuts unchanged for K steps

### Cooling
**Effect:** Gradually reduce Unres without removing cuts.

| Property | Value |
|----------|-------|
| Structure | Unchanged |
| Information | Preserved |
| Pressure | Decreases slowly |

**Current:** (not yet implemented)

## Category Compatibility Matrix

The analyzer uses categories to detect misconfigured agents:

### Stabilize Fold × Explore Fold

| stabilize \ explore | stabilizer | consolidator | resolver | expander |
|---------------------|------------|--------------|----------|----------|
| **stabilizer** | WARN: both reduce | WARN: steer/no-steer | WARN: both reduce | OK |
| **consolidator** | WARN: no-steer/reduce | WARN: no steering | WARN: no-steer/reduce | MILD: weak steering |
| **resolver** | WARN: both reduce | WARN: steer/no-steer | WARN: both reduce | OK |
| **expander** | WARN: inverted | WARN: expand/no-steer | WARN: inverted | WARN: both expand |

### Recommended Pairings

| stabilize | explore | Assessment |
|-----------|---------|------------|
| stabilizer | expander | Correct pairing |
| resolver | expander | Correct pairing |
| consolidator | expander | Weak steering (consolidator is passive) |

### Anti-Patterns

| stabilize | explore | Problem |
|-----------|---------|---------|
| expander | * | Stabilize increases pressure → dissolution |
| * | stabilizer | Explore decreases pressure → crystallization |
| * | resolver | Explore decreases pressure → crystallization |
| consolidator | consolidator | No effective steering |

## Conceptual Clarifications

### Why is resolve-stable a Fold, not a Decay?

`resolve-stable` is a **Fold** (specifically, a Resolver) because:

1. **Value-level operation**: It transforms Side values (Neither/Unres → Neither/Res)
2. **Pattern-based**: Targets specific semantic pattern, not time-based
3. **Deliberate steering**: It's an intentional stabilization action
4. **Policy-selected**: Chosen by policy decision, not background maintenance

### Why is forget-stale a Decay, not a Fold?

`forget-stale` is a **Decay** (specifically, Forgetting) because:

1. **Time-based operation**: Operates on staleness (K steps unchanged)
2. **Structure-level**: Removes entire cuts, not transforming values
3. **Housekeeping**: Background maintenance, not steering
4. **Always applies**: Runs in homeostatic window regardless of specific values

### General Rule

```
Folds   = deliberate value-level transformations (steering)
Decays  = time/policy-based housekeeping (maintenance)
```

## Analyzer Warnings

The analyzer produces these category-based warnings:

| Condition | Warning |
|-----------|---------|
| `stabilize.category = expander` | "Stabilize fold is an expander; expect dissolution" |
| `explore.category ∈ {stabilizer, resolver}` | "Explore fold reduces pressure; expect crystallization" |
| `stabilize.category = consolidator ∧ explore.category = consolidator` | "Both folds are consolidators; regime won't steer effectively" |

## Adding New Components

When adding a new fold or decay:

1. Determine the correct category based on:
   - Primary effect on pressure
   - Whether it's value-level (fold) or structure-level (decay)
   - Whether it's deliberate steering or background maintenance

2. Update registry.json with the `category` field

3. Verify the analyzer warnings still make sense with the new component

4. Document the component in this taxonomy

## See Also

- `registry.json` - Canonical component definitions
- `agent-invariant.md` - Minimal complete agent structure
- `dsl-schema.md` - Full JSON schema
