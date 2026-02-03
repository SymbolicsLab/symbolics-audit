# Gemini Prompt: F.1 Logic Substrate Survey

**Purpose**: Literature survey and feasibility assessment for logic substrate options
**Context**: Formal theory research project using Agda (--safe --without-K)
**Date generated**: 2026-02-01

---

## The Question

I'm developing a formal theory that requires a specific logical substrate. I need help surveying the options and assessing their feasibility for implementation in Agda.

**Core requirements for the logic:**

1. **Contradiction-preservation (paraconsistency)**: Both +a and -a can coexist in a configuration without explosion. The logic must not be explosive—contradiction does not entail everything.

2. **Four truth values**: The theory's ontology uses Neither (no commitment), In (+a only), Out (-a only), and Both (+a and -a). This matches Belnap's FDE (First-Degree Entailment).

3. **Support for a "fold" operation**: A stabilization operator on configurations that satisfies:
   - Idempotence: fold(fold(Φ)) = fold(Φ)
   - Conservativity: atoms(fold(Φ)) ⊆ atoms(Φ)
   - Contradiction-preservation: +a and -a can coexist in fold(Φ)

4. **Agda implementability**: The logic must be implementable in Agda under --safe --without-K (no postulates, no type-in-type, compatible with proof-relevant / homotopy-aware foundations).

**Current state**: We have working Agda proofs for a fold operator over LP (Logic of Paradox, three designated values). The three properties above are verified. But LP may be too narrow—the theory describes four-valued FDE behavior, and there's a deeper question about whether truth-functional logic is sufficient at all.

---

## Background: The Problem in Detail

### Why LP might be insufficient

LP designates three values: True, False, and Both. It does not have a "Neither" value (gaps). The theory I'm formalizing uses all four Belnap values:

| Value | Meaning | LP has it? |
|-------|---------|------------|
| Neither | No polarity commitment | No |
| In | Positive commitment only | Yes (True) |
| Out | Negative commitment only | Yes (False) |
| Both | Contradictory commitment | Yes (Both) |

Without "Neither," LP cannot represent states where a proposition is simply not yet in play—neither asserted nor denied. This matters because the theory describes a process of *becoming* where commitments emerge from an undifferentiated field.

### Why even FDE might be insufficient

A recent theoretical development suggests the fold operation may be inherently *dialogical*—not a single operator acting on a single configuration, but an interaction between two configurations (or two aspects of one configuration) that mutually constrain each other.

If this is right, the question isn't just "LP vs FDE" but whether any truth-functional logic captures what fold actually does. The fold might require:
- A relational or game-theoretic semantics
- A topological or spatial notion of necessity
- Something that treats stabilization as emergent from interaction rather than computed by a function

The theory already uses --without-K in Agda (rejecting uniqueness of identity proofs), which is a step toward homotopy type theory. There may be connections to cubical type theory's paths and homotopies.

### What "canonical normalization" means

In the current LP formalization, fold is defined as "canonical normalization"—the coarsest equivalence that preserves exactly what LP entailment is sensitive to. Two configurations are fold-equivalent if they entail the same things under LP.

If the right logic isn't LP, the right fold isn't LP-fold. The question is: what *is* it?

---

## What I Need From You

### 1. Survey of candidate logics

Please identify logics that meet the core requirements (paraconsistent, non-explosive, supports gaps and gluts). For each, provide:

- Name and key references
- Truth values / semantic structure
- How it handles contradiction (designated values, entailment)
- Whether it has been formalized in Agda or similar proof assistants
- Key differences from LP and FDE

Candidates I'm aware of but need more information on:
- FDE (First-Degree Entailment) — Belnap, Dunn
- Relevant logics (R, E, T) — Anderson, Belnap
- Nelson's logics (N3, N4) — constructive paraconsistency
- Bilattice-based logics — Ginsberg, Fitting
- Many-valued logics with designated value sets

### 2. Agda implementation landscape

What paraconsistent or many-valued logics have actually been implemented in Agda or Coq? Are there libraries I should look at? What are the main technical challenges?

Specific questions:
- Has anyone implemented FDE entailment in Agda?
- Are there Agda formalizations of relevant logic?
- How do bilattice structures work in dependent type theory?
- Are there connections to cubical Agda that might be relevant?

### 3. Beyond truth-functional: alternative substrates

If truth-functional logic is insufficient, what are the options?

- **Topological semantics**: Can "necessity" be defined topologically (interior operator)? Is this implementable in Agda?
- **Game-theoretic semantics**: Can fold be modeled as equilibrium in a dialogue game? Any Agda work on this?
- **Categorical semantics**: Is there a category-theoretic treatment of paraconsistent logic that might provide a cleaner formalization?
- **Cubical type theory**: Does the path structure in cubical Agda offer resources for representing the "dialogical" nature of fold?

### 4. Assessment: what's realistic?

Given that:
- We need Agda implementation (--safe --without-K)
- We have working LP proofs as a baseline
- The theory may require more than truth-functional logic

What's the most promising path forward? Options might include:
- Extend current LP proofs to FDE (conservative, may not be enough)
- Adopt a bilattice framework (more general, unclear Agda support)
- Move to relevant logic (richer, may be overkill)
- Explore topological/categorical alternatives (ambitious, may be necessary)

---

## Specific Sub-questions

1. **Do the three fold properties (idempotence, conservativity, contradiction-preservation) hold for FDE entailment?** This is a concrete proof obligation. If they fail, what changes?

2. **What is "canonical normalization" for FDE?** LP-fold is "the coarsest map that preserves LP entailment." What's the analogous notion for FDE?

3. **Can dialogical fold be formalized?** If fold is inherently bi-directional (two configurations interacting), what formal framework captures this? Game semantics? Dialogue logic? Something else?

4. **What does topological necessity look like formally?** The theory uses --without-K, suggesting some affinity with homotopy type theory. Is there a topological treatment of paraconsistent modality?

5. **Are there existing Agda libraries for paraconsistent logic?** Even partial implementations would be helpful starting points.

---

## Deliverable

I'm looking for a structured survey that:
1. Maps the landscape of candidate logics
2. Assesses Agda implementability for each
3. Identifies the most promising paths forward
4. Flags any showstoppers or major technical challenges
5. Provides key references for deeper investigation

This will inform a decision that blocks all downstream formal work, so thoroughness matters more than speed.

---

## Additional Context

The broader project is a formal theory of distinction, stabilization, and becoming. The fold operator is half of a "metabolism" (fold + unfold) that explains how symbolic systems persist through time while remaining capable of change. The logic substrate must support:

- Contradictions that persist productively (not explode, not disappear)
- Gaps (uncommitted propositions) as well as gluts (contradictions)
- A notion of stabilization that is idempotent and conservative
- Eventually: an "unfold" operator that re-opens configuration space

The theory has applications in philosophy of mind, AI alignment, and formal epistemology, but the immediate need is getting the foundations right.
