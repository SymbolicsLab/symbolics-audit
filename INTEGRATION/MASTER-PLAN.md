# MASTER PLAN: Symbolics Theory Integration

*Created: 2026-02-04*
*Last updated: 2026-02-17 (Session 16 — vault integration pass)*
*Purpose: Comprehensive strategic roadmap for theory development, integration, and publication*

---

## Part I: Loose Ends and Unresolved Questions

### 1.1 Critical Theoretical Gaps

| Gap | Description | Location of Prior Work | Severity |
|-----|-------------|------------------------|----------|
| **Genesis Problem** | How does distinction emerge from non-distinction? The theory describes operations on distinctions but not their origin. "Pressure crystallizes into distinction" is metaphor, not mechanism. | Two-Body paper addresses necessary conditions; no mechanism for crystallization | CRITICAL |
| **Organism Boundaries** | If distinction requires two bodies, but organisms are themselves products of distinction, constitution becomes circular. | Two-Body paper §7 acknowledges but doesn't resolve | CRITICAL |
| **Intelligibility of the Continuum** | The theory assumes the field has articulable structure (joints, ridges). If it lacks this, endogenous/exogenous distinction collapses. | 04_Ecology presupposes; nowhere defended | CRITICAL |
| **Fold: Operator vs Relation** | Pentad describes fold as relation (inclusion); Agda implements fold as operator. These are not equivalent. | 05_Formalism documents gap; no resolution | STRUCTURAL |
| **Pressure Formalization** | Pressure is the claimed primitive but cannot be typed (pre-symbolic). | Multi-agent report §III.1 | FUNDAMENTAL |

### 1.2 Concept Drift (Dossier → Pentad)

| Concept | Dossier Meaning | Pentad Meaning | Status |
|---------|-----------------|----------------|--------|
| **Distinction** | Logical primitive, Level 1 of hierarchy | Emergent from two-body recognition under pressure | MAJOR DRIFT |
| **Pressure** | Downstream of remainder | True primitive, prior to everything | REVERSED CAUSALITY |
| **Fold** | Operator with formal properties | Relation (inclusion) | STRUCTURAL CONFLICT |
| **Self** | Levels 5-6 with Godelian machinery, S_t → S_{t+1}, Filter Equation | Level 5+ (recursive self-modeling) in unified hierarchy | DEGRADATION |
| **Truth** | Cannot not commit (fold-dynamics) | Resilience gradient | MAJOR DRIFT |

**Required Action**: State explicitly what is primitive (pressure vs distinction) and defend the choice. Reconcile or explicitly supersede the Dossier framework.

### 1.3 Lost Architectures Requiring Recovery or Explicit Abandonment

| Architecture | Dossier Location | What Was Lost | Pentad Replacement | Decision Required |
|--------------|------------------|---------------|-------------------|-------------------|
| **Dual Hierarchy** (Organizational + Locus) | Research Dossier: Synthesis parts 1-6, New Insight parts 1-3 | Who folds? Agency at each level. Cross-locus constraints. | Three-level Policy Stratification + interface | DIFFERENT QUESTIONS — may need both |
| **Temporal Hierarchy** | Research Dossier: Synthesis part 3 | 7 distinct time structures by level | Nothing (time treated as uniform) | RECOVER or explain why uniform |
| **Metabolic Regimes** | Research Dossier: Synthesis part 4, New Insight part 2 | Creative/Homeostatic/Crystalline with ΔI conditions | Implicit only | RECOVER formal conditions |
| **Levels 5-6** | Research Dossier: Synthesis part 5-6 | Godelian pressure, S+1 re-entry, Filter Equation | "Self as endpoint of five moves" | RECOVER mechanism or argue abandonment |
| **Inverted Filter** | Research Dossier: New Insight part 3 | F₋₁ ∝ I₅ / Tolerance(P) | Not present | EVALUATE for recovery |

