---
name: idea-brief
description: Use to turn a raw idea, notes file, or early project thought into a portable Markdown idea brief before formal planning begins. Trigger whenever the user says they have an idea and wants to "stabilize it", "work on it", "make an initial document", "create a vision doc", "prepare it for planning", "prepare it for sdd-specify", "turn ideas/foo.md into docs/vision.md", or wants an interview-driven planning seed outside an existing repo. Use this instead of sdd-specify when there is no feature folder yet, no repo context, or the requested output is a general planning artifact rather than docs/features/<slug>/spec.md.
---

# Idea Brief

Create a pre-spec planning document from a rough idea. The output should be useful to any later process: SDD, a product spec, an architecture spike, a research brief, or a manual planning session.

This skill exists because a feature spec is often too late to discover the expensive unknowns. The brief should surface scenario gaps, hidden assumptions, and architecture-affecting risks early without pretending to solve them.

## What This Is

An idea brief is a stable input document. It captures:

- the raw idea and why it matters
- the user or stakeholder problem
- candidate outcomes and non-goals
- scenario coverage, including awkward edge cases
- assumptions that could change the plan
- risks that may force redesign later
- open questions and recommended next planning step

It is not a product requirements document, architecture document, test plan, implementation plan, or acceptance-criteria list. Downstream skills own those.

## Inputs

Accept any of these:

- a raw idea in the prompt
- a path to an idea file, such as `ideas/foo.md`
- a desired output path, such as `researcher/docs/vision.md`
- optional depth: `quick`, `standard`, or `deep`
- optional downstream process, such as SDD, generic PRD, research, or prototype planning

If the source path is provided, read it before interviewing. If the output path is provided, write exactly there. If no output path is provided, ask one concise question for it; if the user explicitly asks you to proceed without asking, write beside the source as `<source-stem>.brief.md` or return the brief inline when there is no source file.

## Protocol

1. **Resolve source, output, and depth.**
   - Identify the idea source and target output path.
   - Default to `standard` depth unless the user asks for quick/deep or the idea clearly has high cost, many stakeholders, sensitive data, or large implementation risk; then recommend `deep` and explain why.
   - State assumptions before writing.

2. **Capture the baseline idea.**
   - Preserve the user's original wording in the brief.
   - Summarize the idea in one neutral paragraph.
   - Do not improve the idea silently; mark inferred improvements as assumptions.

3. **Interview in small batches.**
   Ask only high-value questions. Prefer 2-4 at a time.
   - `quick`: ask only blocking questions, then continue with an assumptions ledger.
   - `standard`: ask 5-8 questions across problem, users, success, scope, and risks.
   - `deep`: ask 10-15 questions across all lenses below, including scenario and redesign risks.

   Cover these lenses:
   - Problem: what pain, trigger, or job creates the need?
   - People: users, buyers, operators, maintainers, reviewers, or other stakeholders.
   - Current alternatives: how the problem is handled today and why that is insufficient.
   - Outcome: what would be observably better if this worked?
   - Scope: first useful version, explicit non-goals, and things to avoid building.
   - Data and trust: sensitive data, source of truth, human review, auditability, retention.
   - Workflow: happy path, interruptions, retries, partial completion, collaboration.
   - Failure: wrong input, unavailable dependency, bad output, misuse, abuse, compliance issue.
   - Change pressure: facts that, if false, would force a different product or architecture.

4. **Run a challenge pass.**
   Before writing the final brief, explicitly test the idea:
   - strongest upside
   - most likely failure path
   - assumption most likely to be false
   - scenario most likely to be missed
   - design or architecture decision most likely to become expensive later

   Keep the critique practical. If the idea is worth continuing, say so and preserve momentum. If it is too vague, write the brief as a discovery artifact and make the gaps visible.

5. **Use external research only when it matters.**
   If the idea depends on current facts, markets, competitors, regulations, pricing, APIs, models, or tool capabilities, verify them with authoritative sources when browsing is available and the user requested or approved research. If research is unavailable or out of scope, mark the relevant claim as unverified instead of inventing confidence.

6. **Draft the document.**
   Read `references/vision-template.md` and follow its structure unless the user requested a different format.
   - Keep the writing concrete and decision-oriented.
   - Separate facts, assumptions, and open questions.
   - Prefer bullets and tables where they improve scanability.
   - Avoid implementation details unless the user supplied them as constraints.

7. **Planning handoff.**
   End with a short next-step recommendation:
   - `sdd-specify` when the brief now has a concrete feature/project boundary.
   - research when the largest risk is market, user, legal, model, or vendor uncertainty.
   - architecture spike when the largest risk is feasibility, integration, source of truth, performance, privacy, or lifecycle.
   - prototype when the largest risk is usability or interaction uncertainty.

   If recommending SDD, include a suggested slug and a 3-6 sentence seed that can be pasted into `sdd-specify`.

8. **Write and verify.**
   Write the brief to the requested path. Then verify:
   - the file exists at the target path
   - all required sections are present
   - raw idea, assumptions, risks, scenarios, open questions, and next step are non-empty
   - the document does not claim unverified research as fact

## Output Rules

- Use Markdown.
- Prefer the title `# Idea Brief: <name>` unless the user requested `vision.md`; in that case use `# Vision: <name>`.
- Keep the brief portable. Do not depend on a repo existing.
- If the output is meant for SDD, keep acceptance criteria out of the brief. Provide SDD seed material instead.
- Every open question should say why it matters and what later work it blocks or influences.
- Risks should include the likely late-stage consequence, not just the risk label.

## Anti-Patterns

- Turning the brief into a full spec with acceptance criteria.
- Choosing architecture, stack, database, framework, or APIs without being asked.
- Asking a long questionnaire before reading the provided idea file.
- Hiding uncertainty by writing polished but unsupported claims.
- Treating "edge cases" as only validation errors; include operational, workflow, trust, and human-review scenarios.
- Writing the document inline when the user gave an output path.

## Definition of Done

- A Markdown brief exists at the requested path, or inline output was explicitly requested.
- The original idea text is preserved or summarized with a clear source reference.
- The document contains scenario coverage, assumptions, risks, open questions, and planning handoff.
- The next step is specific enough that another skill or human planner can continue without reconstructing the idea from the chat.
