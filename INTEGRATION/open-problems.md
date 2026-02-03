# Symbolics: Open Problem Registry
**Version**: 0.1.0 | **Date**: 2026-01-31 | **Status**: Initial Draft

Each problem has:
- **ID**: Type prefix + number (F=Foundational, S=Structural, C=Connective, T=Technical, X=Critical)
- **Status**: Unexplored | Under Investigation | Proposed Resolution | Resolved
- **Priority**: How much downstream work depends on this
- **Blocking**: What this problem blocks if unresolved

---

## FOUNDATIONAL PROBLEMS
*These affect the entire theory. Resolving them may require restructuring.*

### F.1 — The Logic Substrate
**Status**: Under Investigation | **Priority**: HIGHEST

**Problem**: The theory's ontology uses four truth values (Neither/In/Out/Both = Belnap's FDE), but the fold proofs operate over LP (three designated values). The user suspects even FDE may be insufficient—that truth-functional logics oversimplify what the theory actually needs.

**Why it matters**: Every verified proof depends on the choice of underlying logic. If LP is too narrow, the proofs cover only a fragment of what the theory claims. If FDE is also wrong, the formal core may need rebuilding on a different substrate.

**Sub-questions**:
1. Do the three fold properties (idempotence, conservativity, contradiction-preservation) hold over FDE entailment? If not, what changes?
2. Is truth-functional logic sufficient for the theory's needs, or does it require something inherently dynamic (topological, spatial, intensional)?
3. What would "topological necessity" look like formally? Can Agda express it? (Cubical Agda gives actual paths and homotopies—is this relevant?)
4. The UNILOG script says canonical normalization is "the coarsest map that preserves exactly what the logic is sensitive to." If the right logic isn't LP, the right fold isn't LP-fold. What is it?
5. The theory uses --without-K (rejecting uniqueness of identity proofs). This is already a step toward homotopy type theory. How far should this go?

**Approach**: 
- Phase 1: Check whether fold properties hold for FDE. This is a concrete proof obligation.
- Phase 2: Investigate what the theory *needs* from a logic. Map the theory's demands (pressure, becoming, levels, reentry) against what different logics provide.
- Phase 3: If truth-functional is insufficient, identify candidate substrates (FDE with gaps, relevance logics, topological semantics, cubical type theory) and assess feasibility.

**Blocking**: Everything. All formal work downstream inherits this choice.

---

### F.2 — What Is Pressure Formally?
**Status**: Unexplored | **Priority**: High

**Problem**: Pressure is theoretically central (drives unfold, precedes distinction at Level 0, is the engine of becoming) but formally underspecified. The Agda encodes it as binary (Res/Unres). The theory describes it as something more like a continuous scalar or field.

**Sub-questions**:
1. Is pressure a scalar quantity? A field? A type? Something else?
2. Does pressure admit gradation, or is binary (resolved/unresolved) actually correct?
3. What is the formal relationship between pressure and the `Neither` truth value? Both represent "no polarity commitment"—but are they the same thing?
4. The Synthesis says "pressure is not a single quantity but a structural feature: the remainder that any stabilization leaves." If pressure IS remainder, should they be unified?

**Blocking**: Unfold formalization (F.3), metabolism formalization, Lyapunov conjectures, physics connections.

---

### F.3 — Unfold: What Is It?
**Status**: Unexplored | **Priority**: High

**Problem**: Unfold is half the metabolism but has no formal implementation. The Synthesis specifies `unfold : Field × Press → Form × Press`, but Field and Press are not defined in the Agda. The user reports unfold is "least intuitive."

**Sub-questions**:
1. What are the formal types of Field and Press?
2. Is unfold a single operation or a family of level-specific operations? (The Synthesis lists different realizations at each level.)
3. What would a minimal unfold look like? Start with the simplest version that could be formalized.
4. Unfold properties (non-idempotent, pressure-monotone, remainder-feeding): are these the right properties? Are there others?
5. The metabolic tick is `fold ∘ unfold`. Does order matter? The Synthesis claims commutation up to remainder. This would be a significant theorem if proven.

**Blocking**: Metabolism formalization, regime characterization, creative dynamics, most applications.

---

### F.4 — The Designation Question
**Status**: Unexplored | **Priority**: Medium-High

**Problem**: LP designates Both (contradictions are "true enough" to be consequential). FDE does not designate Both by default. The theory needs contradictions to be preserved *and* consequential. Which designation scheme is correct?