### 1.4 Review Feedback Pending (Inference as Policy Paper)

From Session 11 (Gemini + ChatGPT):

**HIGH PRIORITY**:
- `resilience-vs-fit`: Truth tracks FIT (topological), not internal resilience. Paranoid system is resilient but false.
- `dyadic-monadic-problem`: If distinction is dyadic, where does solitary inference get its 'no'?
- `second-box-underdefined`: □ (topological necessity) dissolved — one modality (settlement). Resilience replaces □. Paper needs revision to reflect this.

**MEDIUM PRIORITY**:
- `layer-5-status`: Is metabolic evaluation a policy layer or the interface with world?
- `constitutive-vs-normative`: Distinction-preservation needs a live target, not straw.
- `distinction-token-vs-form`: Separate formal role from metaphysical story.

**Location**: state.yaml `review_feedback_session_11`

### 1.5 Open Questions (from 04_Ecology and Multi-Agent Report)

- Is the endogenous/exogenous distinction itself a distinction? (Self-reference)
- Can a distinction be both endogenous AND exogenous simultaneously?
- When does constraint without an agent become constraint with one?
- Is there a threshold of naturalization beyond which de-naturalization becomes practically impossible?
- What is the name for the opposite pathology of paranoia? (System that treats all constraint as illegitimate)
- How does resilience interact operationally with settlement (□)?

---

## Part II: Current State Assessment

### 2.1 The Pentad (Current North Star)

| Document | Content | Status | Needed Updates |
|----------|---------|--------|----------------|
| **01_Ontology** | Pressure, Index, Distinction, Two-Body, Resilience, Peirce | ACTIVE | Session 16: dyadic-monadic resolution + Peirce connection added |
| **02_Operations** | Cut, Fold, Policy clusters, Three-level stratification + interface | ACTIVE | Session 16: hierarchy unified, metabolic arrest framing, Level renumbering |
| **03_Phenomenology** | Remainder, Unfold, Shimmer, Opacity | ACTIVE | Session 16: remainder anti-parametric argument added, Level renumbering |
| **04_Ecology** | Sources, Naturalization, One modality (settlement) | ACTIVE | Session 16: verified clean — no changes needed |
| **05_Formalism** | Agda bridge documentation, Session 14 milestone | ACTIVE | Session 16: idempotence resolved, Session 14 milestone, gap tables updated |

### 2.2 The Three Papers

| Paper | Location | Status | Next Steps |
|-------|----------|--------|------------|
| **The Two-Body Problem** | `symbolics-research/Papers/two-body-problem/` | DRAFT COMPLETE (6 rounds Gemini review) | Final proofread, decide venue |
| **Remainder Under Feedback** | `symbolics-research/Papers/remainder-under-feedback/` | Draft | Revise in light of two-body framework; social ontology bridge |
| **Inference as Policy** | `symbolics-research/Papers/inference-as-policy/` | Draft with Session 11 feedback | Address HIGH priority review items |

### 2.3 Agda Codebase Status

**Location**: `symbolics-core/src/`

**Verified (~154/163 claims, ~94%)** — post-Session 14 unified formalization:
- Core logic: Val, DNF soundness, lattice properties (~80+ lemmas)
- Gap Theorem: Selective vs Exploratory regimes structurally distinct
- T-Failure: ∘A → A is NOT valid in LFI1
- Conservativity and contradiction-preservation across LP, FDE, WorldIndexed
- Idempotence: proven for both LP and FDE WorldIndexed
- Potential characterization: `potential = 0 ↔ homeostatic window`
- Session 14 unified Symbolics module tree (20 new modules, ~90 new theorems): Remainder (6 properties), Unfold (expansion + incorporation), Settlement (via idempotence), Resilience (bounded by space size), Two-body conditions (structural properties)

**Remaining gaps (9)**:
- 7 DNFSoundness compound consistency stubs (by design)
- 2 Mechanics holes
- Lyapunov property and convergence (postulated in `Potential.Conjectures`)

