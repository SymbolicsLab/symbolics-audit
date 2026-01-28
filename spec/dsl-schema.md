# DSL Agent Specification Schema v0.1.0

## Overview

This schema defines the JSON format for AgentSpec, the configuration object
that defines a symbolic agent. The schema is versioned and tracked under audit.

**Spec Reference:** SPEC-DSL-007

## Schema Version

- Schema version: 0.1.0
- Compatible mechanics version: Phase 3 (Belnap four-valued, two-channel Side)
- Agda source: `Applications.DSL.Core.AgentSpec`

## Root Object

```json
{
  "version": {
    "dsl": "0.1.0",
    "mechanics": "<git-hash-or-spec-version>"
  },
  "domain": {
    "elements": ["Earth", "Air", "Fire", "Water", "Aether"]
  },
  "folds": {
    "stabilize": {
      "name": "aggregate",
      "params": {}
    },
    "explore": {
      "name": "unfold",
      "params": {}
    }
  },
  "decay": {
    "name": "none",
    "params": {}
  },
  "policy": {
    "name": "homeostatic",
    "params": {}
  },
  "regime": {
    "lo": 1,
    "hi": 3,
    "maxSteps": 100,
    "stabilityThreshold": 3
  },
  "observables": ["truth_distribution", "pressure_ratio", "conflicts"],
  "termination": {
    "stopOnCrystallize": true,
    "stopOnDissolve": true
  }
}
```

## Field Definitions

### version (required)

| Field | Type | Description |
|-------|------|-------------|
| `dsl` | string | Semantic version of this schema (e.g., "0.1.0") |
| `mechanics` | string | Git hash or spec version identifying the Agda core |

### domain (required)

| Field | Type | Description |
|-------|------|-------------|
| `elements` | string[] | Array of string labels for domain elements |

**Constraints:**
- Must have at least one element (non-empty domain)
- Elements should be unique (duplicate handling is undefined)

### folds (required)

| Field | Type | Description |
|-------|------|-------------|
| `stabilize` | FoldExpr | Fold expression applied when pressure > hi |
| `explore` | FoldExpr | Fold expression applied when pressure < lo |

**FoldExpr** can be a simple reference or a composite expression.

#### Simple Reference (backward compatible)
```json
{ "type": "ref", "name": "aggregate", "params": {} }
```
Or shorthand (deprecated but supported):
```json
{ "name": "aggregate", "params": {} }
```

#### Sequential Composition
```json
{
  "type": "seq",
  "first": { "type": "ref", "name": "resolve-stable", "params": {} },
  "second": { "type": "ref", "name": "aggregate", "params": {} }
}
```
Applies first, then second. Pipeline semantics.

#### Bounded Repetition
```json
{
  "type": "repeat",
  "fold": { "type": "ref", "name": "aggregate", "params": {} },
  "count": 3
}
```
Applies fold `count` times. Max count: 10.

#### Conditional
```json
{
  "type": "if",
  "metric": "conflicts",
  "cmp": "gt",
  "threshold": 2,
  "then": { "type": "ref", "name": "resolve-stable", "params": {} },
  "else": { "type": "ref", "name": "aggregate", "params": {} }
}
```
If metric comparison is true, apply `then`, else apply `else`.

**Available Metrics:**
- `pressure` - Unres count
- `conflicts` - Both count
- `inCount`, `outCount`, `neitherCount` - Truth distribution
- `cutCount` - Context structure size

**Comparison Operators:** `gt`, `lt`, `eq`, `gte`, `lte`

**FoldExpr Limits:**
- Max depth: 5
- Max repeat count: 10
- Max nodes: 20

These limits keep expressions analyzable and prevent unbounded computation.

### decay (required)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Stable identifier from Decay Registry |
| `params` | object | Parameter name → value mapping |

### policy (required)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Stable identifier from Policy Registry |
| `params` | object | Parameter name → value mapping |

### regime (required)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `lo` | number | - | Lower pressure threshold (natural number) |
| `hi` | number | - | Upper pressure threshold (natural number) |
| `maxSteps` | number | 100 | Maximum steps before budget termination |
| `stabilityThreshold` | number | 3 | Steps without change for crystallization |

**Constraints:**
- `lo` <= `hi` (invalid regime otherwise)
- `maxSteps` > 0
- `stabilityThreshold` >= 1

### observables (required)

Array of observable identifiers (strings):

| ID | Description | Agda Source |
|----|-------------|-------------|
| `truth_distribution` | Neither/In/Out/Both counts | `Observe.countNeither`, etc. |
| `pressure_ratio` | Unres/Res counts | `Observe.pressureCount` |
| `conflicts` | Both count | `Observe.conflictCount` |
| `intervals` | Interval states (future) | — |

### termination (optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `stopOnCrystallize` | boolean | true | Stop when pressure = 0 and stable |
| `stopOnDissolve` | boolean | true | Stop when pressure = domain size |

## Registries

### Fold Registry

| ID | Description | Params | Spec Refs | Agda Source |
|----|-------------|--------|-----------|-------------|
| `identity` | No-op, returns input unchanged | none | SPEC-FOLD-001 | `Standard.identityMeta` |
| `aggregate` | Joins all cuts using Resolution | none | SPEC-JOIN-001, SPEC-CONTRA-004 | `Standard.aggregateMeta` |
| `consensus` | Threshold-based agreement | `threshold: number` | SPEC-FOLD-001 (conjecture) | `Standard.consensusMeta` |
| `unfold` | Increases exploration pressure | none | SPEC-UNFOLD-001 | `Standard.unfoldMeta` |
| `resolve-stable` | Converts Neither/Unres to Neither/Res | none | — | `Standard.resolveStableMeta` |

