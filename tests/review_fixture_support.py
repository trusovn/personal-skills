"""Shared repository-test support for the review-flow owning modules.

Holds the repository root, the acceptance/discovery package paths, and the
small text/fixture helpers shared by several owning test modules. Skill eval
setup programs stay self-contained and must not depend on this module.
"""

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLOW = ROOT / "skills" / "task-implementation-flow"
ACCEPTANCE_PACKAGE = FLOW / "task-acceptance-review"
ACCEPTANCE_SKILL = ACCEPTANCE_PACKAGE / "SKILL.md"
ACCEPTANCE_EVALS = ACCEPTANCE_PACKAGE / "evals" / "evals.json"
ACCEPTANCE_FIXTURE = ACCEPTANCE_PACKAGE / "evals" / "files" / "setup_fixture.py"
DISCOVERY_PACKAGE = FLOW / "task-review-discovery"
DISCOVERY_SKILL = DISCOVERY_PACKAGE / "SKILL.md"
DISCOVERY_REPORT_TEMPLATE = DISCOVERY_PACKAGE / "references" / "discovery-report-template.md"
DISCOVERY_EVALS = DISCOVERY_PACKAGE / "evals" / "evals.json"
DISCOVERY_FIXTURE = DISCOVERY_PACKAGE / "evals" / "files" / "setup_fixture.py"
SENIOR_REVIEW_SKILL = ROOT / "skills" / "senior-code-review" / "SKILL.md"
PREFLIGHT_EVALS = FLOW / "task-preflight" / "evals" / "evals.json"
ACCEPTANCE_VERDICT_TOKENS = ("`ACCEPT`", "`CHANGES_REQUESTED`", "`INCONCLUSIVE`")


CONTEXTUAL_CONTRAST_SETUPS = {
    "consequential-uncertainty-resolved-decision": "uncertainty_contrast",
    "serious-delay-uncertainty-decision": "uncertainty_contrast",
    "serious-delay-uncertainty-resolved-decision": "uncertainty_contrast",
    "known-issue-proposed-work-decision": "known_issue_context",
    "known-issue-committed-work-decision": "known_issue_context",
    "known-issue-priority-only-decision": "known_issue_context",
    "known-issue-no-links-decision": "known_issue_context",
    "repeated-review-formerly-blocked-evidence-decision": "repeated_review",
    "repeated-review-missed-existing-obligation-decision": "repeated_review",
    "repeated-review-changed-context-authority-decision": "repeated_review",
    "repeated-review-newly-demonstrated-material-risk-decision": "repeated_review",
}



def normalized(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).strip()



def fixture_functions(text: str) -> dict:
    tree = ast.parse(text)
    return {
        node.name: ast.get_source_segment(text, node)
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }



if __name__ == "__main__":
    unittest.main()
