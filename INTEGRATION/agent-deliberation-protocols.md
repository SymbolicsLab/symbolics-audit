# Symbolics: Agent Deliberation Protocols
**Version**: 0.2.0 | **Date**: 2026-01-31

Structured reasoning patterns for agents other than Claude Code.
Claude Code's deliberation is handled by its operating modes in `SymbolicsLab/CLAUDE.md`
(PROOF, VAULT-PREP, REASON modes with enforced output structures).

This document covers: Cowork, ChatGPT, Gemini, Codex, and cross-agent patterns.

---

## Cowork: Vault Engine + Theory Writer

### When Creating a New Vault Note from a Scattered Insight

```
DELIBERATION: NEW-NOTE-FROM-INSIGHT
1. READ Vault/CLAUDE.md — refresh conventions (do this every time, don't rely on memory)
2. READ the scattered insight entry in full
3. READ the source material (abstract, paper section, etc.)
4. DETERMINE note type: concept, mechanism, distinction, claim, example, author, source
   - Match to the type whose body structure best fits the content
5. SURVEY existing related notes:
   - Which canonical notes does this connect to?
   - Does it update/conflict with any existing note?
   - If it updates an existing note → use REVISION workflow instead
6. DRAFT the note:
   - Complete frontmatter per vault CLAUDE.md (including type-specific fields)
   - promote_to: [correct folder]
   - spec_links: [known SPEC or "pending"]
   - related: [[existing notes]]
   - Body follows the type-specific structure exactly
   - Include cross-references via [[WikiLinks]]
7. SELF-REVIEW against conventions:
   - [ ] Frontmatter complete and correct for this type?
   - [ ] Body structure matches type template?
   - [ ] Citations follow policy (extracted from source, not reconstructed)?
   - [ ] Cross-references are bidirectional where appropriate?
   - [ ] spec_links present?
   - [ ] Claude's provisional note included only if genuinely warranted?
   - [ ] Filename is correct for one-click promotion?
8. WRITE to 00_inbox/drafts/[Filename].md
```

### When Producing a Revision of an Existing Canonical Note

```
DELIBERATION: REVISION
1. READ Vault/CLAUDE.md revision workflow section
2. READ the existing canonical note in full
3. READ the new material that motivates the revision
4. PLAN the revision:
   - What is being added/changed/removed?
   - Does this change the note's scope, type, or cross-references?
   - Could this revision introduce inconsistency with other canonical notes?
5. DRAFT complete replacement note:
   - Same filename as canonical note
   - Full frontmatter with `revises:` field pointing to canonical path
   - Complete body (not a patch — full standalone note)
   - Changelog section listing all changes with reasons
6. SELF-REVIEW:
   - [ ] Is this a complete standalone note (not a diff)?
   - [ ] Does the changelog accurately describe all changes?
   - [ ] Are cross-references updated?
   - [ ] Is spec_links preserved or updated?
7. WRITE to 00_inbox/drafts/[Same Filename].md
```

### When Generating state.yaml (Emergency: orchestrator session ended without updating)

```
DELIBERATION: STATE-YAML-GENERATION
1. READ all INTEGRATION documents:
   - orchestration-framework.md
   - completeness-map.md
   - open-problems.md
   - scattered-insights.md
   - Latest session log in session-logs/
2. CHECK vault state:
   - Count canonical notes (ls 01_concepts/ 02_mechanisms/ etc.)
   - Count pending drafts (ls 00_inbox/drafts/)
   - Any active tasks (ls 00_inbox/_tasks/)
3. CHECK code state:
   - Any uncommitted changes in symbolics-core?
   - Any open branches?
4. REWRITE state.yaml completely (never patch):
   - Update last_updated, last_session, last_agent
   - Update vault counts
   - Update current_context from latest session log
   - Update active_threads statuses
   - Update next_actions from session log "Next" + open-problems priorities
   - Update agent_status from session log "Agents used"
   - Update flags from session log "Flags" + ongoing concerns
5. Keep it FLAT — no nesting deeper than 2 levels
```

### When Writing Long-Form Theory (Dossier sections, papers)

