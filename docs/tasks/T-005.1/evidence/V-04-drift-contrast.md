# T-005.1 receipt — V-04 fingerprint-excluded drift contrast

Scenario: a disposable target that passed the V-03 full-projection
installation has one fingerprint-excluded copied eval/setup file changed in
the target only; workflow identity may still match while the canonical
`--check` reports managed drift and the independent comparison names the
changed file (verification `V-04`; brief AC-02; S-02 independent review
probe). No temporary fault is left in a target presented as qualified.

## Mutation and observations

Target: the same disposable committed Git target as the V-03 receipt (all
milestones below observed on it). Mutated file, changed in the target only:

```text
.agents/skills/task-implementation-flow/bounded-task-implementer/evals/evals.json
  (one trailing newline appended to the copied bytes)
```

Observed results in order:

```text
workflow identity (installed .agents/scripts/workflow_version.py):
  fingerprint sha256:a11a7689242a3ecf690971bcf7e85f3e745cebb7ea0168c40dbde08efa717da3
  still equals the source fingerprint: True     <- workflow identity alone cannot detect this drift
canonical --check (read-only):
  exit 1, match=False,
  differences=[{"category": "changed",
                "path": ".agents/skills/task-implementation-flow/bounded-task-implementer/evals/evals.json"}]
independent source-to-target byte comparison:
  names the same file as changed (target bytes differ from the source projection)
```

Conclusion recorded: the earlier V-03 full-match receipt cannot describe the
modified installation as a current qualified input. Workflow identity is a
separate claim; projection identity is judged by the full comparison result
plus the `--check` drift report.

## Read-only and preservation proof around the observation

```text
the drift check repaired nothing: the mutated bytes were still present after --check
AGENTS.md bytes identical across the read-only drift check: True
AGENTS.md outside-block bytes identical across the check: True
  (the follow-up preservation probe on an identically prepared fresh target also
   confirmed the first insertion retains the original unmanaged instruction bytes,
   including terminal trailing whitespace, and outside-block bytes survive checks)
app.txt unmanaged bytes unchanged: True
target Git status across the read-only checks: unchanged (' M AGENTS.md' — the
  documented managed-block insertion from installation; the checks mutated nothing)
target HEAD unchanged: eedafb2dd446dc072c8565b5290a4a26ca954d21
source repository status across the probe: unchanged; active installation untouched
```

## Restoration — no fault left in a target presented as qualified

```text
the mutated file was restored byte-exactly from the source projection
recheck: exit 0, match=True, differences=[]
disposable target removed after the receipts were captured
```

## Evidence limits

This contrast is filesystem/Git proof at the real installer/CLI boundary. It
says nothing about agent behavior; no role call was run, and no live,
networked or model-budget check was used. The active installation in the
source repository was never the mutation target and remains untouched.