**Why it matters**: Designation determines what counts as a valid conclusion. If Both is designated, contradictions drive inference. If not, contradictions are inert. The theory needs a middle ground: contradictions that persist and exert pressure without exploding.

**Blocking**: All fold proofs (they assume LP designation). Logic substrate decision (F.1).

---

## STRUCTURAL PROBLEMS
*These affect the architecture of the theory but not its foundations.*

### S.1 — Level Transitions: How Does Organizational Ascent Work?
**Status**: Unexplored | **Priority**: High

**Problem**: The organizational hierarchy has levels -2 through 6, and the theory claims each level arises from reapplying distinction at a different scope. But the *mechanism* of transition from Level n to Level n+1 is not formalized.

**Sub-questions**:
1. What is the type signature of a level transition?
2. Is reentry the mechanism? If so, what formally happens when "a distinction applies to itself"?
3. The Agda has type composition (U → Cut U → Fold), giving ~3 levels. Can this extend to all levels through iteration?
4. Does each level transition require new formal machinery, or can it be uniform?

**Blocking**: Formalization of anything above Level 2. Plasticity proofs. Self model.

---

### S.2 — The Inverted Filter: Formalizing Top-Down Constraint
**Status**: Draft stage | **Priority**: Medium-High

**Problem**: The hierarchy is bidirectional (bottom-up construction + top-down constraint), but only bottom-up is implicit in the Agda. The filter equation (F₋₁ ∝ S₅ / Tolerance(P)) is informal.

**Sub-questions**:
1. Can top-down constraint be modeled as a parametrized fold? (Higher levels set the parameters for lower-level folds.)
2. What types do F₋₁, S₅, Tolerance, P have?
3. The "complete circuit" (Synthesis §12.5.7) is a diagram. Can it be a formal structure?

**Blocking**: Phenomenological applications, pathology models, politics of filter capture, confirmation bias formalization.

---

### S.3 — What Is a Regime Formally?
**Status**: Unexplored | **Priority**: Medium

**Problem**: Three metabolic regimes (creative: unfold > fold; homeostatic: balanced; crystalline: fold > unfold) are described but not formally defined. What metric determines regime? What are the boundaries?

**Sub-questions**:
1. Is regime determined by a ratio? A threshold? Something else?
2. The DSL uses a `regime` parameter with `lo` and `hi` bounds. Is this the right formalization?
3. "Two deaths" (dissolution, crystallization) are the endpoints. What formally characterizes death?
4. The Lyapunov conjectures (6 postulates in `Conjectures.agda`) attempt to formalize regime dynamics. Are they on the right track?

**Blocking**: Dynamics, empirical predictions about regime behavior, educational applications.

---

### S.4 — Multi-Agent / Social Extension
**Status**: Unexplored | **Priority**: Medium

**Problem**: The theory extends to social systems (institutions, cultures, collective contradiction) but the formalism is single-agent. Multi-agent dynamics (shared configurations, conflicting folds, power asymmetry) are not formalized.

**Sub-questions**:
1. What happens when two agents with different folds interact?
2. Can institutions be modeled as shared fold operators? What constrains them?
3. The Synthesis discusses "power as asymmetric access to others' fold." Can this be formalized?

**Blocking**: Social applications, politics of imposed stabilization, institutional diagnosis.

---

### S.5 — The Fold Taxonomy
**Status**: Draft stage | **Priority**: Medium

**Problem**: There are many "folds" in the theory: LP-fold (canonical normalization), attention-fold (perception), identity-fold (self-model maintenance), institutional fold. Are these instances of one thing or a family?

**Sub-questions**:
1. Is there a *general* fold type of which LP-fold, attention-fold, etc. are instances?
2. What properties must any fold satisfy to count as a fold? (Idempotence? Conservativity? Both?)
3. The UNILOG script suggests: "Different logics → different normalizations → different folds." This implies fold is parameterized by logic. But the theory also claims fold *precedes* logic.

**Blocking**: Clarity about what fold *means* across levels and domains.

---

## CONNECTIVE PROBLEMS
*These link the theory to external domains and traditions.*

### C.1 — FEP Dual: Is Symbolics the Symbolic Free Energy Principle?
**Status**: Unexplored | **Priority**: Medium-High

