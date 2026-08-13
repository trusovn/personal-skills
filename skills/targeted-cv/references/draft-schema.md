# Targeted CV draft contract

The drafting step writes JSON. `scripts/targeted_cv.py` validates every claim
against the invocation's facts source, fills the placeholder DOCX, records an
evidence ledger, and verifies the output package.

## Commands

```bash
python3 scripts/targeted_cv.py index \
  --facts /absolute/path/facts-and-claims.md \
  --output /tmp/targeted-cv/facts-index.json

python3 scripts/targeted_cv.py build \
  --facts /absolute/path/facts-and-claims.md \
  --draft /tmp/targeted-cv/draft.json \
  --output /absolute/path/Candidate_CV_Company_Role.docx \
  --ledger /tmp/targeted-cv/claim-ledger.json

python3 scripts/targeted_cv.py verify \
  --draft /tmp/targeted-cv/draft.json \
  --output /absolute/path/Candidate_CV_Company_Role.docx \
  --ledger /tmp/targeted-cv/claim-ledger.json
```

The bundled template and contract are defaults. Override both together only
when a replacement template has a matching distilled contract.

## Claim object

Every rendered factual fragment uses this shape:

```json
{
  "text": "Docker hands-on use for local test environments",
  "evidence_ids": ["FC-0123456789ab"],
  "qualification": "hands-on"
}
```

- IDs come from the generated facts index.
- `SAFE` evidence needs no extra flag.
- `QUALIFIED` evidence needs a non-empty `qualification` visible in `title` or
  `text`.
- `APPLICATION_SPECIFIC` evidence needs `"application_specific": true`.
- Rejected and unclassified statuses cannot support a rendered claim.

## Draft JSON

```json
{
  "schema_version": 1,
  "target": {
    "company": "Example Corp",
    "role": "Test Automation Engineer",
    "job_source": "https://example.test/jobs/123"
  },
  "identity": {
    "name": {"text": "Morgan Ibarra", "evidence_ids": ["FC-..."]},
    "tagline": {"text": "TEST AUTOMATION ENGINEER | WEB & API QUALITY", "evidence_ids": ["FC-..."]},
    "location": {"text": "Lisbon, Portugal", "evidence_ids": ["FC-..."]},
    "contact": {"text": "morgan@example.test", "evidence_ids": ["FC-..."]},
    "header": {"text": "Morgan Ibarra | Test Automation Engineer", "evidence_ids": ["FC-..."]}
  },
  "profile": {"text": "Concise evidence-backed profile.", "evidence_ids": ["FC-..."]},
  "expertise": [
    {"title": "Web Automation", "text": "Selenium and Java evidence.", "evidence_ids": ["FC-..."]}
  ],
  "experience": [
    {
      "source_section": "Example Systems — 2022 to Present",
      "title": "Test Automation Engineer",
      "employer": "Example Systems",
      "dates": "2022–Present",
      "header_evidence_ids": ["FC-..."],
      "bullets": [
        {"text": "Built Selenium and Java regression tests.", "evidence_ids": ["FC-..."]}
      ],
      "environment": {"text": "Selenium, Java, Git", "evidence_ids": ["FC-..."]}
    }
  ],
  "strengths": [
    {"text": "Automation design backed by role evidence.", "evidence_ids": ["FC-..."]}
  ],
  "skills": [
    {"title": "Automation", "text": "Selenium, Java", "evidence_ids": ["FC-..."]}
  ],
  "certificates": {"text": "Not listed", "evidence_ids": ["FC-..."]},
  "languages": {"text": "English — C1", "evidence_ids": ["FC-..."]},
  "availability": {"text": "Based in Lisbon.", "evidence_ids": ["FC-..."]}
}
```

`expertise` must contain exactly six entries. A role bullet or environment must
cite at least one allowed fact whose `section_path` contains that role's exact
`source_section`; this prevents borrowing evidence from another employer.

The ledger is an audit artifact, not CV content. It records each rendered claim
and the exact supplied evidence cited for the final semantic review.