### Decay Registry

| ID | Description | Params | Spec Refs | Agda Source |
|----|-------------|--------|-----------|-------------|
| `none` | No decay | none | — | `Decay.noneMeta` |
| `priority` | Priority-based decay | none | SPEC-DECAY-001 | `Decay.priorityMeta` |
| `forget-stale` | Removes cuts unchanged for K steps | `staleThreshold: number` (1-10, default 3) | — | `Decay.forgetStaleMeta` |

### Policy Registry

| ID | Description | Params | Spec Refs | Agda Source |
|----|-------------|--------|-----------|-------------|
| `homeostatic` | Pressure-based regime switching | none | SPEC-MODAL-001, SPEC-METAB-001 | `Policy.homeostaticMeta` |
| `crystalline` | Always stabilize | none | — | `Policy.crystallineMeta` |

## Policy Semantics

The homeostatic policy decision rules (see `Runtime/Policy.agda`):

```
Given: regime with thresholds (lo, hi)
       pressure = count of elements with Unres in aggregated context

Decision:
  if pressure > hi  → DoStabilize (reduce exploration, commit)
  if pressure < lo  → DoExplore (increase exploration, unfold)
  if lo ≤ pressure ≤ hi → DoDecay (maintain, let system settle)
```

**Policy Axioms (proven in Agda):**
- Empty context explores: `pressureCount(∅) = 0 < lo → DoExplore`
- High pressure stabilizes: `pressureCount(ctx) > hi → DoStabilize`
- Low pressure explores: `pressureCount(ctx) < lo → DoExplore`

## Errors

The runtime produces errors matching Agda's `ElabError` type:

| Error Type | Description | Agda Constructor |
|------------|-------------|------------------|
| `UnknownFold` | Fold ID not in registry | `UnknownStabilize`, `UnknownExplore` |
| `UnknownDecay` | Decay ID not in registry | `UnknownDecay` |
| `UnknownPolicy` | Policy ID not in registry | `UnknownPolicy` |
| `InvalidParam` | Parameter out of valid range | `InvalidParam` |
| `DomainEmpty` | Domain has no elements | `DomainEmpty` |
| `InvalidRegime` | lo > hi or invalid thresholds | `InvalidRegime` |
| `InvalidVersion` | Incompatible schema version | `VersionMismatch` |

## Output

### Analysis Report

```json
{
  "viability": "viable",
  "regimePrediction": "homeostatic",
  "specsReliedOn": [
    {"id": "SPEC-JOIN-001", "status": "verified"},
    {"id": "SPEC-CONTRA-004", "status": "verified"},
    {"id": "SPEC-MODAL-001", "status": "verified"}
  ],
  "warnings": []
}
```

**Viability values:** `"viable"` | `{"nonViable": "<reason>"}`

**Regime prediction values:** `"creative"` | `"homeostatic"` | `"crystalline"` | `"dissolving"` | `"unknown"`

### Trajectory

```json
{
  "steps": [
    {
      "snapshot": {
        "step": 0,
        "neitherCount": 1,
        "inCount": 2,
        "outCount": 1,
        "bothCount": 1,
        "unresCount": 2,
        "resCount": 3
      },
      "events": ["FoldApplied:aggregate"]
    }
  ],
  "finalState": {
    "step": 10,
    "neitherCount": 5,
    "inCount": 0,
    "outCount": 0,
    "bothCount": 0,
    "unresCount": 0,
    "resCount": 5
  },
  "termination": "crystallized"
}
```

**Termination values:** `"budget"` | `"crystallized"` | `"dissolved"` | `"stable"`

**Event formats:**
- `"FoldApplied:<fold-id>"`
- `"UnfoldApplied:<fold-id>"`
- `"DecayApplied"`
- `"RegimeSwitch:<from>-><to>"`
- `"Crystallized"`
- `"Dissolved"`

## Snapshot Semantics

The snapshot captures the **aggregated view** of the system:

> For each element u in the domain, compute `apply (aggregate Resolution ctx) u`.
> This shows what the system is "committed to" after all cuts are joined.

**Invariant:** `neitherCount + inCount + outCount + bothCount = domain.elements.length`

**Invariant:** `unresCount + resCount = domain.elements.length`

## Version Compatibility

| Schema Version | Mechanics Version | Notes |
|----------------|-------------------|-------|
| 0.1.0 | Phase 3 | Belnap four-valued, two-channel Side |

Future versions will maintain backwards compatibility where possible.

## CLI Usage

```bash
# Validate a spec file
symbolics-dsl validate spec.json

# Analyze without running
symbolics-dsl analyze spec.json

# Run simulation
symbolics-dsl run spec.json --steps=50

# Output formats
symbolics-dsl run spec.json --format=json
symbolics-dsl run spec.json --format=summary
```

## See Also

- `Applications.DSL.Core` - Agda AgentSpec definition
- `Applications.DSL.Elab` - Elaboration and error types
- `Applications.DSL.Run` - Runtime execution
- `Applications.DSL.Registry` - Stable ID mappings
