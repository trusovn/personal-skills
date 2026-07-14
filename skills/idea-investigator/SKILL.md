---
name: idea-investigator
description: Investigate software, product, startup, monetization, automation, or project ideas using a STORM-inspired multi-perspective research loop. Use this skill whenever the user asks whether an idea is worth building, how to validate or monetize it, what is missing, what would it take for it to succeed, how it compares to alternatives, or wants an idea turned into an evidence-backed Markdown brief. Guide the user with concise questions and pros/cons when choices matter, then produce a decision-oriented report rather than a polished generic article.
---

# Idea Investigator

Use this skill to turn a raw idea into a practical investigation: what must be true, what evidence exists, what is missing, what it would take to make the idea successful, and what the next decision should be.

This skill borrows the useful part of Stanford STORM-style research: multi-perspective question asking and source-grounded synthesis. It changes the objective. STORM aims to produce a comprehensive article; this skill aims to reduce decision uncertainty for a product, software, monetization, automation, or project idea.

## Core stance

Optimize for a decision, not a beautiful report.

The output should help the user decide one of:

- Proceed: the idea has enough support for the next investment.
- Proceed with guardrails: the idea is promising but specific risks must be tested first.
- Pivot: the problem or segment seems real, but the proposed solution, monetization, or distribution path is weak.
- Park: the idea may be viable later, but prerequisites are missing.
- Stop: the idea is not worth further work as currently framed.

Do not treat desk research as validation. Research can find competitors, patterns, regulations, pricing anchors, and risks; it cannot prove that users will care, switch, or pay. Convert unresolved assumptions into experiments.

## Start by framing the investigation

If the user already gave enough context, proceed and state assumptions. If important context is missing, ask concise questions before deep research. Ask no more than five at once.

Useful opening questions:

1. What is the idea in one or two sentences?
2. Who is the target user or buyer?
3. What is the intended purpose: monetization, internal productivity, learning, portfolio, community, or something else?
4. What constraints matter: time, budget, solo/team, platform, geography, legal/privacy, technical stack, or launch deadline?
5. What depth do they want?

When depth matters, guide with options:

- Quick scan: fastest; good for early triage; can miss demand and switching friction.
- Validation plan: best default; combines research with experiments; requires follow-up with users or prototypes.
- Build/investment brief: deeper market, economics, technical, and risk analysis; slower; useful before committing serious time or money.

If the user does not choose, default to "Validation plan" for commercial ideas and "Quick scan" for lightweight personal projects.

## Adapted STORM workflow

Use this pipeline:

1. Capture the thesis.
   - Restate the idea as: "For [target user], build [solution] to solve [problem], succeeding if [measurable outcome]."
   - If monetization is relevant, include the likely buyer, pricing motion, and payment trigger.

2. Identify perspectives.
   - End user: pain, frequency, urgency, workflow, alternatives.
   - Buyer or economic owner: budget, willingness to pay, ROI, procurement friction.
   - Competitor and substitutes: direct competitors, manual workarounds, status quo, open-source alternatives.
   - Distribution: where users are reachable, acquisition cost, trust requirements, partnerships, platform dependency.
   - Technical feasibility: MVP complexity, integrations, data needs, reliability, security, maintenance.
   - Legal/privacy/compliance: regulated data, licensing, scraping, consumer protection, payments, jurisdiction.
   - Operations/support: onboarding, support burden, abuse/fraud, refunds, content moderation, data quality.
   - Founder/project fit: skills, unfair advantage, motivation, time budget, access to users.

3. Generate assumption-testing questions.
   - Ask questions that can change the decision.
   - Prefer "what would disprove this?" over "how could this work?"
   - Include at least one question from each relevant perspective.

4. Gather evidence.
   - Use current external sources when facts may change: market conditions, laws, APIs, prices, competitors, platform rules, model capabilities, and security standards.
   - Prefer primary or authoritative sources when available.
   - Separate facts, inferences, and guesses.
   - If browsing or source access is unavailable, mark claims as "needs verification" rather than presenting them as known.

5. Build an evidence ledger.
   Track claims in this form:
   - Claim
   - Supporting evidence
   - Conflicting evidence
   - Source quality
   - Confidence
   - What would falsify it

6. Red-team the idea.
   - Identify fatal flaws, not just generic risks.
   - Look for demand risk, switching cost, distribution bottlenecks, weak monetization, technical infeasibility, legal exposure, and founder-fit mismatch.
   - Distinguish fatal, fixable, and monitor-only risks.

7. Convert uncertainty into next actions.
   - Recommend the cheapest credible experiment for each critical unknown.
   - Examples: user interviews, concierge/manual workflow, landing page, pricing conversation, prototype, technical spike, competitor teardown, compliance review.
   - Define success/failure thresholds before suggesting more building.