**Key Gap**: Fold as operator (Agda) vs fold as relation (theory). Would require category-theoretic foundations to close.

### 2.4 DSL Codebase Status

**Location**: `symbolics-dsl/`

**Findings**:
- Core modules functional: `belnap.ts`, `side.ts`, `context.ts`, `policy.ts`
- **Additive Evidence Bound PROVEN**: Under monotone evidence, conflict switches ≤ 1
- **CRITICAL**: "Metabolic tension" results INVALIDATED — placeholder artifacts discovered

### 2.5 Vault Archive

**Location**: `symbolics-research/Vault/_Archive/Legacy_2026-02/`

**Key recoverable insights** (80 files surveyed):
- Full Organizational Hierarchy with Levels -2 through 6
- Locus Hierarchy (Locus 0-3 with organizational reach)
- Levels 5-6 formal machinery: S_t structure, Godelian pressure, P operator
- Filter Equation: F₋₁ ∝ I₅ / Tolerance(P)
- LLM Phenomenology notes
- Alignment as attractor engineering
- Many unintegrated draft concepts

### 2.6 Research Dossier

**Location**: `/Users/vivianesauriol/Documents/RESEARCH/Research Dossier/`

**Key files**:
- `Summary of New Insight.txt` — Overview of lost architectures
- `New Insight part 1-3.txt` — Dual hierarchy, metabolic regimes, inverted filter
- `Synthesis part 1-6.txt` — Most complete exposition of Dossier-era theory

**Note**: PDFs in this folder were not surveyed (file too large for agent). May contain additional insights.

---

## Part III: What Should Be Done

### 3.1 Theoretical Coherence (Internal Consistency)

| Priority | Task | Rationale | Deliverable |
|----------|------|-----------|-------------|
| 1 | **Resolve primitivity question** | Dossier has distinction primitive; Pentad has pressure primitive. Cannot both be true. | Explicit statement in 01_Ontology with defense |
| 2 | **Reconcile Dossier/Pentad architectures** | Two incompletely synthesized systems. Policy stratification and dual hierarchy answer different questions. | Mapping document or explicit supersession argument |
| 3 | **Address fold operator/relation gap** | Structural conflict at heart of formalization | Either category-theoretic extension OR explicit acceptance that Agda captures one aspect only |
| 4 | ~~**Formalize the two modalities**~~ | **SUPERSEDED** (Session 12): One modality — settlement. Resilience is the measure. | Done — integrated into vault (04_Ecology, 05_Formalism) |
| 5 | **Maintain anti-paranoia mechanisms** | Theory's self-sealing capacity is a risk | Continue documenting tensions; resist explaining everything as "different levels" |

### 3.2 Theoretical Reach (What Hasn't Been Addressed)

| Priority | Gap | Why Important | Approach |
|----------|-----|---------------|----------|
| 1 | **Genesis mechanism** | Theory starts in medias res; cannot distinguish from phenomenology of already-constituted systems | Develop sixth document or extend Two-Body paper |
| 2 | **Multi-agent dynamics** | "Whose fold dominates?" unanswered; all cross-domain tests revealed this | Game-theoretic module or multi-agent extension |
| 3 | **Substrate constraints** | Organism-side limits (neural, material, developmental) not captured by "pressure" | Connect to embodied cognition; develop Locus downward |
| 4 | **Timescale significance** | Theory claims "timescale not structurally interesting" but cross-domain evidence contradicts | Either recover temporal hierarchy OR explain away rate-dependence |
| 5 | **Ethical dimension** | Theory describes how distinctions operate but not which should be made | Explicitly mark as outside scope OR develop normative extension |

### 3.3 Integration Work

