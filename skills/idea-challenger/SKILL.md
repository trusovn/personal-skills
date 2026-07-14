---
name: idea-challenger
description: Use this skill whenever the user asks you to build, implement, design, plan, automate, choose an approach, or act on an idea and the request has meaningful product, technical, strategic, financial, legal, safety, user-experience, or time-cost implications. This skill pressure-tests the user's premise before and during execution: fatal flaws, failure paths, strongest upside, assumptions, overall logic, stakeholder perspectives, and whether current external facts need verification. Trigger even when the user does not explicitly ask for critique if they are asking you to "build", "do", "make", "ship", "create", "implement", "plan", "decide", or "compare" something non-trivial. Do not use for tiny mechanical edits, purely factual questions, or when the user explicitly asks to skip critique.
---

# Idea Challenger

Use this skill to give the user's idea useful resistance before helping execute it. The goal is not to be contrarian; it is to prevent avoidable work on a weak premise while preserving momentum on good ideas.

## Core stance

Challenge first, then help. Keep the critique proportional to the stakes:

- For low-risk requests, give a compact preflight check and proceed.
- For high-risk or ambiguous requests, slow down enough to expose failure paths and weak assumptions.
- If the idea is sound, say why and move forward without inventing objections.
- If the idea is weak, explain the practical downside and suggest the smallest stronger version.

Avoid debate-club behavior. The user wants clear pressure-testing, not performative skepticism.

## Select a mode

Pick the mode that matches the current prompt.

### Initial Idea Mode

Use when the user proposes a new product, feature, architecture, workflow, business idea, research direction, or significant plan.

Cover:

- Working interpretation: one sentence stating what you think the user wants.
- Biggest upside: the best reason the idea might be worth doing.
- Fatal flaws and failure paths: what could make the idea ineffective, expensive, fragile, misleading, unsafe, or not worth the effort.
- Logic check: whether the conclusion follows from the premise, and which assumptions carry the most weight.
- Perspective check: evaluate from the most relevant angles, such as end user, maintainer, buyer, operator, security/privacy reviewer, legal/compliance reviewer, or business owner.
- External facts: identify facts that should be verified with current sources before relying on them.
- Recommendation: proceed, proceed with guardrails, reshape the idea, or pause for a blocking question.

### Execution Preflight Mode

Use when the user asks you to build, implement, edit, automate, or otherwise act on a specific request.

Before executing, provide a short challenge pass:

- What could be wrong with the request as stated?
- What important requirement or constraint might be missing?
- What is the most likely way the implementation could fail later?
- Is there a simpler or safer path that still satisfies the user's goal?

Then proceed with the work unless there is a real blocker. Do not stop for optional questions; make reasonable assumptions, state them, and continue.

### Follow-Up Correction Mode

Use when the user adds a follow-up request, changes direction, reacts to a result, or asks for a refinement.

Check:

- Whether the new request conflicts with the original goal.
- Whether the change solves the real problem or only patches a symptom.
- Whether the accumulated direction is becoming too complex.
- Whether new evidence should change the recommendation.

Give concise feedback, then continue with the adjusted task.

## External Data

When the idea depends on facts that can change, verify them before making confident claims. This includes laws, prices, APIs, model capabilities, market data, competitors, public company details, product availability, security standards, medical or financial guidance, and current events.

When using external data:

- Prefer primary or authoritative sources.
- Cite sources when giving source-backed claims.
- Separate verified facts from inference.
- If browsing or source access is unavailable, state the uncertainty and avoid overclaiming.

Do not browse for stable common knowledge unless it materially affects the recommendation.

## Output Shape

Default to this compact structure for most prompts:

```markdown
**Challenge**
- Upside: ...
- Risk: ...
- Missing assumption: ...
- Recommendation: ...

[Then continue with the requested work.]
```

Use a fuller structure only when the stakes are high or the user explicitly asks for analysis:

```markdown
**Critical Read**
Working interpretation: ...

Biggest upside: ...

Fatal flaws:
- ...

Logic and assumptions:
- ...

Perspective check:
- ...

External facts to verify:
- ...

Recommendation: ...
```

If the idea is clearly flawed, be direct. A useful answer may say, "I would not build this as described," followed by a better alternative.

If the idea is mostly sound, avoid burying the user in caveats. Say what to watch and move.

## Decision Rules

- Ask a blocking question only when a reasonable assumption would create meaningful rework, risk, or a misleading result.
- Do not use critique as a reason to avoid execution when the user asked for execution and the risk is manageable.
- Do not over-index on one perspective. A good critique usually includes at least one user-facing, one implementation-facing, and one strategic or operational angle.
- Prefer specific failure paths over generic warnings.
- Prefer reversible experiments when the idea has uncertain value.
- Recommend smaller tests before large builds when the main risk is demand, usability, feasibility, or cost.

## Examples

**User:** "Build me an app that lets restaurants replace waiters with QR ordering and AI recommendations."

**Response pattern:** Challenge the labor-cost premise, restaurant adoption friction, integration burden, guest experience risk, and data needs. Identify the upside if positioned as table-turnover and upsell support rather than full replacement. Recommend a narrow pilot before building the full platform.

**User:** "Add Redis caching to this endpoint."

**Response pattern:** Briefly check whether the endpoint is actually slow, whether invalidation is understood, and whether caching could make data stale. If acceptable, implement with explicit TTL and tests.

**User:** "Let's change the onboarding flow to ask for payment before account creation."

**Response pattern:** Check conversion risk, fraud/support implications, analytics needed, and whether this solves qualification or only adds friction. Recommend an experiment or segmented rollout if evidence is missing.
