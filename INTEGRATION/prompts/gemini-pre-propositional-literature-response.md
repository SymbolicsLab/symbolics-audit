# Gemini Response: Pre-propositional Literature Reconnaissance

**Date received**: 2026-02-01
**Prompt**: `gemini-pre-propositional-literature.md`
**Context**: ADR-002 open thread

---

## Summary

Gemini validated the core intuition: `Cut : A → A` is fundamentally wrong because standard functions rearrange elements of fixed types; they don't generate the types they inhabit. The response provides three major tracks:

1. **Spencer-Brown formalizations** (Bricken, Kauffman)
2. **Categorical approaches** (Lawvere adjointness, walking arrow, comonads)
3. **Type signature solutions** (Induction-Recursion, context extension)

---

## Full Response

### 1. Spencer-Brown Formalizations

#### A. Boundary Logic (Bricken)

**Source**: William Bricken, "The Mathematics of Boundaries" (2001)

**Key insight**: Formalize the "unmarked state" not as a set, but as a **rewrite rule target**. The "mark" is a container. `(()) -> (void)`.

**Agda recommendation**: Do not model the mark as a function. Model it as:
- An **Inductive Type** (tree structure of nested marks)
- A **Relation** (reduction rules)

#### B. Topological/Knot-Theoretic (Kauffman)

**Source**: Louis Kauffman, "Laws of Form and the Logic of Non-Duality" & *Knots and Physics*

**Key insight**: Maps the "Mark" to a crossing in knot theory. Formalizes the mark as a self-referential operator `J = -1/J`.

**Agda utility**: For "depth" or "crossing" aspects, look at **Planar Algebras** (Temperley-Lieb), which have categorical definitions.

#### C. The "Unmarked State"

**Consensus split**:
- **Logical interpretation**: Unmarked = False (⊥), Mark = negation (¬)
- **Topological interpretation**: Unmarked = Plane (universal), Mark = boundary

**Agda recommendation**: In Type Theory, the unmarked state is best modeled as the **Context (Γ) itself**, not a type within the context.

---

### 2. Categorical Pre-Distinction

#### A. Lawvere's Adjointness

**Source**: F. William Lawvere, "Adjointness in Foundations" (1969)

**Key concept**: The act of distinction is a pair of **Adjoint Functors**:
- "Unmarked" = category of simple objects (e.g., Sets)
- "Marked" = category with more structure (e.g., Graphs)
- "Cut" = **Free Functor** (Left Adjoint) moving from simpler to complex

**Why this fits**: Adjoints satisfy universal properties. The Left Adjoint (Free construction) is the "canonical" way to make a distinction.

#### B. The Walking Arrow & Interval

**Concept**: Category **2** (two objects 0, 1 and one arrow 0 → 1)

**Relevance**: This is the *generic distinction*. In Cubical Type Theory:
- The **Interval Type (I)** has endpoints `i0` and `i1`
- It is **pre-logical**: `i0` and `i1` are distinct, but you cannot case-split on them like Booleans
- They represent the **potential for distinction**

#### C. Comonads and "Before"

**Source**: Varela, Maturana, Uribe (Autopoiesis)

**Formalism**: Aligns with **Cofree Comonad**. The "Act of Distinction" extracts a specific value from this cofree context.

---

### 3. The Type Signature Problem

#### A. Induction-Recursion (Recommended)

**Concept**: Define a Universe type (U) and decoding function (El : U → Set) **simultaneously**.

**How it works**:
```agda
-- U = the set of distinctions made so far
-- Cut is a constructor of U
-- El (Cut u) defines contents of new distinction

data U : Set
El : U → Set

data U where
  base : U
  cut  : (u : U) → U

El base     = ⊥        -- or ⊤, depending on interpretation
El (cut u)  = Either (El u) (El u)  -- or some extension
```

**Why it fits**: The "Cut" literally expands the universe of discourse.

#### B. Context Extension (Sigma Types)

**Signature**: `Cut : (Γ : Context) → Σ (Γ' : Context) (mapping : Γ' → Γ)`

**Mechanism**: "Cut" returns new context paired with a way to view old context inside it.

**Literature**: Categorical Logic (Hyperdoctrines). The "Cut" is a pullback of the subobject classifier.

---

## Assessment

### Best Formal Model: Induction-Recursion

**Why**: Only standard Agda feature that allows the codomain type to be defined by the function's input.

**Implementation sketch**:
- Define `World` (Pre-Cut field) as inductive type
- Define `Observation : World → Set` recursively
- `cut` is a constructor: `cut : (w : World) → World`
- "New Type" is `Observation (cut w)`

### Best Theoretical Reference: Kauffman & Bricken

- Don't implement Spencer-Brown's arithmetic as functions on bits
- Implement **Boundary Algebra as rewrite system on Trees**
- "Unmarked State" = Empty type in `Observation` (nothing observed), but Unit type in `World` (exists as root)

### Best Categorical Abstraction: Adjointness

- Treat "Pre-cut" field not as object, but as **Category**
- "Cut" is a Functor creating more complex category

---

## Deliverables Summary

| Concept | Formalization Strategy | Key Source |
|---------|----------------------|------------|
| Unmarked State | Unit (Terminal) or Void (Initial) | Bricken (void-substitution) |
| The Mark | Inductive Constructor `cross : Form → Form` | Kauffman (Knot Logic) |
| The Cut | Induction-Recursion: Cut extends Universe U | Martin-Löf / Agda Docs |
| Laws of Form | Equivalence Relations on Inductive Type | Spencer-Brown (Primary Algebra) |

---

## Key Citations

1. Bricken, W. (2001). *The Mathematics of Boundaries: A Beginning*
2. Kauffman, L. H. (2001). *The Mathematics of Charles Sanders Peirce*
3. Lawvere, F. W. (1969). *Adjointness in Foundations*
4. Spencer-Brown, G. (1969). *Laws of Form*

---

## Implications for ADR-002

### Validated
- `Cut : A → A` is fundamentally wrong (confirmed)
- Pre-cut as Context (Γ), not type within context
- Need something beyond standard function types

### New Options Surfaced
1. **Induction-Recursion**: Most promising for `--safe` Agda
2. **Cubical Interval**: Pre-logical distinction (`i0`/`i1` can't be case-split)
3. **Adjoint Functors**: Cut as Free construction

### Concerns
- Induction-Recursion may be complex to work with
- Cubical approach would require `--cubical` (different from current `--without-K`)
- Need to verify Bricken/Kauffman formalizations are actually implementable

### Next Steps
1. Create vault draft synthesizing Gemini's findings
2. Update ADR-002 with new candidate approaches
3. Consider small proof-of-concept: Induction-Recursion World/Observation
