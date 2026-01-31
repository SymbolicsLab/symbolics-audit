# Evidence TTL Specification

**Date**: 2026-01-29
**Status**: DRAFT
**Related**: EVIDENCE-INTERFACE.md, ADDITIVE-EVIDENCE-BOUND.md

---

## Definition

Each evidence item has a **time-to-live (TTL)**: the number of steps until expiration.

```typescript
interface EvidenceWithTTL {
  source: string;
  cut: Cut;
  timestamp: number;       // Original evidence timestamp
  ingestedAt: number;      // Step when ingested
  expiresAt: number;       // ingestedAt + ttl
}
```

## Expiration Semantics

At each step, before action selection:
1. Check all ingested evidence
2. Remove any where `currentStep >= expiresAt`
3. Recompute context (remove expired cuts)
4. Then proceed with normal policy

## Effect on Truth

- When evidence expires, its cut is removed from context
- Aggregate is recomputed from remaining cuts
- Truth support can decrease (non-monotone!)
- Conflict can be created AND resolved

## Two TTL Models

### Hard TTL (Phase 3B.3)
- Each evidence expires exactly at `ingestedAt + k`
- Deterministic, easy to analyze
- Predictable memory horizon

### Exponential Decay (Future)
- Each step, evidence survives with probability α
- Stochastic, smoother dynamics
- More realistic "forgetting" model

## Invariants

- Total ingested evidence = `ingestedCount` (tracked for analysis)
- Active evidence = evidence where `currentStep < expiresAt`
- Aggregate depends only on active evidence (plus initial context)
- `activeCount + expiredCount = ingestedCount`

## Conservativity

TTL is NOT conservative (by design):
- It removes truth support
- This is the mechanism that enables cycling
- It's explicit and transparent (not hidden in fold)

## Interpretation

TTL represents an **active memory horizon**:
- k is the institution's memory half-life
- Audit horizon / operational cadence
- Not "forgetting" as failure; forgetting as operational scope

---

## Memory Architecture

### baseContext (STABLE)
- **Does not change after initialization**
- Contains: Initial prior cuts from init strategy (empty by default)
- Role: Fixed background knowledge / priors
- Implementation: Preserved in `updateStateAfterFold`, never mutated

### Evidence Store (TTL-managed)
- **ONLY source of time-varying truth support**
- Managed by TTLEvidenceManager
- Expiration removes truth support
- Evidence added via DoIngest action

### context (computed)
- Rebuilt when evidence changes: `baseContext + active evidence cuts`
- Used for all aggregate computations
- Not directly mutated; recomputed from sources

### Implication for Cycling
Since baseContext is stable, all cycling dynamics come from:
1. Evidence ingestion (adds truth support)
2. Evidence expiration (removes truth support)

DoStabilize/DoExplore modify `context` but NOT `baseContext`,
so they don't create a "second memory store" that accumulates.

---

## Contract

### Configuration

```typescript
interface TTLConfig {
  enabled: boolean;   // Can disable for baseline comparison
  ttl: number;        // Steps until expiration (k)
}
```

### Events

```typescript
type EvidenceExpiredEvent = {
  type: 'EvidenceExpired';
  step: number;
  count: number;           // How many expired this step
  sources: string[];       // Which evidence items expired
};
```

### State Extension

```typescript
interface RuntimeState {
  // ... existing fields

  ttlManager?: TTLEvidenceManager;
  baseContext: Context;    // Context before evidence
  // context = baseContext + active evidence cuts
}
```

---

## Interaction with Policy

Evidence expiration happens BEFORE action selection:

```
1. Check for expired evidence
2. If any expired:
   a. Remove expired cuts from context
   b. Emit EvidenceExpired event
3. Compute pressure on updated context
4. Select action via policy
5. Execute action
```

This means:
- Expiration can change pressure mid-run
- Policy sees post-expiration state
- DoStabilize/DoExplore decisions reflect current active evidence

---

## Theoretical Implications

### Additive Evidence Bound No Longer Applies

With TTL enabled:
- Truth aggregate is NOT monotone (can decrease)
- `conflictOn` can flip in BOTH directions
- `switches` is UNBOUNDED in principle

### State Space Analysis

Under TTL with finite evidence stream (λ items total, k TTL):
- At most `min(λ, k)` evidence items active at once
- If evidence is consumed faster than it expires: window fills
- If evidence is consumed slower: window never fills

### Cycling Conditions

Sustained cycling requires:
1. Ongoing evidence supply (or cycling of existing evidence)
2. Evidence with conflicting polarity
3. TTL short enough that conflicts don't persist forever
4. TTL long enough that conflicts form before expiring

The "sweet spot" for cycling is a balance of these factors.

---

## See Also

- `EVIDENCE-INTERFACE.md` - Core evidence specification
- `ADDITIVE-EVIDENCE-BOUND.md` - Why TTL is needed for cycling
- `conjectures/CYCLING-DEFINITION.md` - What counts as "sustained cycling"