| Task | Sources | Target | Priority |
|------|---------|--------|----------|
| Recover Locus Hierarchy | Research Dossier Synthesis parts, Vault Archive | Either 01_Ontology OR new document | HIGH |
| Recover Levels 5-6 machinery | Research Dossier Synthesis part 5-6 | 01_Ontology self section | HIGH |
| Recover Metabolic Regimes | Research Dossier New Insight part 2 | 03_Phenomenology | MEDIUM |
| Recover Filter Equation | Research Dossier New Insight part 3 | Where? (connects identity to attention) | MEDIUM |
| Recover Temporal Hierarchy | Research Dossier Synthesis part 3 | Needs evaluation: recover or abandon? | MEDIUM |
| Integrate Session 10 insights | state.yaml `session_10_insights` | 02_Operations (policy stratification details) | ~~HIGH~~ DONE (Session 16) |
| Address Session 11 review | state.yaml `review_feedback_session_11` | Inference as Policy paper | HIGH |

---

## Part IV: Should the Pentad Be Expanded?

### 4.1 The Case for a Sixth Document: Genesis

The Multi-Agent Report's strongest recommendation:

> "Without an account of genesis, the theory cannot distinguish itself from a sophisticated phenomenology of already-constituted symbolic systems. The bootstrap is missing."

