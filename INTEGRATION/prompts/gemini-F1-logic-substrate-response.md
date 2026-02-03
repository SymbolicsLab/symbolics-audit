# Gemini Response: F.1 Logic Substrate Survey

**Date received**: 2026-02-01
**Prompt file**: gemini-F1-logic-substrate-survey.md

---

## Executive Summary

For your formal theory of distinction and becoming, **Logic of First-Degree Entailment (FDE)** and its generalization into **Bilattices** are the correct theoretical successors to LP. They provide the necessary "Neither" value (gaps) and distinct "Both" value (gluts) required by your ontology.

For the Agda implementation (--safe --without-K), the most robust path is to formalize **Ginsberg/Fitting Bilattices**. This structure naturally separates the "Truth" ordering (entailment) from the "Knowledge" ordering (stabilization), providing a rigorous algebraic home for your "fold" operator. While FDE is the logic, the Bilattice L₄ is the structure that explains the mechanics of becoming.

---

## 1. Survey of Candidate Logics

### Primary Candidate: First-Degree Entailment (FDE)

**Key Reference**: Belnap, N. D. (1977). "A Useful Four-Valued Logic".

- **Ontology**: Four values: {T, F, B, N} (True, False, Both, Neither)
- **Structure**: A De Morgan Monoid or a Bilattice (L₄)
- **Designated Values**: {T, B} (preserves truth)
- **Negation**: Maps T↔F and fixes B, N

**Comparison to LP**: LP is FDE restricted to {T, F, B}. LP lacks N (the empty set/gap). LP validates B→T (Ex Falso allows "Both" to imply "True" in some formulations, though strict LP invalidates Modus Ponens). FDE is strictly weaker; it creates a symmetric independence between Gaps and Gluts.

**Relevance to "Fold"**: In FDE, the "Fold" operation corresponds to movement along the Knowledge Ordering (≤ₖ). N is the bottom (no info), B is the top (over-determined). Stabilization implies a flow from N→{T,F}→B or a resolution B→{T,F}.

### Constructive Option: Nelson's Paraconsistent Logic (N4)

**Key Reference**: Nelson, D. (1949); Wansing, H. (1993).

- **Ontology**: Constructive logic with Strong Negation (∼)
- **Structure**: A model is M = (W, ≤, v⁺, v⁻) where v⁺ verifies and v⁻ falsifies

**Why it fits**: It is natively constructive (intuitionistic base), making it highly compatible with Agda's type theory. It supports "gaps" (via intuitionistic negation) and "gluts" (via strong negation).

**Trade-off**: It is more complex than FDE. It introduces an accessibility relation (Kripke semantics) which may be overkill if you only need algebraic truth-functions.

### Structural Generalization: Bilattices

**Key Reference**: Ginsberg, M. L. (1988); Fitting, M. (1990).

**Concept**: A set equipped with two partial orders:

- **≤ₜ (Truth order)**: F ≤ₜ N, B ≤ₜ T (horizontal in Hasse diagram)
- **≤ₖ (Knowledge order)**: N ≤ₖ T, F ≤ₖ B (vertical in Hasse diagram)

**Why it fits**: This is the most promising substrate for "stabilization." Your "fold" operator can be rigorously defined as a closure operator or filter on the ≤ₖ axis.

---

## 2. Agda Implementation Landscape

### Current State of the Art

There is no "standard" library for paraconsistent logic in Agda, but the primitives are well-understood.

- **Finite Lattices**: Implementing FDE as a data type with 4 constructors is trivial
- **Algebraic Structures**: The agda-stdlib Algebra hierarchy (Lattices, Boolean Algebras) can be extended to De Morgan Algebras or Bilattices
- **Proof Relevance**: Under --without-K, you must be careful with equality. If your configurations are sets of formulas, you will need to use Setoid or Relation.Binary to handle equivalence, as you cannot rely on UIP (Uniqueness of Identity Proofs)

### Feasibility Assessment

| Logic | Agda Effort | Difficulty | Fit for "Fold" |
|-------|-------------|------------|----------------|
| FDE | Low | Easy | High (Direct mapping to requirements) |
| N4 | High | Hard | Medium (Requires Kripke structures/Setoids) |
| Bilattices | Medium | Moderate | Perfect (Captures the "stabilization" intuition) |

### Technical Plan for Agda

Define a Bilattice Structure class:

```agda
record Bilattice (A : Set) : Set where
  field
    -- Truth Lattice
    _∧_ : A → A → A
    _∨_ : A → A → A
    -- Knowledge Lattice
    _⊗_ : A → A → A  -- Consensus / Meet in k-order
    _⊕_ : A → A → A  -- Gullibility / Join in k-order
    -- Negation
    ¬_ : A → A
```

