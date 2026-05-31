# 2026-05-20 — Tercet strategic pivot from academic-first to B2B-revenue-first

**Session type**: Strategic + product execution
**Duration**: ~half-day
**Trigger**: User named the six-week action-gap between Paris realization (2026-04-15, AI-audience pivot) and any operational change. Theoretical/academic work continued during that window; runway burned without revenue movement. Money pressure made the gap existential.

---

## 1. Strategic decision: Phase A/B bifurcation

The AI-audience pivot established Apr 15 is now operationally bifurcated:

- **Phase A — Immediate revenue (Tercet B2B, May 2026 → ongoing)**: 20 specific buyers in legal tech / medical / compliance / insurance / financial services running LLM classifiers in production. Outreach early next week (Tue–Wed AM). Wait for conversion signal before scaling. RAG public landing second; Merge later. Academic work paused.
- **Phase B — AI-company pitch (late summer / fall 2026)**: Anthropic preferred. Dependency: Phase A produced ≥1 paying customer. arXiv preprint of Two Regimes shelved until endorser surfaces or revenue lands.

Full strategy state in `project_ai_pitch_strategy.md` (updated).

### Academic work paused

Three submissions targeting May 31 dropped — user named "I'm not feeling any of them" pre-dating the pivot itself:
- Phil Psych Imagination / Creativity / AI SI
- Synthese Range of Perception
- Synthese Science-Policy

Drafts exist on disk; not pursuing further. In-flight submissions (Inquiry SI, Synthese Free Will, Open Phil Kant, etc.) ride out passively as CV evidence for Phase B. Accepted presentations (Konstanz, Madrid, ENS, Turin) honored — travel-covered or partial, work largely done.

### Baraghith observation banked

Hannover, 2026-04-09: Baraghith said "you can't think like that, it's too fundamental." Structurally the APQ paper's diagnosis in microcosm — mandate-fidelity selects against agents whose distinctions don't fit the field's index. Confirms the academic-route headwind isn't about quality. AI-industry buyers have the opposite selection pressure (closing problems is the deliverable).

---

## 2. What changed today

### Code

- **Repo rename**: `~/Developer/Symbolics/product-site/` → `tercet-site/`. Updated `package.json` name field. GitHub remote already `SymbolicsLab/tercet-site` so no remote change needed.
- **`app/page.tsx`** — five edits:
  - Hero subhead reframed LLM-forward ("Production reliability for LLM classifiers — and any classifier you ship"); headline ("Know when your model knows.") kept.
  - Result stripe added above the CTAs: `99.2% accuracy on committed predictions · 67% auto-decided · Credit risk, 1,000 applications`.
  - Demo cards: `margin: X · support: Y` line removed.
  - Code section heading: "Four lines to typed uncertainty." → "Four lines to ship."
  - Footer: Symbolics Lab line removed → `© 2026 Tercet`.
  - Pricing restructured (Free killed; 14-day trial banner; annual/monthly toggle; Team $499/$599 with `Save $1,200/yr`; Business $1,999/$2,999 with `Save $12,000/yr`; Enterprise unchanged).

### Files created

- `~/Developer/Symbolics/tercet-site/outreach/email-v1.md` — outreach email template v1 (two subject candidates, body with `[Name]`/`[Company]`/`[their specific use]` placeholders, vertical defaults, open decisions, conversion-criterion checkbox to pre-commit before send).

### Memory updates

- **Updated** `project_ai_pitch_strategy.md` — Phase A/B bifurcation, Baraghith observation.
- **Updated** `project_tercet_launch.md` — new "2026-05-20 Strategic alignment for B2B outreach" section (repo rename, site copy, pricing restructure, outreach plan, NOT-shippable flag).
- **New** `feedback_pricing_altitude.md` — B2B enterprise pricing principle (tier-total > per-unit math).
- **New** `feedback_operational_follow_through.md` — when strategy is settled, foreground operational over theoretical; explicit exception for exhaustion/processing modes.
- **`MEMORY.md`** index refreshed (two updated entries, two new entries). Note: MEMORY.md is now ~29KB vs 24.4KB limit — trim pass on legacy long entries needed at some point.