**What a Genesis document would address**:
1. The threshold problem (when does proto-distinction become distinction?)
2. The bootstrapping problem (how can two systems coordinate on a distinction neither possesses?)
3. The first distinction problem (what was it? how constituted without scaffolding?)
4. The minimal dyad (simplest system capable of distinction constitution)
5. Developmental ontogeny (organism's passage from differentiation to distinction)
6. Phylogeny (evolutionary emergence of the symbolic order)

**Recommendation**: YES, add 06_Genesis.md. This is the theory's deepest gap.

### 4.2 The Case Against: Keep Pentad, Develop in Papers

Counter-argument: The Two-Body paper addresses emergence. Genesis mechanism may be better developed through papers where speculative proposals can be tested against peer review before being canonized in the vault.

**Compromise**: Create 06_Genesis.md as a placeholder that:
- Acknowledges the gap explicitly
- Documents the necessary conditions (two-body, shared pressure, observability, alignment)
- Lists candidate mechanisms (sensory exploitation, coordination games, symmetry breaking, recursive condensation)
- Does not assert a solution

### 4.3 Should Locus Be Recovered?

The Locus Hierarchy answers "who folds?" — a question the Policy Stratification doesn't address.

**Options**:
1. **Recover Locus as separate dimension** — Pentad becomes Hexad (or Locus gets integrated into 01_Ontology)
2. **Extend Two-Body** — Develop the account of agency from the two-body framework
3. **Accept the gap** — Explicitly acknowledge that agency/locus is outside scope

**Recommendation**: Integrate Locus into 01_Ontology as a section on "Agency: Who Folds?" rather than a separate document. The question is too foundational to separate.

### 4.4 Verdict on Pentad Expansion

| Proposed Change | Recommendation | Rationale |
|-----------------|----------------|-----------|
| Add 06_Genesis.md | YES (as placeholder) | Deepest theoretical gap; explicit acknowledgment better than silence |
| Add Locus Hierarchy | INTEGRATE into 01_Ontology | Not a sixth topic but a dimension of distinction |
| Recover Temporal Hierarchy | INTEGRATE into 03_Phenomenology OR argue against | Rate-dependence evidence is strong |
| Recover Metabolic Regimes | INTEGRATE into 03_Phenomenology | Diagnostic power lost without formal conditions |
| Recover Levels 5-6 | INTEGRATE into 01_Ontology | Mechanism of self-referential systems is missing |

---

## Part V: Papers to Write or Revise

### 5.1 Papers in Progress

| Paper | Status | Priority | Next Actions |
|-------|--------|----------|--------------|
| **The Two-Body Problem** | Draft complete | 0 (ready) | Final proofread, venue selection |
| **Remainder Under Feedback** | Draft | 1 | Align with two-body framework; verify institutional examples |
| **Inference as Policy** | Draft + Session 11 feedback | 2 | Address review feedback (resilience vs fit, dyadic-monadic, □ definition) |

### 5.2 Papers to Write

| Proposed Paper | Core Claim | Source Material | Priority |
|----------------|------------|-----------------|----------|
| **The Genesis Problem** | Mechanism for how distinction emerges from non-distinction | Multi-agent report §VI; candidate mechanisms | HIGH (if genesis remains gap) |
| **Policy Stratification** | Three-level structure + interface with presupposition ordering + dynamic entanglement | state.yaml `session_10_insights.policy-stratification`; precedent analysis (Ostrom, Beer, Bateson) | MEDIUM |
| ~~**The Two Modalities**~~ | **DISSOLVED** (Session 12): One modality — settlement. Resilience does the work □ was trying to do. | n/a | SUPERSEDED |
| **Metabolic Regimes** | Formal conditions for Creative/Homeostatic/Crystalline; diagnostic power | Research Dossier materials | LOW (integrate into existing first) |
| **LLM as Case Study** | LLMs lack triangulation; inference without distinction; metabolism temporally segmented | Vault Archive LLM notes; Session 11 insight | LOW (after foundational papers) |

### 5.3 Publication Strategy

**Foundational layer** (establish the framework):
1. The Two-Body Problem → Submit first
2. Inference as Policy → After addressing feedback

**Bridge layer** (connect to disciplines):
3. Remainder Under Feedback → Social ontology bridge
4. Policy Stratification → Logic/philosophy of science

**Extension layer** (develop reach):
5. Genesis → Developmental/evolutionary
6. Resilience paper → Modal logic / epistemology (replaces dissolved Two Modalities)

---

## Part VI: Execution Order

### Phase 1: Stabilize Core (Weeks 1-2)

**Objective**: Achieve theoretical coherence before extending reach.

1. **Resolve primitivity question** — Is pressure or distinction primitive? Write explicit defense in 01_Ontology.
2. **Address Session 11 review feedback** — Fix Inference as Policy paper (resilience vs fit, □ definition, dyadic-monadic).
3. **Finalize Two-Body paper** — Proofread, select venue, submit.
4. **Integrate Session 10 insights** — Update 02_Operations with policy stratification details.

### Phase 2: Recover Lost Architectures (Weeks 3-4)

**Objective**: Bring valuable Dossier-era insights into the Pentad.

5. **Recover Locus Hierarchy** — Integrate into 01_Ontology as "Agency: Who Folds?"
6. **Recover Levels 5-6 machinery** — Integrate into 01_Ontology (self section).
7. **Recover Metabolic Regimes** — Integrate into 03_Phenomenology with formal conditions.
8. **Decide on Temporal Hierarchy** — Either recover or argue against; cross-domain evidence suggests recovery.

### Phase 3: Address Theoretical Reach (Weeks 5-6)

**Objective**: Extend theory to cover gaps.

9. **Create 06_Genesis.md** — Placeholder document acknowledging the gap, listing candidate mechanisms.
10. ~~**Formalize two modalities**~~ — SUPERSEDED (Session 12): One modality (settlement). Formalize resilience instead.
11. **Revise Remainder Under Feedback paper** — Align with two-body framework.

### Phase 4: Reconcile Dossier/Pentad (Week 7)

**Objective**: Achieve explicit synthesis or supersession.

12. **Produce architecture mapping document** — Show how Policy Stratification relates to Dual Hierarchy, or argue supersession.
13. **Update 05_Formalism** — Document what Agda captures and what it doesn't (operator vs relation, pre-symbolic limits).

### Phase 5: Formalization Push (Weeks 8+)

**Objective**: Close the gap between theory and Agda.

14. **Evaluate category-theoretic path** — Would it close operator/relation gap?
15. ~~**Complete bucket sortedness**~~ — DONE (Session 14): WorldIndexed idempotence proven.
16. **Deepen unified Symbolics modules** — Move from type encodings to richer proofs (remainder dynamics, resilience as continuous measure, emergence mechanism).
17. **Address coinductive types** — If metabolism is to be modeled as infinite process.

### Phase 6: Papers and Publication (Ongoing)

18. **Submit Two-Body Problem**
19. **Revise and submit Inference as Policy**
20. **Revise and submit Remainder Under Feedback**
21. **Draft Policy Stratification paper** (if warranted after integration)
22. ~~**Draft Two Modalities paper**~~ — DISSOLVED (Session 12). Consider resilience paper instead.

---

## Part VII: All Valuable Insights with Locations

### 7.1 Core Theory (Pentad)

| Insight | Location | Status |
|---------|----------|--------|
| Pressure as true primitive | 01_Ontology | Needs explicit defense |
| Index as organism's orientation (5 components) | 01_Ontology | Established |
| Two-Body Hypothesis | 01_Ontology, Two-Body paper | Draft complete |
| Distinction = representation | 01_Ontology | Integrated Session 9 |
| Recursion of distinction (mise en abyme) | 01_Ontology | Integrated Session 9 |
| Cut = distinction-to-field; Fold = distinction-to-distinction | 02_Operations | Established |
| Policy = cluster of folds; induces operator | 02_Operations | Established |
| Three-level policy stratification + interface | 02_Operations | INTEGRATED (Session 16) |
| Remainder as what any distinction excludes | 03_Phenomenology | Integrated Session 9 |
| Incremental vs catastrophic unfold | 03_Phenomenology | Established |
| Shimmer (dual: oscillation + trace) | 03_Phenomenology | Established |
| Opacity as gradient of index access | 03_Phenomenology | Established |
| Endogenous (fit) vs Exogenous (constraint) | 04_Ecology | Established |
| Constraint produces fit; de-naturalization | 04_Ecology | Integrated Session 9 |
| □ (settlement) — one modality; resilience as measure | 04_Ecology, 05_Formalism | INTEGRATED (Session 12 decision, Session 16 vault pass) |
| Naturalization = constraint appearing as topology | 04_Ecology | Established |
| The Fall: irreversibility and desire | 04_Ecology | Integrated Session 11 |
| T-failure: □φ → φ fails | 05_Formalism | Verified in Agda |
| Gap Theorem: Selective vs Exploratory distinct | 05_Formalism | Verified in Agda |

### 7.2 Lost Architectures (Dossier)

| Insight | Location | Recovery Priority |
|---------|----------|-------------------|
| Organizational Hierarchy (Levels -2 to 6) | Research Dossier Synthesis parts 1-2 | HIGH (partial — Levels 5-6) |
| Locus Hierarchy (0-3 with organizational reach) | Research Dossier Synthesis part 2; Vault Archive | HIGH |
| Temporal Hierarchy (7 time structures) | Research Dossier Synthesis part 3 | MEDIUM |
| Metabolic Regimes (Creative/Homeostatic/Crystalline) | Research Dossier New Insight part 2 | HIGH |
| Filter Equation: F₋₁ ∝ I₅ / Tolerance(P) | Research Dossier New Insight part 3 | MEDIUM |
| S_t structure with Godelian pressure | Research Dossier Synthesis part 5 | HIGH |
| P operator (plastic act: S_t → S_{t+1}) | Research Dossier Synthesis part 6 | HIGH |
| Level crossing via S+1 recursive re-entry | Research Dossier Synthesis part 5-6 | HIGH |

### 7.3 Session 10-11 Insights (state.yaml)

| Insight | Location | Integration Status |
|---------|----------|-------------------|
| Inference not distinct category; gradient of constraint | state.yaml `inference-not-distinct-category` | INTEGRATED into 02_Operations (Session 16) |
| Truth as resilience (not topological necessity) | state.yaml; Session 12 one-modality decision | INTEGRATED into 01_Ontology, 04_Ecology, 05_Formalism |
| Distinction-preservation truly constitutive | state.yaml `distinction-preservation-truly-constitutive` | INTEGRATED into 02_Operations metabolic arrest (Session 16) |
| Three-level policy stratification + interface | state.yaml `policy-stratification` | INTEGRATED into 02_Operations (Session 16) |
| Fatal objection dissolved (regress terminates) | state.yaml `fatal-objection-dissolved` | Ready for paper |
| One modality (settlement); two-modalities dissolved | Session 12 decision | INTEGRATED into 04_Ecology, 05_Formalism |
| Peirce connection (alignments + divergences) | state.yaml `peirce-connection` | INTEGRATED into 01_Ontology (Session 16) |
| Classical logic bias owned (LP vs classical+AGM) | state.yaml `classical-logic-bias-owned` | INTEGRATED into 02_Operations (Session 16) |

### 7.4 Formalization Status (Agda/DSL)

| Claim | Location | Status |
|-------|----------|--------|
| Conservativity | symbolics-core: Core, FDE, WorldIndexed | VERIFIED |
| Contradiction-preservation | symbolics-core: Core, FDE, WorldIndexed | VERIFIED |
| Idempotence (LP) | symbolics-core: LP | VERIFIED |
| Idempotence (WorldIndexed) | symbolics-core: WorldIndexed | VERIFIED (Session 14) |
| Gap Theorem | symbolics-core: Gap.agda | VERIFIED |
| T-Failure | symbolics-core: TFailure.agda | VERIFIED |
| Potential = 0 ↔ homeostatic | symbolics-core: Mechanics | VERIFIED |
| Lyapunov property | symbolics-core: Potential.Conjectures | POSTULATED |
| Additive Evidence Bound | symbolics-dsl | PROVEN |
| Metabolic tension | symbolics-dsl | INVALIDATED (placeholder) |

### 7.5 Cross-Domain Insights (Multi-Agent Report)

| Insight | Location | Applicability |
|---------|----------|---------------|
| Catastrophic unfold pattern: rigid + organized remainder + blocked L4 = rupture | Multi-agent report §IV.2.1 | Immune, markets, institutions |
| Naturalization highly general | Multi-agent report §IV.2.2 | All domains |
| T-failure maps across all domains | Multi-agent report §IV.2.3 | Most formally precise portable insight |
| Policy stratification (L1-4) maps; L5 breaks | Multi-agent report §IV.2.4 | Systems without self-modeling |
| Multi-agent failure pattern | Multi-agent report §IV.1.1 | Immune, markets, language |
| Substrate constraints not captured | Multi-agent report §IV.1.2 | All biological domains |
| Rate/timescale matters | Multi-agent report §IV.1.3 | Flash crashes, critical periods |

### 7.6 The Dark Pentad (Structural Shadow)

| Reframing | Standard Pentad | Dark Pentad | Location |
|-----------|-----------------|-------------|----------|
| Cut | Partition enabling form | Wound destroying continuum | Multi-agent report §VIII |
| Fold | Stabilization achievement | Ossification/loss of possibility | Multi-agent report §VIII |
| Remainder | Pressure driving generation | Mourning/haunting | Multi-agent report §VIII; 04_Ecology "The Fall" |
| Fit | Tracking structure | Successful domination | Multi-agent report §VIII |
| T-failure | Formal signature of becoming | Formal signature of failure | Multi-agent report §VIII |

**Status**: Acknowledged in 04_Ecology ("The Fall" section). Theory owns both framings as true.

---

## Part VIII: Monitoring and Maintenance

### 8.1 Anti-Paranoia Checklist

The theory's self-sealing capacity is a structural risk. Maintain these safeguards:

- [ ] Continue distinguishing "conjecture" from "verified" in formalization
- [ ] Document where the theory doesn't cohere (don't explain away as "different layers")
- [ ] Maintain formalization commitment (external constraint)
- [ ] Acknowledge the Dark Pentad as equally consistent interpretation
- [ ] Test claims against cross-domain cases (where does theory break?)