This structure allows you to prove the properties of fold abstractly.

---

## 3. Beyond Truth-Functional: The Dialogical/Topological Turn

### A. Game Semantics (Dialogical)

**Concept**: "Fold" is not a function, but an Equilibrium in a game between a "Verifier" and "Falsifier" (or "Stabilizer" and "Perturber").

**Agda Fit**: Agda is excellent for Game Semantics (using inductive families for Game/Strategy).

**Relevance**: In paraconsistent game semantics, a winning strategy for Player A does not imply the lack of a winning strategy for Player B. This models "Both" (gluts) as a state where both players have winning strategies.

**Fold**: fold(Φ) is the state where the game reaches a stable cycle or fixed point.

### B. Topological Semantics (Boundary Logic)

**Concept**: Use a topological space where "In" is the Interior, "Out" is the Exterior, and "Both" is the Boundary (∂S).

**Agda Fit**: Requires agda-topology or modeling neighborhood bases. Harder to mechanize than algebra.

**Relevance**: "Becoming" is often modeled as crossing a boundary. "Neither" is the whole space before a cut is made.

**Fold**: The topological boundary operator ∂ is not idempotent (∂∂S ≠ ∂S usually), but the Closure operator is. Fold is likely a Clopen operation or a regularization.

---

## 4. Specific Answers to Sub-Questions

### 1. Do the three fold properties hold for FDE entailment?

**Yes, but requires re-definition.** In LP, fold was "canonical normalization." In FDE, "canonical normal forms" exist (Conjunctive Normal Form where literals can be negated).

- **Idempotence**: Yes. Normalizing a normal form is identity.
- **Conservativity**: Yes. FDE normalization does not introduce new variables.
- **Contradiction-preservation**: Yes. (A ∧ ¬A) is a valid, irreducible term in FDE normal forms. It does not explode to B.

### 2. What is "canonical normalization" for FDE?

It is the transformation of a configuration into a **Prime Filter on the Bilattice**, or syntactically, into FDE-CNF (conjunction of disjunctions of literals {p, ¬p}). Unlike Classical Logic, p ∧ ¬p is not eliminated; it is a stable atom of the syntax.

### 3. Can dialogical fold be formalized?

**Yes.** You can define a game where a configuration Φ is a set of moves. fold is the strategy composition that eliminates "dominated strategies" (unstable moves). This is formalizable in Agda using Sized Types or coinductive records (Guarded Recursion) to handle the potential infinite play of "becoming."

### 4. What does topological necessity look like?

In paraconsistent topology, "Necessity" (□A) is often the Interior operator. However, paraconsistency usually requires "closed sets" (to allow overlap). If v(A) is a closed set, then v(A) ∩ v(¬A) (the boundary) can be non-empty.

### 5. Existing Agda Libraries?

There is no "drop-in" Paraconsistent Logic library. You will likely need to write the Bilattice module yourself. It is a standard weekend project for an intermediate Agda user.

---

## 5. Recommendations & Path Forward

### The Realistic Path

Do not jump straight to Game Semantics or Topology unless necessary. The algebraic structure of Bilattices (specifically L₄) is sufficient to solve the "Neither" problem and is easy to implement in Agda.

**Step 1 (Immediate)**: Implement Data.Bilattice in Agda. Define L₄ with its four values.

**Step 2 (The Operator)**: Redefine fold not as "LP normalization" but as an operation on the Knowledge-ordering of the bilattice.
- **Hypothesis**: fold pushes values from N (Neither) toward T/F (Decision) or B (Conflict).

**Step 3 (Entailment)**: Define entailment via the Truth-ordering (≤ₜ). Verify that fold respects ≤ₜ (monotonicity).

### Showstopper Warning

Since you use --without-K, be careful if you define configurations as Types rather than Sets (data). If a configuration is a Type A, "Equality" is isomorphism. You might need **Quotient Types (HITs in Cubical Agda)** to properly express "canonical normalization" (identifying equivalent configurations) without restricting yourself to decidable sets.

---

## Key References for Next Steps

1. **Fitting, M. (1990). "Bilattices and the theory of truth".** (The bible for this structure)
2. **Arieli, O., & Avron, A. (1996). "Reasoning with logical bilattices".** (Defines entailment rigorously)

---

## Sources (from Gemini)

- youtube.com, consequently.org, ufrn.br, nih.gov, arxiv.org, kdpu.edu.ua, github.io, nfshost.com, canbaskent.net, wikipedia.org, unicamp.br

### Suggested Follow-up Searches

- Agda implementation First Degree Entailment FDE
- bilattice logic formalization Agda
- topological semantics for paraconsistent logic
- canonical normalization FDE logic
- Nelson logic N4 Agda formalization
- game semantics paraconsistent logic Agda
