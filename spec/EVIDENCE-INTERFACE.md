# Evidence Interface Specification

**Date**: 2026-01-29
**Status**: DRAFT
**Related**: METABOLISM-IMPOSSIBILITY.md, SWITCH-BOUND.md

---

## Definition

An **Evidence** is a cut with truth content that enters from outside the system.

```typescript
interface Evidence {
  source: string;           // Where it came from (for tracing)
  cut: Cut;                 // The actual truth content
  timestamp: number;        // When it arrived
}

interface EvidenceStream {
  next(): Evidence | null;  // Get next evidence (null if none)
  peek(): Evidence | null;  // Look without consuming
  isEmpty(): boolean;       // Check if stream exhausted
  remaining(): number;      // Count of remaining items
}
```

---

## Motivation

### The Truth-Invariance Problem

Under canonical semantics, we proved (SB-1) that `switches(τ) = 0`:
- DoStabilize adds aggregate (idempotent for truth)
- DoExplore adds Neither/Unres (identity for truth join)
- DoDecay removes absorbed cuts (preserves aggregate)

**No operation changes truth**, so metabolic cycling is impossible.

### The Solution: Explicit Novelty

Evidence provides a **controlled channel** for external observations that:
- Can inject truth support (In, Out, Both) at any element
- Explicitly violates truth-invariance (by design)
- Is logged and traceable
- Can be rate-limited

---

## Contract

### What Evidence CAN Do

1. **Inject truth support** (In, Out, Both) at any element
2. **Change the truth aggregate** (violates truth-invariance)
3. **Create conflict** where none existed (In + Out → Both)
4. **Enable cycling** if evidence stream has appropriate structure

### What Evidence CANNOT Do

1. **Directly modify existing cuts** — only adds new cuts
2. **Bypass the aggregate** — still joins with existing context
3. **Act without logging** — every evidence item is traced
4. **Violate rate limits** — bounded by policy

---

## Integration with System

### New Action: DoIngest

```typescript
type Action = 'DoStabilize' | 'DoExplore' | 'DoDecay' | 'DoIngest';

// DoIngest effect:
// 1. Pop next evidence from stream
// 2. Add evidence.cut to context
// 3. Log evidence to ingestedEvidence array
// 4. Increment step counter
```

### Policy Integration

The policy decides when to check for and ingest evidence. Options:

| Policy | When to Ingest | Rationale |
|--------|---------------|-----------|
| Evidence-first | Before any action | Responsive to environment |
| Explore-trigger | When pressure < lo | "Looking for novelty" |
| Explicit | DoIngest as choosable action | Maximum control |
| Interleaved | Alternate internal/external | Balanced |

See DD-011 for design decision.

---

## Conservativity Constraints

### Rate Limiting

```typescript
interface RateLimits {
  maxPerStep: number;      // Max evidence per step (default: 1)
  maxPerTrajectory: number; // Max total evidence (default: unlimited)
  cooldown: number;        // Min steps between ingests (default: 0)
}
```

### Truth Budget (Optional)

For advanced experiments, limit total truth injection:

```typescript
interface TruthBudget {
  maxInSupport: number;    // Total In flags across all evidence
  maxOutSupport: number;   // Total Out flags across all evidence
  maxBothSupport: number;  // Total Both elements allowed
}
```

### Source Tracking

Every evidence item includes:
- `source`: String identifier for origin
- `timestamp`: When evidence was generated/received
- Enables analysis: "which inputs caused which conflicts"

---

## Evidence Stream Types

### ArrayEvidenceStream

Fixed sequence of evidence items. For deterministic tests.

```typescript
new ArrayEvidenceStream([
  { source: 'test-1', cut: cut1, timestamp: 1 },
  { source: 'test-2', cut: cut2, timestamp: 2 }
]);
```

### RandomEvidenceStream

Generates random evidence with configurable rates.

```typescript
new RandomEvidenceStream({
  elements: ['A', 'B', 'C', 'D', 'E'],
  maxItems: 100,
  seed: 42,
  inRate: 0.3,    // P(supportsIn = true)
  outRate: 0.3,   // P(supportsOut = true)
  bothRate: 0.1   // P(both = true) - overrides in/out
});
```

### EnvironmentEvidenceStream (Future)

For art project: evidence from external environment.

```typescript
new EnvironmentEvidenceStream({
  source: 'social-media',
  parser: (input) => parseToEvidence(input)
});
```

---

## Theorems

### Evidence Breaks Truth-Invariance

**Theorem**: There exist evidence e, context C, and element u such that:
```
truthOf(Agg(e.cut :: C))(u) ≢ truthOf(Agg(C))(u)
```

**Proof**: Constructive. Take:
- C = [] (empty context, aggregate = Neither everywhere)
- e.cut = uniformCut(sideIn) (In everywhere)
- Then truthOf(Agg(e.cut :: C))(u) = In ≠ Neither = truthOf(Agg(C))(u)

### Cycling is Now Possible

**Theorem**: With appropriate evidence stream, switches > 0.

**Proof**: Constructive. Take:
- Initial: No conflict
- Evidence 1: Inject In at element 0
- Evidence 2: Inject Out at element 0
- Now In ⊔ Out = Both → conflict
- Switch from no-conflict to conflict

---

## Relation to Art Project

The symbolic creature's "metabolism" is processing external evidence:

| Art Concept | Formal Mapping |
|-------------|----------------|
| Social interaction | Evidence from environment |
| "Likes" | Evidence with In support |
| "Dislikes" | Evidence with Out support |
| Controversy | Evidence creating Both (conflict) |
| Metabolizing | Processing evidence stream |
| Crystallization | No evidence (truth-invariant) |
| Life | Ongoing evidence processing |

The creature is "alive" when:
1. Evidence stream is non-empty
2. System is processing (ingesting) evidence
3. Conflicts are being created and resolved
4. Switch rate > 0

Without evidence, the creature crystallizes (SB-1: switches = 0).

---

## See Also

- `DESIGN-DECISIONS.md` DD-011 - Evidence ingestion policy
- `results/METABOLISM-IMPOSSIBILITY.md` - Why evidence is needed
- `conjectures/SWITCH-BOUND.md` - What canonical semantics guarantees
