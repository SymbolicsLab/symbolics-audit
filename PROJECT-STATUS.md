# Symbolics Project Status (Post-Phase 12)

**Date**: 2026-01-29
**Arc**: DSL Development Phases 1-12 Complete
**Epistemic Status**: Mixed (see below)

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

## What Is Conjectural / Postulated

The following are **not proven** and rely on postulates:

- Lyapunov potential properties (7 postulates in `Mechanics.Potential.Conjectures`)
  - `potential-zero-iff-in-window`
  - `stabilize-reduces-potential-above`
  - `convergence-to-equilibrium`
  - `potential-is-lyapunov` (master conjecture)
- Fold idempotence (SPEC-FOLD-002 - conjecture)
- Fold conservativity (SPEC-FOLD-003 - conjecture)

**Impact**: All claims about system convergence and stability are unproven.

## What Is Incomplete in Implementation

### TypeScript Folds (CRITICAL)
Location: `symbolics-dsl/src/runtime/interpreter.ts:72-99`
Status: **Placeholder implementations** that return uniform cuts
```typescript
case 'aggregate':
  return uniformCut(sideIn);  // Does NOT actually aggregate
case 'unfold':
  return uniformCut(sideRem); // Just adds uniform Rem
```
**Impact**: DSL runtime does NOT implement Agda semantics.

### Subsumption Check (CRITICAL)
Location: `symbolics-core/Mechanics/Context.agda:163-164`
Status: **Always returns true** (placeholder)
**Impact**: Decay cannot actually garbage-collect redundant cuts.

### Agda-TS Equivalence
Status: **Not established**
**Impact**: "Golden test equivalence" tests placeholder behavior only.

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

## Repository Overview

### symbolics-core (Agda)
- Verified: Belnap types, lattice operations, T-failure
- Unverified: Potential dynamics, fold properties
- DSL layer: Applications/DSL/ with FoldLibrary, Elab, Run

### symbolics-audit
- 61 specs in registry.yaml (see epistemic breakdown above)
- SPEC-DSL-001 through SPEC-DSL-021
- DSL schema documentation

### symbolics-dsl (TypeScript)
- **WARNING**: Fold implementations are placeholders
- CLI: validate, analyze, run, sweep, search, diff, capsule
- 60 tests passing (but testing placeholder behavior)

### symbolics-research
- Vault notes on theory concepts (philosophy, not formalization)

---

## Experiment Status: Metabolic Tension

### What Was Observed
- 600 runs with `emitPressure=true` configuration
- Conflict switch distribution: 0 (7.5%), 1 (17.5%), 2 (52.5%), 3 (22.5%)
- Maximum observed switches: 3

### Honest Characterization

| Regime | Max Switches | Description |
|--------|--------------|-------------|
| Static | 1 | Conflict appears, persists |
| Dynamic | 2 | Conflict appears, resolves once |
| **Transient Return** | **3** | **Conflict returns once after resolution** |

**Note**: The term "metabolic cycling" overstates the phenomenon. With max=3 switches, conflict appeared, resolved, and returned once. This is **one return**, not sustained cycling.

### Limitations
- Threshold sensitivity: "Tension zone" ≥3 switches captures exactly 22.5%
  - With threshold ≥2: 75% qualify
  - With threshold ≥4: 0% qualify
- Based on **placeholder implementations**, not true Agda semantics
- Association observed, not causality proven

---

## Key Files

### Verified Core
- `symbolics-core/src/Mechanics/Primitive.agda` - Core types
- `symbolics-core/src/Mechanics/CutOps.agda` - Lattice proofs

### Experiment Artifacts (preliminary)
- `symbolics-dsl/experiments/metabolic-tension/` - Full artifact pack
- `symbolics-dsl/experiments/metabolic-tension/TENSION-ZONE-DEFINITION.md` - Metric definitions

### Specifications
- `symbolics-audit/spec/registry.yaml` - All SPEC entries with epistemic status

---

## Next Steps (Priority Order)

1. **Fix critical implementation gaps**
   - Implement actual aggregation in TypeScript folds
   - Implement subsumption check for finite domains

2. **Establish Agda-TS equivalence**
   - Golden tests comparing Agda evaluation to TS output
   - Fix semantic divergences

3. **Prove or downgrade conjectures**
   - Attempt fold idempotence proof for concrete implementations
   - Either prove Lyapunov or mark all dependent claims conjecture

4. **Sensitivity analysis**
   - Test threshold robustness for metabolic tension claims
   - Test across domain sizes

---

## Development Environment

- Node.js for TypeScript runtime
- Agda 2.6+ for formal verification
- Python 3 for visualization tools

## See Also

- `LIMITATIONS.md` - Full list of known gaps
- Individual repository `CLAUDE.md` files for development guides
