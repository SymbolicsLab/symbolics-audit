# Conjecture: Switch Bound Under Canonical Semantics

**ID**: CONJ-SWITCH-001
**Status**: Open
**Date**: 2026-01-29
**Related**: RQ-007, DD-001

## Statement

Under the following conditions:
1. Finite domain U with |U| = n
2. Aggregate = pointwise join (canonical, conservative)
3. Decay = subsumption-based pruning (removes subsumed cuts)
4. Policy = homeostatic (deterministic given pressure bands)
5. No external evidence injection
6. No unfold operator (or unfold is conservative)

The conflict indicator (number of elements with `Both` truth value) can change sign
(conflict appears or disappears) at most K times before the system reaches
a fixed point or monotone region.

**Formal Statement** (to be proven in Agda):
```agda
switch-bound :
  (sys : FiniteSystem U) (lo hi : ℕ) (fold : Fold U) (ctx₀ : Context U)
  → ∃ λ (K : ℕ) →
    ∀ (trace : Trajectory sys lo hi fold ctx₀) →
      switchCount trace ≤ K
```

## Empirical Evidence

From canonical-tension experiments (symbolics-dsl):

| Domain | Runs | Max Switches | Mean Switches | ≥2 Switches | ≥3 Switches |
|--------|------|--------------|---------------|-------------|-------------|
| |U|=5  | 239  | 2            | 0.79          | 28.8%       | 0%          |
| |U|=10 | 319  | 2            | 1.11          | 46.0%       | 0%          |
| |U|=15 | 2249 | 2            | 1.16          | 39.2%       | 0%          |
| |U|=30 | 559  | 2            | 1.36          | 51.5%       | 0%          |

**Key observation**: No run in 3368 trials achieved ≥3 switches.

The maximum of 2 is consistent across all domain sizes tested, suggesting a structural bound rather than a statistical artifact.

## Proof Strategy (Sketch)

### Why switches might be bounded:

1. **Aggregate is conservative**:
   - `joinAllRes` computes pointwise join over all cuts
   - Cannot introduce new In/Out support that wasn't already present
   - `In ⊔ᵗ Out = Both` creates conflict, but only if both exist

2. **Context is finite**:
   - Bounded number of cuts, each over finite domain
   - Total state space is finite (though exponential)

3. **Decay is monotone-ish**:
   - `update` removes subsumed cuts via `removeSubsumed`
   - Context size is bounded by subsumption pruning
   - Existing proof attempt in `DecayLemmas-legacy.agda:221-299`

4. **Policy is deterministic**:
   - Same state → same action (Stabilize/Explore/Decay)
   - No external randomness

### Potential approach:

Define a measure M(C) over contexts such that:
- M decreases (or doesn't increase) on most transitions
- Conflict changes require M to change in specific ways
- Bounded M → bounded conflict changes

**Candidate measures**:
1. Lyapunov potential (existing in `Mechanics.Potential`): `(lo ∸ mass) + (mass ∸ hi)`
2. Context size (number of cuts)
3. Aggregate complexity (number of Both/Unres elements)
4. Combined measure: potential × context size

### Key lemmas needed:

1. **Aggregate monotonicity** (partial proof exists):
   ```agda
   aggregate-monotone : ∀ ctx c → aggregate (update ctx c) ⊒ aggregate ctx
   ```
   Proof attempt in `DecayLemmas-legacy.agda` but incomplete.

2. **Conflict creation requires divergent cuts**:
   ```agda
   conflict-creation : ∀ ctx u →
     aggregate ctx u ≡ Both →
     ∃ c₁ c₂ ∈ ctx. c₁(u) ≡ In ∧ c₂(u) ≡ Out
   ```

3. **Decay removes conflict sources**:
   ```agda
   decay-removes-conflict-source : ∀ ctx c →
     c(u) ∈ {In, Out} →
     c ∈ ctx →
     ∃ d ∈ (update ctx c'). d(u) ≡ c(u)  -- or c was subsumed
   ```

4. **After conflict resolves, no regeneration**:
   ```agda
   no-conflict-regeneration : ∀ ctx₀ →
     (∃ step. aggregate (iterate step ctx₀) u ≡ Both) →
     (∃ step'. aggregate (iterate step' ctx₀) u ≢ Both) →
     ∀ step'' > step'. aggregate (iterate step'' ctx₀) u ≢ Both
   ```
   This is the core claim: once conflict resolves, it can't return.

## What Exists in Agda

### Proven (safe, no postulates):
- Belnap four-valued logic encoding (`mkTruth`)
- Side lattice operations (`_⊔ˢ_`, `_⊓ˢ_`)
- Empty aggregate identity: `joinAllRes [] = mkSide Neither Res`
- Conflict preservation: `In ⊔ᵗ Out = Both`
- Resolution order: `sideOut ≤ anything`, `sideBoth ≤ only itself`

### Postulated (conjectures):
From `Mechanics.Potential.Conjectures`:
1. `potential-zero-iff-in-window` (both directions)
2. `stabilize-reduces-potential-above`
3. `explore-maintains-potential-below`
4. `adaptive-step-bounds-potential`
5. `convergence-to-equilibrium`
6. `potential-is-lyapunov` (master conjecture)

### Partial proofs (legacy/incomplete):
From `Mechanics.Archive.DecayLemmas-legacy`:
- `joinAllRes-monotone` (lines 221-225)
- `aggregate-monotone-helper` (lines 269-299)

## Gap Analysis

### What's needed for switch-bound:

1. **Define switchCount formally**:
   ```agda
   switchCount : Trajectory → ℕ
   switchCount = count transitions where conflict indicator changes
   ```

2. **Connect to existing potential machinery**:
   - If potential is Lyapunov, then potential changes are bounded
   - Need: conflict changes ≤ f(potential changes)

3. **Prove or disprove the master conjecture**:
   `potential-is-lyapunov` would imply bounded potential changes, which may imply bounded switches.

4. **Alternative approach if Lyapunov fails**:
   - Use context size as the measure
   - Prove: subsumption pruning bounds context growth
   - Prove: bounded context → bounded conflict oscillations

## Status Checklist

- [ ] Formalize `switchCount` in Agda
- [ ] Formalize the conjecture statement
- [ ] Connect to existing Lyapunov machinery
- [ ] Attempt proof of aggregate-monotone (complete partial proof)
- [ ] Identify the right measure/order
- [ ] Prove or find counterexample
- [ ] If proven, extract K as a function of system parameters

## Alternative Hypothesis

If the conjecture is FALSE:

The switch bound fails under [specific conditions]. Characterize when cycling is possible:
- Non-deterministic policy?
- Unfold that adds genuinely new cuts?
- External evidence injection?
- Specific fold behaviors?

Either outcome is valuable:
- **Proven**: System is inherently stable; metabolism requires additional structure
- **Disproven**: Characterizes the conditions for genuine cycling

## References

- `symbolics-core/src/Mechanics/Potential/Conjectures.agda` - Lyapunov postulates
- `symbolics-core/src/Mechanics/Archive/DecayLemmas-legacy.agda` - Partial monotonicity proofs
- `symbolics-dsl/experiments/canonical-tension/RESULTS.md` - Empirical evidence
- `symbolics-audit/RESEARCH-QUESTIONS.md` RQ-007 - Is this a theorem?
