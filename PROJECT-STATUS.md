# Symbolics Project Status

**Date**: 2026-01-29
**Arc**: DSL Development Phases 1-12 + Phase 2 Semantic Bridge + Phase 2.5 Ablation
**Epistemic Status**: Grounded (see below)

---

## Phase 2.5 Critical Finding: Prior Results Were Artifact

The "metabolic tension" result (22.5% with 3+ switches) was caused by **placeholder fold implementations** that injected uniform `sideIn` at every element.

### Ablation Comparison

| Metric | Placeholder | Canonical |
|--------|-------------|-----------|
| Max switches | 3 | **2** |
| Mean switches | 1.90 | **1.16** |
| ≥3 switches | 22.5% | **0.0%** |

### Domain Size Scaling (Canonical)

| Domain | Runs | Max | Mean | ≥2 | ≥3 |
|--------|------|-----|------|-----|-----|
| |U|=5 | 239 | 2 | 0.79 | 28.8% | 0% |
| |U|=10 | 319 | 2 | 1.11 | 46.0% | 0% |
| |U|=15 | 2249 | 2 | 1.16 | 39.2% | 0% |
| |U|=30 | 559 | 2 | 1.36 | 51.5% | 0% |

**The 2-switch maximum is consistent across all domain sizes tested.**

The prior results are invalid as evidence about the formal system.
See `symbolics-dsl/experiments/canonical-tension/RESULTS.md` for full analysis.

---

## What Is Actually Verified (Agda --safe --without-K)

The following have been formally proven with no postulates:

- Belnap four-valued truth representation (`mkTruth` encoding)
- Side = Truth × Resolved type structure
- Lattice properties: associativity, commutativity, idempotence of join
- T-failure countermodel (□φ ⊭ φ in non-reflexive frames)
- Extensional equality for Cuts is an equivalence relation
- De Morgan laws hold for the Truth bilattice
- Conflict preservation: `In ⊔ᵗ Out = Both`
- Empty aggregation identity: `joinAllRes [] = mkSide Neither Res`

## What Is Conjectural / Postulated

The following are **not proven** and rely on postulates:

- Lyapunov potential properties (7 postulates in `Mechanics.Potential.Conjectures`)
- Fold idempotence (SPEC-FOLD-002 - conjecture)
- Fold conservativity (SPEC-FOLD-003 - conjecture)

**Impact**: All claims about system convergence and stability are unproven.

---

## Implementation Status (Phase 2 Complete)

### TypeScript Folds ✅ FIXED
Location: `symbolics-dsl/src/runtime/fold-expr.ts`
Status: **Real semantics implemented**
```typescript
case 'aggregate':
  return aggregateCut(state.context);  // Actual pointwise join
```

### Subsumption Check ✅ FIXED
Location: `symbolics-dsl/src/runtime/context.ts`
Status: **Real lattice order implemented**
```typescript
export function isSubsumed(d: Cut, c: Cut, domainSize: number): boolean {
  return elements.every(i => sideLeq(d(i), c(i)));
}
```

### Update with Decay ✅ FIXED
Location: `symbolics-dsl/src/runtime/context.ts`
Uses Finite.agda semantics: add new cut, remove subsumed.

### Agda-TS Equivalence ✅ ESTABLISHED
- 29 semantic equivalence tests
- 9 Agda grounding tests
- Reference evaluator for cross-validation

---

## Specs by Epistemic Status (Total: 61)

| Category | Count | Notes |
|----------|-------|-------|
| Verified theorems (Agda proof) | 20 | Lattice properties, T-failure |
| Definitions (no proof needed) | 21 | Type encodings, terminology |
| Conjectures (unproven claims) | 8 | Lyapunov, idempotence |
| Bridges (cross-layer mapping) | 5 | Theory↔Agda translations |
| Theory-only (philosophical) | 7 | No formalization expected |

---

## Test Coverage

| Category | Tests | Status |
|----------|-------|--------|
| Golden tests | 60 | ✅ Pass |
| Semantic equivalence | 29 | ✅ Pass |
| Agda grounding | 9 | ✅ Pass |
| Total | 98 | ✅ Pass |

---

## Repository Overview

### symbolics-core (Agda)
- Verified: Belnap types, lattice operations, T-failure
- Unverified: Potential dynamics, fold properties
- DSL layer: Applications/DSL/ with FoldLibrary, Elab, Run

### symbolics-audit
- 61 specs in registry.yaml
- CANONICAL-SEMANTICS.md: Authoritative spec for TS implementation
- RESEARCH-QUESTIONS.md: Open and resolved questions

### symbolics-dsl (TypeScript)
- Phase 2 complete: Real Agda semantics implemented
- 98 tests passing
- Canonical tension experiment: 3368 runs across domain sizes

### symbolics-research
- Vault notes on theory concepts

---

## What Canonical Semantics Show

Under real Agda semantics:
- **Maximum switches**: 2 (conflict can appear, resolve, return once)
- **No sustained cycling**: After one return, conflicts resolve permanently
- **High stability rate**: 96.7% of runs reach stable termination

The system is conservative. Sustained "metabolic cycling" does not occur with current operators.

---

## Next Steps (Research Fork)

The question "does the formal system exhibit sustained cycling?" has a preliminary answer: **No, under current configuration.**

Options for Phase 3:

**A. Accept stability as the result**
- The formal system is conservative
- "Metabolism" metaphor may not apply
- Document what the system actually does

**B. Add legitimate novelty source**
- Design evidence interface or unfold operator
- Requires formal conservativity constraints
- Must not be a hidden forcing function

**C. Explore different policies**
- Test non-homeostatic policies
- Test different decay mechanisms
- Search parameter space more thoroughly

See `DESIGN-DECISIONS.md` for detailed analysis.

---

## Development Environment

- Node.js for TypeScript runtime
- Agda 2.6+ for formal verification
- Python 3 for visualization tools

## See Also

- `LIMITATIONS.md` - Known gaps and their status
- `RESEARCH-QUESTIONS.md` - Open and resolved questions
- `DESIGN-DECISIONS.md` - Pending architectural decisions