**Problem**: A previous conversation identified the possibility that symbolics is the "symbolic dual of the Free Energy Principle." The structural parallel: FEP says systems minimize surprise/free energy; symbolics says systems minimize commitment instability. Both describe organisms/agents that stabilize under pressure, with remainder/prediction error driving the next cycle.

**Sub-questions**:
1. Is this a formal duality (in the category-theoretic sense) or a structural analogy?
2. FEP uses variational inference and Markov blankets. Symbolics uses fold and configurations. Can a precise mapping be constructed?
3. FEP operates on continuous probability distributions. Symbolics operates on finite discrete configurations. Is there a continuous generalization of fold?
4. FEP has active inference (the organism acts on the world to reduce surprise). Symbolics has... what? Unfold? Policy-level action?
5. If this is a genuine duality, it would mean symbolics provides the *logical/symbolic* complement to FEP's *statistical/physical* account. This would be significant.

**Blocking**: Physics connections, grounding of pressure concept, continuous generalization.

---

### C.2 — Quantum Mechanics: Structural Resonance or Formal Connection?
**Status**: Unexplored | **Priority**: Medium

**Problem**: Multiple points of contact between symbolics and quantum mechanics:
- Cut ↔ Measurement (selective stabilization of undifferentiated field)
- Superposition ↔ Pre-cut multiplicity
- Decoherence ↔ Fold (stabilization)
- Interference/shimmer ↔ Remainder
- Observer effect ↔ Reentry

The Physics abstract makes a structural (not reductive) claim. But is there a formal connection?

**Sub-questions**:
1. Is there a precise mathematical relationship between fold operators and measurement operators in quantum theory?
2. Does decoherence have formal properties that mirror idempotence, conservativity, contradiction-preservation?
3. The Synthesis places quantum field at Level -2. Is this a genuine embedding or just a label?
4. Cubical type theory (potential substrate for F.1) has connections to quantum computing. Does this create a bridge?

**Blocking**: Physics applications, empirical predictions about bistable perception, grounding of Level -2.

---

### C.3 — Category Theory: The Right Language?
**Status**: Unexplored | **Priority**: Medium

**Problem**: The Synthesis and open problems repeatedly mention category-theoretic formulation. Fold as functor? Reentry as natural transformation? The metabolism as adjunction?

**Sub-questions**:
1. Is fold a functor? If so, from what category to what category?
2. Are fold and unfold adjoint? (Left adjoint produces, right adjoint preserves—this would be clean.)
3. Could the organizational hierarchy be a tower of categories with level transitions as functors?
4. Is there an existing categorical treatment of paraconsistent logic that symbolics could use?

**Blocking**: Formal elegance, connections to other mathematical frameworks, potential simplification of proofs.

---

### C.4 — Phenomenological Tradition: Where Does Symbolics Sit?
**Status**: Partially developed | **Priority**: Low-Medium

**Problem**: The theory engages Husserl, Merleau-Ponty, Heidegger, Bergson, Deleuze, Malabou. The NTNU, York, and Konstanz abstracts develop specific connections. But the theory's relationship to phenomenology as a tradition is not fully articulated.

**Scattered Insights**:
- The theory agrees with phenomenology that experience has structure.
- It disagrees with the need for a transcendental subject.
- It offers formalization where phenomenology offers description.
- "Shimmer" is a phenomenological concept with potential formal correlate.

---

### C.5 — Post-Hegelian Positioning: Is the Settlement Stable?
**Status**: Developed in Synthesis | **Priority**: Low-Medium

**Problem**: Chapter 19 of the Synthesis argues for fold over Aufhebung, remainder over negation, fixed points over Absolute. This is philosophically developed but could face objections.

**Sub-questions**:
1. A Hegelian might respond: "Your fold-stable states with remainder are just Hegel's determinate negation, arrested prematurely." How to respond?
2. Is the claim that contradiction *never* synthesizes too strong? Sometimes contradictions do resolve.

---

## TECHNICAL PROBLEMS
*Specific formalization challenges.*

### T.1 — FDE Fold Properties
**Status**: Unexplored | **Priority**: High (contingent on F.1)

**Problem**: Prove or disprove: idempotence, conservativity, and contradiction-preservation hold for fold defined over FDE entailment rather than LP entailment.

---

### T.2 — Lyapunov Conjectures
**Status**: Conjectural | **Priority**: Medium

**Problem**: 6 postulates in `Conjectures.agda` about potential dynamics. The master conjecture: potential is a Lyapunov function (non-increasing under step). All currently `postulate` (unsafe).

