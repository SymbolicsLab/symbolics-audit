# Research Questions

**Date**: 2026-01-29
**Status**: Post-Phase 2.5 Ablation

This document tracks research questions that have emerged during the Symbolics project, organized by resolution status.

---

## Resolved Questions

### RQ-001: Are the TypeScript folds semantically equivalent to Agda?

**Status**: Resolved (Phase 2)

**Answer**: Yes, after Phase 2 fixes. The original implementation had placeholder semantics that diverged from Agda. Specifically:

| Operation | Placeholder | Canonical (Agda) |
|-----------|-------------|------------------|
| aggregate | `uniformCut(sideIn)` | `pointwiseJoin(context)` |
| subsumption | `return true` | `∀i. d(i) ≤ c(i)` |
| update | `[newCut, ...ctx]` | `add + remove subsumed` |

**Evidence**:
- 29 semantic equivalence tests pass
- 9 Agda grounding tests pass
- Reference evaluator cross-validation

**Location**: `symbolics-dsl/test/semantic-equivalence.test.ts`, `symbolics-dsl/test/agda-grounding.test.ts`

---

### RQ-002: Does the formal system exhibit sustained metabolic cycling?

**Status**: Resolved (Phase 2.5)

**Answer**: **No**, under current configuration with canonical semantics.

The "metabolic tension" result (22.5% with 3+ switches) was caused by placeholder fold implementations that injected artificial positive evidence at every step.

Under canonical semantics:
- Maximum switches observed: **2** (across all domain sizes tested)
- Runs with ≥3 switches: **0.0%**
- The 2-switch maximum is consistent across |U| = 5, 10, 15, 30

**Interpretation**: The system is conservative. After one conflict-resolution cycle, the system reaches a stable state. There is no sustained oscillation or "metabolic breathing" under current operators.

**Evidence**: `symbolics-dsl/experiments/canonical-tension/RESULTS.md`

---

### RQ-003: What is the correct identity element for empty aggregation?

**Status**: Resolved (Phase 2)

**Answer**: `mkSide Neither Res` (Neither/Res)

From Agda Context.agda:116-118:
```agda
joinAllRes [] = mkSide Neither Res
```

This is semantically important:
- `Neither` means "no information" (not negative information)
- `Out` would mean "definitely outside" (negative information)
- The identity must be the lattice bottom for join

**Impact**: All tests and implementations now use Neither/Res as identity.

---

### RQ-004: What ordering should subsumption use?

**Status**: Resolved (Phase 2)

**Answer**: Resolution order (≤ʳ), not knowledge order (≤ᵏ).

From Finite.agda:189-201:
- `sideOut` is bottom (≤ everything)
- `sideBoth` is top (only ≤ itself)
- `sideRem ≤ sideIn` but `sideIn ⊈ sideRem`

This differs from knowledge order where Both would be top for information content.

**Rationale**: Resolution order tracks "commitment" not "information". Out (no commitment) is below In (positive commitment).

---

## Open Questions

### RQ-005: Can legitimate novelty sources enable sustained dynamics?

**Status**: Open (Research Fork)

**Question**: If we add a principled mechanism for introducing new information, can the system exhibit sustained cycling without artificial forcing?

**Options Being Considered**:

1. **Evidence interface**: External observations that introduce new cuts
   - Must be formally constrained (conservativity)
   - Cannot be a hidden forcing function

2. **Unfold operator**: Expansion from compressed representations
   - Currently a stub in TypeScript
   - Agda has spec but no implementation

3. **Different decay mechanisms**: Alternative conflict resolution strategies
   - Current: drop-persistent-conflict
   - Alternatives: probabilistic decay, threshold-based