8. Produce the decision brief.
   - Keep it concise enough to act on.
   - Put the decision and strongest reasons near the top.
   - Include "what is missing / needed / would it take" as a first-class section.

## How to guide the user

Ask questions when the answer would materially change the investigation. Otherwise, make a reasonable assumption, label it, and continue.

When presenting choices, show compact pros/cons and a recommended default. For example:

- Narrow niche first: lower build and acquisition risk; smaller market; best when demand is uncertain.
- Broad horizontal tool: bigger upside; harder positioning and distribution; best when the user already has an audience or strong channel.
- Internal tool first: easier validation and lower sales friction; monetization may be indirect; best when the user wants operational leverage.

Do not overwhelm the user with a long questionnaire. Use staged questions: ask the minimum needed now, then ask deeper questions only after an initial map reveals the bottleneck.

## Evidence standards

Use these guardrails:

- A competitor's existence is not proof of demand; it is evidence that someone believes demand exists.
- Positive comments are not willingness to pay.
- A large market is not reachable distribution.
- A technically possible MVP is not a viable product.
- User pain without urgency usually does not convert.
- Monetization must identify the payer, payment trigger, pricing basis, and reason to switch.
- "AI can do it" is not a feasibility argument unless data quality, latency, cost, reliability, and evaluation are addressed.

When facts are current or high-stakes, verify them. If you cannot verify them, state the uncertainty explicitly.

## Markdown report format

Use this structure for the final report. If the user asks for a file, write it as Markdown. If no path is specified and writing files is allowed, use `idea-investigation-<slug>.md` in the current working directory; otherwise provide the report in chat.

```markdown
# Idea Investigation: [Idea Name]

## Executive verdict
[Proceed / Proceed with guardrails / Pivot / Park / Stop]

Short rationale:
- [Reason 1]
- [Reason 2]
- [Reason 3]

## Working thesis
- Target user/buyer:
- Problem:
- Proposed solution:
- Success definition:
- Monetization or purpose:
- Key assumptions made:

## What must be true
| Assumption | Why it matters | Current confidence | What would falsify it |
|---|---:|---:|---|
| ... | ... | Low/Medium/High | ... |

## Evidence summary
| Claim | Evidence found | Conflicting evidence / caveat | Source quality | Confidence |
|---|---|---|---|---|
| ... | ... | ... | Low/Medium/High | Low/Medium/High |

## Perspective analysis
### User/problem
[Pain frequency, urgency, workflow, alternatives.]

### Buyer/monetization
[Payer, budget, pricing basis, ROI, willingness-to-pay risks.]

### Market and alternatives
[Competitors, substitutes, status quo, differentiation.]

### Distribution
[Reachable channels, trust requirements, acquisition risks.]

### Technical feasibility
[MVP scope, integrations, data, reliability, maintenance.]

### Legal/privacy/operations
[Compliance, platform rules, support, abuse, refunds, data quality.]

## Fatal flaws and fixable risks
| Risk | Severity | Why it matters | Mitigation or test |
|---|---|---|---|
| ... | Fatal/Fixable/Monitor | ... | ... |

## What is missing / needed / what it would take
### Missing evidence
- ...

### Needed capabilities or assets
- ...

### Needed resources
- Time:
- Budget:
- Skills:
- Access to users/data/channels:
- Partnerships/integrations:

### What it would take to become a successful project
- Product:
- Distribution:
- Monetization:
- Technical:
- Operational/legal:

## Recommended validation plan
| Step | Goal | Method | Success threshold | Stop/pivot signal |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

## Decision and next move
[Concrete next action, owner if known, and what to decide after it.]

## Open questions for the user
- [Only questions that would materially change the plan.]
```

## File handling

If the user explicitly asks for a `.md` file or artifact:

- Prefer one self-contained Markdown file.
- Use the user's requested path when provided.
- If no path is provided, choose a clear local filename such as `idea-investigation-<slug>.md`.
- Do not create a full project structure unless the user asks for one.

## Lightweight examples

**User:** "I have an idea for an AI tool that summarizes Slack threads for managers. Can this be monetized?"

**Approach:** Frame the buyer, identify assumptions about pain frequency and willingness to pay, compare against Slack-native features and workflow tools, check privacy/security friction, then recommend interviews or a concierge prototype before building.

**User:** "Investigate this app idea and make an md report."

**Approach:** Ask only for missing essentials, choose a sensible depth, research current competitors and platform constraints if browsing is available, and write the report using the template above.

**User:** "Should I build this as a SaaS or a local-first desktop tool?"

**Approach:** Compare both paths by user trust, distribution, monetization, support burden, data sensitivity, implementation complexity, and switching friction; recommend the default only after exposing tradeoffs.