---

### T.3 — DSL/Agda Alignment
**Status**: Known gap | **Priority**: Medium

**Problem**: DSL fold implementations are placeholders that don't match Agda semantics. Subsumption check always returns true. No Agda→TS code generation exists.

---

### T.4 — Transition Relation Generalization
**Status**: Unexplored | **Priority**: Medium

**Problem**: Current transition adds exactly one formula per step (License₁). The theory describes larger perturbations. Should the transition relation be generalized?

---

## CRITICAL / META PROBLEMS
*Potential failure modes of the theory itself.*

### X.1 — Is This One Theory or Several?
**Status**: Unexplored | **Priority**: High

**Problem**: Symbolics covers logic, phenomenology, AI, culture, physics, ethics, social ontology. Is this genuine unification or overreach? How do we tell the difference?

**Diagnostic**: If applications in different domains produce *different* insights using the same structure, it's unification. If they produce *the same* insight rebranded, it might be a hammer looking for nails.

---

### X.2 — Falsifiability
**Status**: Partially addressed | **Priority**: High

**Problem**: The Synthesis identifies testable predictions. But are they genuinely risky? Could the theory accommodate any outcome?

**Key predictions to track**:
1. □φ/φ dissociation is behaviorally measurable
2. Benchmark displacement requires value-level intervention
3. LLM behavior shows bimodal regime structure (partially confirmed by Two Regimes data)
4. Alignment failures cluster into value-level and policy-level types
5. Insight shows metabolic phenomenological structure

---

### X.3 — The Theory's Own Metabolism
**Status**: Unexplored | **Priority**: Meta

**Problem**: If the theory is correct, it should apply to itself. What is symbolics' own metabolic regime? Is it crystallizing (over-stabilizing core claims) or maintaining homeostasis (generating new questions)? Is there remainder the theory isn't processing?

---

### X.4 — What Does the Theory Predict That No Other Theory Predicts?
**Status**: Partially addressed | **Priority**: High

**Problem**: For the theory to be more than redescription, it needs to predict something no rival framework predicts. The Synthesis lists predictions, but:
1. Are any of these *unique* to symbolics? Or could FEP, dialectics, predictive processing, or enactivism make the same predictions?
2. What is the *signature* prediction that only this theory makes?

---

## DEPENDENCY GRAPH

```
F.1 (Logic Substrate) ←── blocks ──→ ALL FORMAL WORK
  ├── T.1 (FDE properties)
  ├── F.4 (Designation)
  └── S.5 (Fold taxonomy)

F.2 (Pressure) ←── blocks ──→ F.3 (Unfold)
F.3 (Unfold) ←── blocks ──→ Metabolism formalization
                              ├── S.3 (Regimes)
                              ├── T.2 (Lyapunov)
                              └── All dynamic applications

S.1 (Level Transitions) ←── blocks ──→ S.2 (Inverted Filter)
                                        ├── Plasticity proofs
                                        └── Level 3+ formalization

C.1 (FEP Dual) ←── informs ──→ F.2 (Pressure)
C.2 (QM) ←── informs ──→ F.1 (Logic Substrate)
C.3 (Category Theory) ←── informs ──→ F.3 (Unfold), S.1 (Level Transitions)
```

---

## PRIORITY SEQUENCE

**Immediate** (weeks):
1. F.1 — Investigate logic substrate. At minimum, check whether fold properties hold for FDE.
2. Completeness Map review — ensure all scattered insights are captured and routed.
3. Vault hygiene — promote key drafts, create missing notes (Phenomenon, Shimmer, Side).

**Near-term** (months):
4. F.3 — Develop unfold specification. Start with minimal formal characterization.
5. F.2 — Clarify pressure. Determine if binary is sufficient or gradation needed.
6. S.1 — Investigate level transitions. Can the type structure extend?
7. T.3 — Fix DSL/Agda alignment. At minimum, make DSL fold match Agda fold.

**Medium-term**:
8. C.1 — FEP dual investigation. Literature review + structural comparison.
9. C.3 — Category-theoretic exploration. Is fold a functor? Are fold/unfold adjoint?
10. S.2 — Formalize inverted filter.
11. T.1 — Prove FDE fold properties (if F.1 resolves toward FDE).

**Long-term**:
12. S.4 — Multi-agent extension.
13. C.2 — Quantum mechanics connection.
14. Empirical work on predictions.