### OVERVIEW.md

- `### product-site (tercet.dev)` heading → `### tercet-site (tercet.dev)`; Repository Map line updated.
- Active Priorities rows for Phil Psych Imagination, Synthese Range, Synthese Science-Policy marked DROPPED 2026-05-20 (detail preserved for archive).

---

## 3. Open decisions (carry into tomorrow's session)

These are unresolved as of session end:

1. **Subject A/B for outreach.** Two candidates in `outreach/email-v1.md`:
   - "99% accuracy on committed LLM predictions" (recommended primary — body delivers verbatim)
   - "60-point accuracy lift on LLM classification" (variant — bigger hook, soft mismatch with body)
   Decide: lead with 3, or A/B with n=10 each.

2. **Personalization standard for `[their specific use]`.** Verified ("I checked their docs/blog/job listings") vs plausible ("they're in this vertical so probably"). Verified is stronger but slower; plausible scales but accepts higher bounce.

3. **Conversion criterion (pre-commit before send).** What counts as success for the 20-email batch? E.g., ≥3 replies, ≥1 try-page hit traceable to email, ≥1 call booked. Different signals → different next moves. Avoid motivated reasoning later.

4. **Whether to A/B the subject or commit.** Send 10 + 10, or 20 with primary.

---

## 4. Tomorrow's implementation queue (in order)

### Stripe (blocks deploy)

- Create new products at the four new prices:
  - Team / annual / $5,988/yr ($499/mo equivalent)
  - Team / monthly / $599/mo
  - Business / annual / $23,988/yr ($1,999/mo equivalent)
  - Business / monthly / $2,999/mo
- Keep old products around for any in-flight subscriptions (none expected; user count is small).
- Update server-side checkout endpoint to route to new price IDs based on tier + billing period.

### Backend (signup flow)

- New `/signup/trial` endpoint:
  - Accepts email + tier ("team" default)
  - Validates corporate-email-domain (rejects gmail/yahoo/outlook.com personal → returns 422 with message redirecting to `/try`)
  - Enforces one trial per corporate domain (rejects with graceful "company already has a trial" message)
  - Creates API key with `trial_expires_at = now + 14 days`
  - Returns API key (no Stripe redirect)
- Domain-gating logic: maintain blocklist of personal-email domains; check `email.split("@")[1]` against it.

### Site (app/page.tsx, app/try/, etc.)

- `SignupModal`: narrow `tier` type from `"free" | "team" | "business"` to `"team" | "business"`. Add `mode: "paid" | "trial"` flag. Trial mode skips Stripe redirect; shows API key + "Trial expires in 14 days" message.
- All "Start trial" buttons in pricing grid + trial banner → call `onSignup("team", "trial")`.
- Nav "Get API key" button → "Start trial" routing through trial flow.
- Test the full flow with a personal email (should redirect) and a corporate email (should grant trial).

### Infrastructure

- Fly.io: turn warm API back on (`min_machines_running = 1`) on the API service the `/try` page calls. Set budget alert at $30 to catch spikes before they hit the card. Re-evaluate after one week of outreach against actual traffic.

### Email + outreach

- Fresh-eyes pass on `outreach/email-v1.md`. Catch insider language, false notes, awkward asks.
- Decide open decisions (§3 above).
- Research 20 specific companies — defaults by vertical in `email-v1.md`.

### Deploy

- Only push to Vercel after Stripe is aligned. Verify the displayed price matches what Stripe actually charges by testing one end-to-end signup with a real card.

### Theory-track work (deferred)

- Two Regimes arXiv preprint: shelved (needs endorser).
- RAG public landing: second priority after Tercet outreach shows signal.
- Merge public: later still.

---

## 5. Next-session opener (for fresh Claude tomorrow)

Read this file, then `project_ai_pitch_strategy.md` and `project_tercet_launch.md` for full state. Foreground tomorrow's queue (§4). Default to operational moves over theoretical refinement (per `feedback_operational_follow_through.md`). If user opens in theoretical mode, follow them; if user opens neutral, lead with "what's first — Stripe products or the trial endpoint?"

The check at any branching moment: *is this move runway-moving or runway-preserving?* Foreground the first.
