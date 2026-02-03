# Gemini Prompt: Pre-propositional Formalization Literature

**Purpose**: Focused literature reconnaissance for ADR-002
**Context**: Formalizing Levels -1/0/1 (pre-cut field, act of distinction, immediate polarity)
**Date generated**: 2026-02-01

---

## Background

I'm working on a formal theory where **distinction is primitive**—logic is generated *by* distinction, not the other way around. I have working Agda proofs for what happens *after* atoms exist (stabilization, fold properties), but the act that *creates* atoms is unformalized.

The key insight: **cut cannot be a function from a fixed type to itself**, because it changes what exists. The type of the output is not the type of the input. Any formalization that makes cut `A → A` has already missed the point.

I need focused literature on two specific topics that might help.

---

## Topic 1: Spencer-Brown's Laws of Form

George Spencer-Brown's *Laws of Form* (1969) develops a "calculus of distinctions" that seems directly relevant. The key concepts:

- **The unmarked state**: the condition before any distinction is made
- **The mark**: the act of distinction (drawing a boundary)
- **Cross**: entering or leaving a marked space
- **Call**: the name of a distinction

### Questions for Gemini

1. **How has Laws of Form been formalized?** Are there type-theoretic, proof-assistant, or categorical treatments? I'm specifically interested in:
   - Any Agda, Coq, or Lean implementations
   - Category-theoretic interpretations
   - Connections to Boolean algebra or logic

2. **What is the "unmarked state" formally?** Spencer-Brown treats it as the background from which all distinctions emerge. Has anyone given this a rigorous mathematical definition? Is it:
   - The empty set? (Seems wrong—it's described as "full" not "empty")
   - A universal set? (Has paradox issues)
   - Something topological? (The whole space before partition?)
   - An initial object in some category?

3. **How does the mark relate to dependent types?** The mark "creates" a distinction that didn't exist before. This sounds like it might require dependent types where the output type depends on the act. Has anyone made this connection?

4. **Key papers or formalizations** to look at? I'm aware of:
   - Varela's work extending Spencer-Brown
   - Kauffman's reformulations
   - But I don't know the type-theoretic literature

---

## Topic 2: Initial Objects in Category Theory

The **initial object** in a category has a unique morphism to every other object. This might model how the pre-cut field "becomes" any particular cut—there's exactly one way to go from "undifferentiated" to any specific distinction.

### Questions for Gemini

1. **Can the pre-cut field be modeled as an initial object?** If so:
   - What category are we in?
   - Are cuts the morphisms from the initial object?
   - How does this handle the fact that multiple cuts are possible? (Initial object has *unique* morphism to each object, but we want *multiple* possible cuts)

2. **The "walking arrow"**: The simplest category with a morphism (two objects, one arrow). Is this relevant? It's the minimal structure that has a distinction (domain vs codomain).

3. **Universal properties and distinction**: Does the universal property of initial objects (unique morphism out) capture anything about how distinction works? Or is it too strong?

4. **Comonads and cofree structures**: I've seen suggestions that the "before" state might be cofree or final rather than initial. Any literature on this?

---

## What I'm Looking For

Not a general survey—I need **specific, citable sources** that:

1. Formalize Spencer-Brown in a way compatible with type theory or proof assistants
2. Connect the "unmarked state" to a rigorous mathematical object
3. Use initial objects or universal properties to model "before distinction"
4. Address the type signature problem: how to formalize an operation that changes what types exist

---

## Constraints

The formalization must eventually work in **Agda under --safe --without-K**. This means:
- No postulates
- No uniqueness of identity proofs (UIP)
- Compatible with proof-relevant / homotopy-aware foundations

So I'm especially interested in anything that connects Spencer-Brown or categorical initial objects to:
- Homotopy type theory
- Cubical type theory
- Dependent type theory generally

---

## Deliverable

Please provide:

1. **Spencer-Brown formalizations**: Any papers, implementations, or discussions of Laws of Form in formal/type-theoretic settings

2. **Initial object approaches**: Any work using category-theoretic universal properties to model "pre-distinction" or "potential"

3. **The type signature question**: Any discussion of operations that "create new types" or "extend domains" in dependent type theory—anything that addresses how to formalize genuine creation rather than rearrangement

4. **Assessment**: Which of these approaches is most likely to be tractable in Agda? Which is most likely to capture what the theory needs?
