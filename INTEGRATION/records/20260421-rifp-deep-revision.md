# RIFP Post-Cognitivism — Deep Revision Session (2026-04-21)

## Context

RIFP Post-Cognitivism paper ("Cognition Without Representation: Necessity, Commitment, and the Structure of Post-Cognitivist Explanation") was at `REVISED + ASSEMBLED` status after an Apr 19 revision pass. This session was a deep critical-feedback-driven revision addressing peer-review vulnerabilities flagged by the user before submission.

Not a theory-change session. Paper-level framing refinement plus anonymization work.

## Revisions applied (10 structural moves)

1. **§2 rewrite**: Target named explicitly as classical computational representationalism (Fodor/LOT, Marr). Four phenomena (error, selection, learning, cognition/reflex) collapsed to one signatures-of-one-deficit paragraph. Facchin (2021) positioned earlier as closest proximate target-specifier. Ecological-psychology footnote added (Gibson 1966, Withagen 2012, Ingold 2000) acknowledging education-of-attention and affordance solicitation.

2. **§3.5 inserted**: Three-level ontology (field → differentiation → intersubjective encounter) with Tomasello et al. 2012 circularity inoculation — takes intersubjectively capable organisms as evolutionary given; theorizes what it *constitutes*, not how it evolved.

3. **§3.2 directionality hedge**: Preempts active-inference objection (production is present from birth). Claim sharpened: *constitutive* priority of being-bound-by over binding-oneself-to, not temporal priority of reception over production.

4. **§5.2 trimmed**: References §3.5 rather than re-introducing the three levels.

5. **§5.3 ethical seed**: Plants "committing to what matters while remaining open to what the commitment excludes from mattering" in §5.3, earning the conclusion's closing flourish.

6. **§5.4 tightened**: Dreyfus-McDowell setup compressed; Sutton/Christensen meshed-control paragraph cut (tacked on).

7. **§6 gap-migration rewrite** (highest-leverage move): Concedes the softmax objection (structural foreclosure present in LLMs on operational criteria alone). Relocates load-bearing criterion at foreclosure-under-mattering. Introduces gap migration as sharper diagnostic: the gap doesn't vanish, it migrates to the user who adopts the output, under stakes the system does not bear. Predicts characteristic LLM-deployment harms concentrate at the migration boundary.

8. **§7.2 Milkowski deepened**: Direct engagement with mechanistic representation framework (not just Bickhard via proxy). Accepts anti-intrinsicalism; presses one step further — what mechanistic "representations" are *for* is foreclosing alternatives under mattering; that role is commitment, not representation. Empirically leveraged prediction: populations with disrupted early intersubjective history show specific impairments in error-sensitivity *itself*, not merely detection/anticipation machinery.

9. **§7.3 four predictions**: Stakes-modulated narrowing (Cisek-Kalaska paradigm adapted with stakes manipulation). Directionality via Romanian-orphanage cohort (Rutter 2007, Sonuga-Barke 2017); autism parenthetical dropped per neurodiversity/replication concerns. Metabolic cost via bistability (Kloosterman 2015 pupillometry). OCD as detection-without-revision *dissociation* (Gehring 2000, Endrass & Ullsperger 2014) — consistent with the established heightened-ERN literature rather than contradicting it.

10. **Modal notation dropped**: §3.1 □φ ∧ ¬φ prose replaced; footnote 1 removed entirely. §7.1 collapsed to single paragraph. §6 final paragraphs merged. §1 preview tightened.

## Anonymization decisions

**De-anonymization risk identified**: Two published blog posts on symbolicslab.ai — `/blog/gap` (titled "The gap between commitment and realization") and `/blog/structure-of-insight` — use the paper's central conceptual phrase. A reviewer Googling the exact phrase would find them as first hits under the Lab identity.

**Resolution**:
- Set `published: false` on both posts for the ~10-week review window (committed and pushed from `symbolics-lab-site`, Vercel redeployed)
- Renamed "stale necessity" → "gapless necessity" throughout draft (7 replacements). Concept identical; vocabulary distinct enough from "stale closure" in the unpublished blog post to avoid secondary hit
- Kept "commitment and realization" framing in paper — generic enough to Bratman/deontic-logic standard vocabulary, and with the blog posts down, the exact-phrase Google hit disappears

**Pattern worth preserving for future submissions**: when a paper's central concept overlaps with published blog content, unpublishing the blog posts for the review window is lower-friction than rephrasing the paper.

## Framing decisions with downstream relevance

**Gap migration as LLM diagnostic**: The move that concedes structural foreclosure to LLMs (softmax) while locating the diagnostic at foreclosure-under-mattering, and introduces gap migration as the sharper tool, is the strongest technical move the paper makes for the AI-pitch strategy (see `symbolics-pitch/STRATEGY.md`). The gap-migration claim — the user inherits a commitment without access to the mattering-structure — is a principled account of where the characteristic harms of LLM deployment concentrate. Reusable for the field-building/founding-document work.

**Target specification**: Explicitly naming classical computational representationalism (Fodor/Marr) as the target and positioning Gibson/Chemero/Hutto-Myin/Barandiaran as successor frameworks with partial resources is a framing move that will replay in future post-cognitivist-adjacent papers (Synthese Range of Perception, Phil Psych Imagination/Creativity/AI, Inquiry AI Agency). The "representation was doing *foreclosure*" argument is portable.

**Facchin positioning**: Facchin's representation-skeptic PP work is the closest target-specifier. Positioning the paper as continuing Facchin's project rather than reinventing it is the right SI move; worth repeating in other post-cognitivist-adjacent submissions.

## Word count

| Component | Words |
|---|---|
| Body + footnotes | ~10,703 |
| References | 1,199 |
| Total file | 11,902 |

Under RIFP's 11,000 body+footnotes limit with ~300 words of headroom.

## References changed

**Added**: Gibson (1966), Withagen et al. (2012), Tomasello et al. (2012), Rutter et al. (2007), Sonuga-Barke et al. (2017), Gehring et al. (2000), Endrass & Ullsperger (2014), Kloosterman et al. (2015).

**Removed**: Sutton et al. (2011), Christensen et al. (2016).

## Remaining pre-submission tasks

1. `.docx` conversion via `Submissions/_tools/docx_cleanup.py` (Times New Roman, 1.5 spacing, all-black, no links/bookmarks)
2. Supplementary file (author info) for non-anonymous version
3. Final citation audit
4. Submit via www.rifp.it with code "Post-cognitivism2026" in Communications to the Editor

## Cross-repo state

- `symbolics-research`: `Submissions/2026-04-30_RIFP_Post-Cognitivism/draft.md` modified
- `symbolics-lab-site`: `site/content/blog/gap.mdx` and `site/content/blog/structure-of-insight.mdx` set to `published: false` (committed + pushed, SHA: 6473507)
- `~/Developer/OVERVIEW.md` and `~/.claude/.../MEMORY.md` updated
