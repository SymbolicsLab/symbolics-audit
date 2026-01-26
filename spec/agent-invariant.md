# Minimal Complete Agent Invariant

**Spec Reference:** SPEC-DSL-009

An AgentSpec is **complete** if and only if it specifies all required structure
for meaningful execution. This document defines that invariant.

## Required Fields

1. **Domain**: A finite set U of elements (non-empty)
2. **Stabilize Fold**: Applied when pressure > hi
3. **Explore Fold**: Applied when pressure < lo
4. **Decay Strategy**: Applied when lo ≤ pressure ≤ hi
5. **Policy**: Decision rule for choosing actions
6. **Regime Window**: (lo, hi) thresholds with lo ≤ hi
7. **Termination**: Conditions for stopping (maxSteps required)

## Optional Fields

| Field | Default | Description |
|-------|---------|-------------|
| `termination.stopOnCrystallize` | `true` | Stop when pressure = 0 and stable |
| `termination.stopOnDissolve` | `true` | Stop when pressure = domain size |
| `regime.stabilityThreshold` | `3` | Steps without change for stability |
| `observables` | `["truth_distribution", "pressure_ratio"]` | What to track |

## Completeness Invariant

```
isComplete(spec) =
  domain.elements.length > 0 ∧
  stabilizeFold ∈ FOLD_REGISTRY ∧
  exploreFold ∈ FOLD_REGISTRY ∧
  decay ∈ DECAY_REGISTRY ∧
  policy ∈ POLICY_REGISTRY ∧
  regime.lo ≤ regime.hi ∧
  regime.maxSteps > 0 ∧
  regime.stabilityThreshold ≥ 1
```

This invariant is checked by:
- **Agda**: `Applications.DSL.Elab.elaborate`
- **TypeScript**: `src/schema/validate.ts:validateAgentSpec`

## Why This Set?

| Field | Rationale |
|-------|-----------|
| **Domain** | Without elements, nothing to observe or transform |
| **Stabilize Fold** | Core of regime-based steering (high pressure response) |
| **Explore Fold** | Core of regime-based steering (low pressure response) |
| **Decay** | What happens in the homeostatic window |
| **Policy** | How to choose between stabilize/explore/decay |
| **Regime** | Defines the pressure boundaries that partition behavior |
| **Termination** | Prevents infinite runs, defines success conditions |

Everything else is configuration, not structure.

## Viability vs Completeness

**Completeness** is structural: all required fields are present and valid.

**Viability** is semantic: the spec can produce meaningful behavior.

A complete spec may still be non-viable if:
- Folds are miscategorized (stabilize = expander)
- Regime is degenerate (lo = hi = 0)
- Domain is pathologically small

The analyzer checks both completeness (via validation) and viability (via analysis).

## Initial State

A complete AgentSpec starts with:
- **Context**: Empty (no cuts)
- **All elements**: Neither/Res (no information, resolved)
- **Pressure**: 0 (empty context has no unresolved elements)

This means:
- `pressureCount(∅) = 0`
- If `lo > 0`, first action is always DoExplore
- If `lo = 0`, first action depends on `hi` (DoDecay if `0 ≤ 0 ≤ hi`)

## Invariant Preservation

During execution, these invariants are maintained:

1. **Truth Sum**: `neitherCount + inCount + outCount + bothCount = domain.length`
2. **Resolved Sum**: `unresCount + resCount = domain.length`
3. **Monotonicity**: Context can only grow (without decay) or shrink (with decay)
4. **Termination**: Eventually reaches budget, crystallized, dissolved, or stable

## Error Conditions

Incomplete specs produce `ElabError`:

| Error | Condition |
|-------|-----------|
| `DomainEmpty` | `domain.elements.length = 0` |
| `UnknownStabilize` | Stabilize fold not in registry |
| `UnknownExplore` | Explore fold not in registry |
| `UnknownDecay` | Decay not in registry |
| `UnknownPolicy` | Policy not in registry |
| `InvalidRegime` | `lo > hi` or `maxSteps ≤ 0` |

## See Also

- `dsl-schema.md` - Full JSON schema documentation
- `taxonomy.md` - Fold and decay classification
- `Applications.DSL.Elab` - Agda elaboration
