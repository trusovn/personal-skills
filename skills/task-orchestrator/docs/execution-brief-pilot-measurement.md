# Execution-Brief Pilot Measurement

Use this note after each brief. Do not include it in the worker prompt.

## Session record

| Session role | Session file | Tool calls | Final context input | Quota start | Quota end | Delta |
|---|---|---:|---:|---:|---:|---:|
| implementation | `<rollout-...jsonl>` |  |  |  |  |  |
| first review | `<rollout-...jsonl>` |  |  |  |  |  |
| review fix | `<rollout-...jsonl or N/A>` |  |  |  |  |  |

- First independent review: `PASS | CHANGES REQUESTED | not run`
- Passed first review: `yes | no | not reviewed`
- Review-rework calls: `<sum of tool calls in review-fix sessions; 0 if passed>`
- Task result: `accepted | blocked | abandoned`
- Boundary adjustment for the next task: `<none or one concrete change>`

Measure each session separately. Do not run sessions concurrently, because a
shared quota change could not then be attributed reliably.

## Measure one session

Replace `<session.jsonl>` with the session trace path and run:

```sh
jq -s '
  def tokens: [.[] | select(.type == "event_msg" and .payload.type == "token_count")];
  {
    tool_calls: ([.[] | select(.type == "response_item" and .payload.type == "custom_tool_call")] | length),
    final_context_input: (tokens | last | .payload.info.last_token_usage.input_tokens),
    quota_start: (tokens | first | .payload.rate_limits.primary.used_percent),
    quota_end: (tokens | last | .payload.rate_limits.primary.used_percent),
    quota_delta: ((tokens | last | .payload.rate_limits.primary.used_percent) -
                  (tokens | first | .payload.rate_limits.primary.used_percent))
  }
' <session.jsonl>
```

The quota values are coarse and the first value is observed after the session's
first model interaction. Use them for comparison, not exact accounting.

## Interpret the first three briefs

- Worker budget signal: implementation session at or below 35 tool calls and
  100,000 final context input tokens.
- First-review pass rate: briefs passing their first independent review divided
  by briefs independently reviewed.
- Review-rework ratio: review-fix tool calls divided by implementation tool
  calls. Lower is better; investigate task boundaries when it exceeds 25%.
- Quota delta: observe implementation, review, and fixes separately. Do not use
  2 percentage points as a hard gate until the pilot establishes a baseline.

After the third brief, change task boundaries or agent/reasoning selection when
the same budget or review failure repeats. Do not respond by lengthening every
brief.
