---
name: ask-user-questions
description: >
  Use whenever an agent needs user clarification before safely continuing, especially when
  a task has multiple plausible interpretations, irreversible or high-blast-radius choices,
  missing required inputs, or a decision should be explicitly confirmed. This skill provides
  an AskUserQuestions-style interaction contract: ask the fewest useful questions, offer
  clear recommended options when possible, explain the consequence of each choice, and then
  continue from the user's answer. Use it for specs, implementation planning, code review
  follow-ups, product decisions, migration choices, permissions, and any workflow that says
  "AskUserQuestion", "AskUserQuestions", "clarify with the user", or "confirm before
  proceeding".
---

# Skill: ask-user-questions

Ask focused questions only when the answer materially affects the work. The goal is to unblock progress without turning the session into an interview.

This skill mirrors the useful parts of Claude's `AskUserQuestions` pattern for environments that may or may not expose a native question tool.

## Decision Boundary

Ask the user when at least one of these is true:

- The request has two or more reasonable interpretations that would produce meaningfully different work.
- A choice is expensive to undo, security-sensitive, destructive, user-visible, or likely to affect architecture.
- A required input cannot be discovered from local context.
- The user explicitly asks to be consulted, approve, confirm, choose, or resolve an ambiguity.
- You are about to encode a product, domain, or policy decision that should belong to the user.

Do not ask when a conservative assumption is obvious, cheap to reverse, and can be stated in the next update.

## Question Protocol

1. Name the blocker in one sentence.
2. Ask no more than three questions at once; prefer one.
3. For each question, provide two or three concrete choices when the choice space is clear.
4. Put the recommended option first and label it `(Recommended)`.
5. Explain each option's consequence in one short sentence.
6. Include an `Other` path only as free-form text, not as a listed option, unless the UI tool adds it automatically.
7. After the user answers, restate the decision briefly and continue.

When a native structured question tool is available, use it. In Codex Plan mode, prefer `request_user_input` for short multiple-choice questions. Outside that mode, ask in plain text using the same structure.

## Plain-Text Format

Use this format when no structured question tool is available:

```text
I need one decision before I edit this because <reason>.

Question: <short question>
- <Option A> (Recommended): <impact/tradeoff>
- <Option B>: <impact/tradeoff>
- <Option C>: <impact/tradeoff>

You can also answer with a custom choice.
```

For open-ended required input, skip fake options:

```text
I need one missing input before I can continue: <what is missing and why>.

Question: <specific request>
```

## Option Quality

Good options are mutually exclusive, concrete, and action-oriented.

Prefer:

- `Patch only this endpoint`: Smallest change; leaves shared behavior untouched.
- `Update the shared validator (Recommended)`: Fixes every entry point that accepts this payload.

Avoid:

- `Yes`: Ambiguous once the conversation scrolls.
- `Best practice`: Hides the actual consequence.
- `Other`: The user can always type a custom answer.

## Autonomy Rules

If the user does not respond and the environment allows continued work, proceed only when a safe default exists. State the assumption and keep the change reversible.

If no safe default exists, stop and wait. Do not fabricate domain facts, credentials, policy choices, migration strategy, data retention rules, legal interpretations, or product acceptance criteria.

## Examples

**Ambiguous implementation scope**

```text
I need one scope decision before I edit this because either choice changes different files.

Question: Where should the validation live?
- Service layer (Recommended): Covers API and scheduled imports with one rule.
- Controller only: Smaller patch, but imports can still accept invalid data.
- Database constraint: Strongest enforcement, but requires a migration.

You can also answer with a custom choice.
```

**Missing required input**

```text
I need one missing input before I can continue: the destination branch is not inferable from the repo.

Question: Which branch should I target for the PR?
```

**Confirmation before destructive work**

```text
I need confirmation before deleting generated files because this cannot be confidently separated from user edits.

Question: Should I remove the generated reports directory?
- Leave it in place (Recommended): Avoids deleting anything user-created.
- Delete only files matching the generator timestamp: Cleans the current run while reducing risk.
- Delete the whole directory: Fastest cleanup, but may remove manual files.

You can also answer with a custom choice.
```

## Definition of Done

- The question is necessary, specific, and tied to a decision that affects the work.
- The user can answer quickly without decoding hidden assumptions.
- Recommended options are justified by impact, not preference.
- The agent resumes work from the answer and records any assumption that shaped the result.