### 8.2 Key Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Agda verification rate | ~94% (~154/163 claims) | Maintain or improve |
| Remaining gaps | 9 (7 stubs + 2 holes) | Reduce |
| Lost architectures recovered | 0/5 | 5/5 |
| Session 10-12 insights integrated into vault | 8/8 | DONE |
| Session 11 review feedback addressed (paper) | 0/10 | 10/10 |
| Papers submitted | 0/3 | 3/3 |

### 8.3 Regular Review Points

- **After each vault update**: Check for concept drift; update this plan if needed
- **Before paper submission**: Verify alignment with current vault state
- **Monthly**: Assess metabolic regime (creative vs homeostatic vs crystalline)
- **Quarterly**: Re-evaluate whether genesis gap has been addressed

---

## Appendix A: File Location Reference

### Symbolics-Research (Vault)
```
symbolics-research/Vault/
├── 00_Theory_Map.md           # Entry point
├── Active/
│   ├── 01_Ontology.md         # Pressure, Index, Distinction, Two-Body
│   ├── 02_Operations.md       # Cut, Fold, Policy
│   ├── 03_Phenomenology.md    # Remainder, Unfold, Shimmer, Opacity
│   ├── 04_Ecology.md          # Sources, Naturalization, Modalities
│   └── 05_Formalism.md        # Agda bridge
├── _Archive/Legacy_2026-02/   # 80 legacy files (searchable)
├── Papers/
│   ├── two-body-problem/      # Draft complete
│   ├── remainder-under-feedback/
│   └── inference-as-policy/
└── CLAUDE.md
```