**Constraints**: Any novelty source must be:
- Formally specified in Agda
- Provably conservative (doesn't create information from nothing)
- Semantically meaningful (not just noise injection)

**See**: DESIGN-DECISIONS.md for implementation options

---

### RQ-006: What do the Lyapunov postulates actually guarantee?

**Status**: Open (Formal)

**Question**: The 7 postulates in `Mechanics.Potential.Conjectures` are unproven. What would proving them establish?

**Current Postulates**:
1. Potential is always non-negative
2. Potential decreases or stays constant on each step
3. Zero potential implies stability
4. Conflict increases potential
5. Resolution decreases potential
6. Potential bounded above
7. Step function is monotonic in potential

**Risk**: If these are false, the convergence guarantees don't hold.

**Path Forward**: Either prove these properties or find counterexamples.

---

### RQ-007: Is the 2-switch maximum a theorem or empirical observation?

**Status**: Open (Formal)

**Question**: We observed max 2 switches across 3368 runs and 4 domain sizes. Is this provable from the formal system?

**Hypothesis**: Under aggregate-only folds with drop-persistent-conflict decay, conflicts can:
1. Appear (In + Out → Both)
2. Resolve (decay drops one side)
3. Return once (if residual pressure)
4. Resolve permanently (no more pressure sources)

**Proof Strategy**: Show that after decay removes conflict, no operator can recreate it without external input.

**Blocking**: Depends on proving fold properties (SPEC-FOLD-002, SPEC-FOLD-003)

---

### RQ-008: What is the relationship between domain size and dynamics?

**Status**: Partially Resolved

**Observation**: Domain size affects mean switches but not maximum:

| Domain | Mean Switches | Max Switches |
|--------|---------------|--------------|
| |U|=5  | 0.79 | 2 |
| |U|=10 | 1.11 | 2 |
| |U|=15 | 1.16 | 2 |
| |U|=30 | 1.36 | 2 |

**Interpretation**: Larger domains have more opportunities for conflict but the resolution dynamics are the same. The maximum is structurally bounded, not statistically.

**Open**: Formal proof of why maximum is invariant to domain size.

---

### RQ-009: What role does the policy play?

**Status**: Open (Experimental)

**Question**: Current experiments use homeostatic policy. What happens with other policies?

**Homeostatic Policy**: Alternates stabilize/explore based on conflict level.

**Alternatives to Test**:
- Always-stabilize (no exploration)
- Always-explore (no stabilization)
- Threshold-based (only act above threshold)
- Random (coin flip each step)

**Hypothesis**: Policy affects path to stability but not final stability. Needs experimental verification.

---

## Methodology Questions

### RQ-M1: How do we prevent shared-bug risk?

**Status**: Addressed (Phase 2)

**Answer**: Three-layer validation:

1. **Reference evaluator**: Minimal Python-style implementation
2. **Agda grounding tests**: Values computed from Agda definitions
3. **Semantic equivalence tests**: Runtime vs reference comparison

If all three agree and match Agda, shared-bug risk is minimized.

---

### RQ-M2: How do we distinguish artifact from phenomenon?

**Status**: Addressed (Phase 2.5)

**Answer**: Ablation studies with placeholder vs canonical semantics.

The 22.5% "metabolic tension" was an artifact because:
- It disappeared under canonical semantics
- It was caused by placeholder code injecting artificial evidence
- The effect was implementation-dependent, not system-dependent

**Lesson**: Always verify emergent phenomena survive implementation fixes.

---

## Archive (Superseded)

### RQ-A1: Is the 22.5% metabolic tension rate significant?

**Status**: Superseded by RQ-002

**Original Question**: Does 22.5% of runs with 3+ switches indicate emergent metabolism?

**Resolution**: The 22.5% was an artifact. Under canonical semantics, 0% of runs have 3+ switches.

---

## See Also

- `PROJECT-STATUS.md` - Current project state
- `LIMITATIONS.md` - Known gaps and their status
- `DESIGN-DECISIONS.md` - Pending architectural decisions
- `experiments/canonical-tension/RESULTS.md` - Ablation study data
