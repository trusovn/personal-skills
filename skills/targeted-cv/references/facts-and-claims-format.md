# Facts-and-claims source format

Provide one candidate-specific Markdown file at skill invocation time. This
file is the closed-world authority for CV wording; it is not bundled with the
skill.

Use headings for identity, positioning, chronology, each employer or project,
skills, education, credentials, languages, and application constraints. Put
each claim in a bullet or chronology table row. Mark sensitive or uncertain
claims explicitly.

## Status vocabulary

- `SAFE`: may be used as written or accurately paraphrased.
- `QUALIFIED`: usable only with its limiting qualifier visible.
- `APPLICATION-SPECIFIC`: usable only for an explicitly permitted application.
- `NEEDS CONFIRMATION`: not usable until the user changes its status.
- `DO NOT CLAIM`: never use in a CV.
- `INTERNAL`: context for decision-making; never render it.

Unmarked bullets are rejected unless they sit under an explicitly recognized
safe or qualified heading. Explicit status labels are preferred.

## Minimal fictional example

```markdown
# Candidate CV facts

## Identity and contact

- **SAFE — Name:** Morgan Ibarra
- **SAFE — Base:** Lisbon, Portugal
- **SAFE — Email:** morgan@example.test

## Positioning

- **SAFE:** Test Automation Engineer.
- **SAFE:** Web and backend-service quality engineering.

## Employment chronology

| Period | Company | Safe title |
|---|---|---|
| 2022–Present | Example Systems | Test Automation Engineer |

## Example Systems — 2022 to Present

- **SAFE:** Built Selenium and Java regression tests for web applications.
- **SAFE:** Integrated automated suites into CI pipelines.
- **QUALIFIED:** Docker — hands-on use for local test environments.

## Skills

### Strong commercial / production experience

- Selenium
- Java
- Git

### Do not claim

- Professional German proficiency

## Languages

- **SAFE:** English — C1.

## Application constraints

- **INTERNAL:** Do not disclose compensation expectations in a CV.
```

Chronology rows are treated as `SAFE`. For experience validation, each draft
role's `source_section` must exactly match one heading in the compiled
`section_path` for that employer or project.