### Symbolics-Core (Agda)
```
symbolics-core/src/
├── Core/           # Val, DNF, lattice
├── LP/             # LP policy
├── FDE/            # FDE policy
├── LFI/            # T-failure proofs
├── Mechanics/      # Dynamics, Gap theorem
├── Modal/          # Modal operators
└── Applications/   # DSL wiring
```

### Symbolics-DSL (TypeScript)
```
symbolics-dsl/
├── belnap.ts       # Four-valued logic
├── side.ts         # Side type
├── context.ts      # Context operations
└── policy.ts       # Policy implementations
```

### Symbolics-Audit (Integration)
```
symbolics-audit/
├── INTEGRATION/
│   ├── state.yaml              # Current project state
│   ├── decision-log.md         # Reframe history
│   ├── MASTER-PLAN.md          # This document
│   └── Multi-Agent-Reports/    # Survey reports
├── spec/registry.yaml          # Cross-layer contract
└── scripts/audit.py            # Audit script
```

### Research Dossier
```
/Users/vivianesauriol/Documents/RESEARCH/Research Dossier/
├── Summary of New Insight.txt
├── New Insight part 1-3.txt
├── Synthesis part 1-6.txt
└── [PDFs not surveyed]
```

---

## Appendix B: Decision Log for This Plan

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-04 | Created MASTER-PLAN.md | Need comprehensive roadmap after multi-agent survey |
| 2026-02-04 | Recommend 06_Genesis.md as placeholder | Genesis is deepest gap; explicit acknowledgment better than silence |
| 2026-02-04 | Recommend Locus integration into 01_Ontology | Agency question is dimension of distinction, not separate topic |
| 2026-02-04 | Phase 1 priority: stabilize core before extending reach | Theoretical coherence must precede theoretical reach |
| 2026-02-17 | Session 16: Full vault integration pass | Integrated Session 12 decisions (one modality, hierarchy unification, layer collapse, metabolic arrest) + Session 10 insights (Peirce, classical logic bias, policy stratification) + Session 14 Agda milestone into all 5 vault docs. Two Modalities paper dissolved. Level renumbering across all documents. |

---

*End of Master Plan*
