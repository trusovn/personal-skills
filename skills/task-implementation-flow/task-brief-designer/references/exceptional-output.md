# Exceptional responses

Read before returning a direction-delta-needed or blocked-design response.
The entry direction-authority check takes precedence over blocked design.

When supplied direction does not authorize a needed product, priority,
assurance, trust, intervention, or scope choice, return only:

```markdown
# Direction delta needed: `<requested task>`

- Governing direction: `<exact source and relevant section>`
- Missing decision: `<plain-language choice the task cannot make>`
- Why it matters: `<practical consequence for the owner or user>`
- Options: `<concise choices and their practical tradeoffs>`
- Recommendation: `<optional and clearly non-authoritative, or none>`
- Downstream impact: `<briefs or plans that may need review>`
- Owner action: `<smallest decision or direction update needed>`
```

This is a routing response, not a task brief. Return it in the conversation and
leave the requested task path absent or unchanged. Write a durable delta only
when the user explicitly requests a separate direction-delta artifact path;
never store it at the requested implementation-task path.

## Blocked response limits

For `blocked_design`, return only the requested outcome as stated, the missing
decisions or authority, their owner, and the smallest planning action. Omit
launch metadata, readiness routing, proposed architecture, implementation
scope or paths, work items, implementation ACs, finite-risk coverage,
verification obligations, and implementation handoff language. Those details
would turn an unapproved premise into apparent authority.

## Blocked design

Use only the abbreviated form below; direction gaps use the skill's
conversation-only direction-delta response instead.

```markdown
# Design block: <requested outcome as stated>

Status: `blocked_design`

## Missing decisions or authority

- <decision or authority gap; why it materially changes the task>

## Owner and smallest next action

- Owner: <user or decision owner>
- Next: <smallest planning/approval action; proof-task dependency if required>
```