```
DELIBERATION: THEORY-WRITING
1. GATHER all relevant vault notes (canonical > drafts)
2. GATHER relevant INTEGRATION docs for formal status
3. IDENTIFY the audience: academic reviewers? Anthropic? Internal reference?
4. OUTLINE before writing:
   - What claims are being made?
   - What is the evidence for each? (vault notes, Agda proofs, experiments)
   - What is the honest epistemic status of each claim?
5. DRAFT with honesty markers:
   - "Verified" / "Proven" — only for type-checked Agda results
   - "Established" — for well-developed theory with formal backing
   - "Proposed" — for theoretical claims without full formalization
   - "Conjectural" — for ideas still being explored
   - "Open" — for unresolved questions
6. SELF-REVIEW:
   - Does every strong claim have traceability to evidence?
   - Is anything overstated relative to its actual status?
   - Does it read clearly to someone unfamiliar with the system?
```

---

## ChatGPT: Theory Consultant

(These protocols are for the orchestrator to keep in mind when generating prompts — ChatGPT doesn't receive them directly.)

### When Asking for Theory Critique

```
ORCHESTRATOR DELIBERATION: CHATGPT-CRITIQUE
1. FRAME the question in user's voice
2. PROVIDE enough context for ChatGPT to engage deeply
   - What's the claim being examined?
   - What's the current evidence/argument for it?
   - What specifically needs scrutiny?
3. EXPLICITLY ask for pushback: "Be honest if you think I'm wrong"
4. AFTER receiving response:
   - Separate structural insights (trust these) from formal claims (verify independently)
   - If ChatGPT raises a concern the orchestrator hasn't considered → promote it
   - If ChatGPT becomes protective/defensive → rephrase and try again, or note the limitation
```

### When Asking for Connection-Finding

```
ORCHESTRATOR DELIBERATION: CHATGPT-CONNECTIONS
1. IDENTIFY the two (or more) concepts to connect
2. PROVIDE what's known about each
3. ASK specifically: "What am I missing?" or "How do these relate structurally?"
4. AFTER receiving response:
   - Evaluate: is this a genuine structural connection or a surface similarity?
   - If genuine → route to appropriate open problem or vault note
   - If surface → discard (don't add noise)
```

---

## Gemini: Research Engine

### When Conducting a Literature Survey

```
ORCHESTRATOR DELIBERATION: GEMINI-SURVEY
1. FORMULATE a precise research question (not a vague topic)
2. SPECIFY what's already known (avoid redundant results)
3. SPECIFY what counts as relevant (criteria for useful results)
4. AFTER receiving results:
   - Assess quality: primary sources > aggregators
   - Check for genuinely related work vs. keyword overlap
   - Route findings to appropriate INTEGRATION doc or open problem
   - Flag any result that suggests the theory's claimed novelty isn't novel
```

---

## Codex: Code Reviewer

### When Reviewing Agda

```
ORCHESTRATOR DELIBERATION: CODEX-REVIEW
1. PROVIDE the Agda module(s) to review
2. SPECIFY what the code is supposed to prove/implement
3. ASK specifically:
   - "Are there hidden assumptions?"
   - "Is there a simpler way to do this?"
   - "What edge cases aren't covered?"
4. AFTER receiving response:
   - Cross-check with Claude Code's understanding
   - If disagreement → run the type-checker; proof wins
```

---

## Cross-Agent Deliberation

### Convergence Protocol (The "Council")

When a question needs input from multiple agents (e.g., "Is FDE the right logic?"),
use a Map-Reduce pattern:

```
ORCHESTRATOR DELIBERATION: CONVERGENCE
1. FORMULATE one clear question
2. SEND to agents independently:
   - Do NOT share one agent's answer with another
   - Each agent gets the same context and question
   - For ChatGPT: frame in user's voice
3. COLLECT responses
4. COMPARE:
   - Where do they agree? → Higher confidence
   - Where do they disagree? → This is where the real question is
   - Where does one see something the others miss? → Investigate further
5. SYNTHESIZE: Present the convergence/divergence to user
6. USER decides (Principle III: user's intuition is final authority)
```

**Automation option (future):** Build a Council script (~100 lines TypeScript)
that takes a question, queries multiple models via API, and produces a
synthesis document in `INTEGRATION/_council/`. See orchestration-framework.md §Council Pattern.

### Escalation Protocol

When an agent encounters something unexpected or beyond its scope:

```
DELIBERATION: ESCALATION
1. AGENT flags the issue clearly: "I expected X but found Y"
2. ORCHESTRATOR assesses:
   - Is this a bug? → Fix it
   - Is this a genuine theoretical question? → Route to ChatGPT or user
   - Is this a formal gap? → Add to open problems
   - Is this a risk? → Add to state.yaml flags
3. DO NOT silently work around unexpected results
```
