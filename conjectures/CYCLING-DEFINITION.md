# Cycling Definition

**Date**: 2026-01-29
**Status**: SPECIFICATION
**Related**: ADDITIVE-EVIDENCE-BOUND.md, EVIDENCE-TTL.md

---

## Motivation

We learned the "threshold artifact" lesson in Phase 2.5.
Do not define cycling by a single arbitrary threshold.

---

## Robust Criteria for "Sustained Cycling"

A trajectory τ exhibits **sustained cycling** if ALL of:

1. **Multiple alternations**: `switches(τ) ≥ 4`
2. **Full cycles**: At least 2 complete off→on→off or on→off→on cycles
3. **Non-degenerate**: Trajectory length ≥ 100 steps
4. **Minimum dwell time** (optional): Each phase lasts ≥ 3 steps

---

## Primary Observable

Report the **full switch distribution**, not just "% cycling".

```
Switch distribution:
  0 switches: 45%
  1 switch:   30%
  2 switches: 15%
  3 switches:  7%
  4+ switches: 3%
```

This avoids hiding structure behind a single threshold.

---

## Secondary Observables

### Duty Cycle
Fraction of time with `conflictOn = true`:
```
dutyCycle = stepsWithConflict / totalSteps
```

### Cycle Length Distribution
If cycling detected, measure length of each on/off phase:
```
cycleLengths = [12, 8, 15, 10, ...]  // steps per phase
meanCycleLength = mean(cycleLengths)
```

### Conflict Mass Autocorrelation
Detect periodicity in conflict dynamics:
```
autocorr(lag) = correlation(conflictMass[t], conflictMass[t+lag])
```
Periodic cycling shows peaks at regular intervals.

---

## Classification

### No Cycling (switches ≤ 1)
- Additive evidence bound applies
- System reaches stable conflict state (or never has conflict)
- Monotone dynamics

### Transient Cycling (2 ≤ switches ≤ 3)
- Some switching but not sustained
- May be transient response to initial conditions
- Not robust to parameter variation

### Sustained Cycling (switches ≥ 4)
- Multiple full cycles
- Robust alternation pattern
- Candidate for "metabolic" interpretation

---

## What We DON'T Claim

1. **"Metabolic" without evidence of robust cycling**
   - The term implies sustained dynamics
   - Single switch ≠ metabolism

2. **Cycling rate without sensitivity analysis**
   - Report across TTL values
   - Check robustness to seeds

3. **Universal cycling**
   - Cycling may only occur in narrow parameter regime
   - This is itself informative

---

## Measurement Protocol

For any trajectory:

```typescript
interface CyclingMetrics {
  // Primary
  switches: number;
  isSustainedCycling: boolean;  // switches >= 4 && steps >= 100

  // Secondary
  dutyCycle: number;
  cycleLengths: number[];
  meanCycleLength: number | null;

  // Distribution support
  conflictOnHistory: boolean[];
}

function classifyTrajectory(metrics: CyclingMetrics):
  'no-cycling' | 'transient' | 'sustained' {
  if (metrics.switches <= 1) return 'no-cycling';
  if (metrics.switches <= 3) return 'transient';
  return 'sustained';
}
```

---

## See Also

- `ADDITIVE-EVIDENCE-BOUND.md` - Why switches ≤ 1 without TTL
- `spec/EVIDENCE-TTL.md` - TTL specification
- `experiments/ttl-cycling/PROTOCOL.md` - Experimental design
