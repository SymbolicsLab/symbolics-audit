# Symbolics Project: Core Principles
**Version**: 0.1.0 | **Date**: 2026-01-31

These principles govern all work on the Symbolics project. When in doubt, come back here.

---

## I. The theory comes first.

Infrastructure, tooling, agent systems, and processes exist to serve the theory. If the ratio of meta-work to object-level work starts climbing, stop and redirect. The measure of a good session is not how many documents were updated but whether something was understood better, proven, or honestly questioned.

## II. Honesty over completeness.

Never claim something is verified when it is conjectural. Never present a pattern-match as a proof. Never smooth over a genuine uncertainty to make the system look more complete. The theory's credibility depends on being ruthlessly honest about what is established, what is open, and what might be wrong. Every document, every note, every claim must accurately report its own epistemic status.

## III. Let the material speak before refining it.

The theory is wider and stranger than any single session's analysis can capture. Before imposing structure, read carefully. Before formalizing, understand conceptually. Before dismissing an intuition, explore it. The user's philosophical intuition is the ultimate authority on what the theory IS — not any agent's interpretation.

## IV. One source of truth per domain.

- **Vault conventions**: `Vault/CLAUDE.md` (authoritative — never restate or simplify elsewhere)
- **Formal verification**: Agda under `--safe --without-K` (if it doesn't type-check, it isn't proven)
- **Audit alignment**: `symbolics-audit/spec/registry.yaml` and audit scripts
- **Research orchestration**: `INTEGRATION/` documents
- **Current state**: `INTEGRATION/HANDOFF.md`

Do not create competing versions of any of these. If a convention needs to change, change it at the source.

## V. Trace everything.

Every claim should be traceable to its evidence. Every formal result to its proof. Every vault note to its source material. Every decision to its rationale (via ADRs). Every insight to the abstract or document it came from. If it can't be traced, it can't be trusted.

## VI. Depth over breadth.

Better to solve one problem thoroughly — understanding it conceptually, formalizing it correctly, stress-testing it honestly — than to touch ten problems superficially. The open problem registry has 20 entries; most sessions should focus on one or two. Resist the temptation to "make progress on everything."

## VII. Build in skepticism.

If no one is questioning a claim, question it yourself. Schedule red-team sessions. Ask for strongest objections. Construct counterexamples. The theory becomes stronger through honest challenge, not through accumulating confirmations. Every agent should be instructed to push back, not to agree.

## VIII. Persistent state lives in files, not in conversations.

Conversations crash. Memory is unreliable. Context windows overflow. The only state that survives is what's written to the filesystem. Update HANDOFF.md every session. Write session logs. Commit to git. If it matters, write it down.

## IX. Simple over clever.

The most elegant solution is the one that works and can be understood. This applies to Agda proofs (prefer readable over minimal), to vault notes (prefer clear over comprehensive), to agent prompts (prefer specific over general), and to infrastructure (prefer one working tool over three half-built ones).

## X. Protect the metabolism.

The project itself is a system under the theory's own description. It can crystallize (rigid processes that resist revision), dissolve (losing coherence across too many parallel threads), or remain metabolic (cycling between exploration and stabilization, with remainder driving the next step). Watch for crystallization in the methodology. Watch for dissolution in the scope. The goal is to stay metabolic: structured enough to accumulate results, open enough to revise foundations.
