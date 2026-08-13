from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "targeted_cv.py"
TEMPLATE = SKILL / "assets" / "targeted-cv-template.docx"
CONTRACT = SKILL / "assets" / "template-contract.json"


def load_subject():
    spec = importlib.util.spec_from_file_location("targeted_cv", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


FACTS = """
# Morgan Ibarra — CV facts

## 1. Identity and contact

- **SAFE — Name:** Morgan Ibarra
- **SAFE — Base:** Lisbon, Portugal
- **SAFE — Email:** morgan@example.test
- **SAFE — Phone:** +351 000 000 000
- **SAFE — Profile:** linkedin.com/in/morgan-example
- **SAFE — Availability:** Available immediately

## 2. Positioning

- **SAFE:** Platform Engineer.
- **SAFE:** Reliable cloud delivery and infrastructure automation.

## 3. Employment chronology

| Period | Company | Safe title |
|---|---|---|
| 2021–Present | Northstar Labs | Platform Engineer |
| 2018–2021 | Cedar Systems | Systems Engineer |

## 4. Northstar Labs — 2021 to Present

- **SAFE:** Operated twelve Kubernetes services on AWS.
- **SAFE:** Managed infrastructure changes with Terraform.
- **SAFE:** Reduced paging incidents by 35% after introducing SLO reviews.
- **SAFE:** Built delivery automation that increased deployments from three to twelve per week.
- **SAFE:** Mentored two engineers through incident-response rotations.
- **QUALIFIED:** Mentoring did not include formal people-management responsibility.

## 5. Cedar Systems — 2018 to 2021

- **SAFE:** Administered Linux infrastructure and monitoring.

## 9. Skill claim matrix

## Strong commercial / production experience

- Kubernetes
- AWS
- Terraform
- Python
- incident response

## Do not claim

- Go production experience

## Application constraints

- **INTERNAL:** Do not disclose compensation expectations in a CV.

## Certificates

- **SAFE:** Certificates not listed.

## Languages

- **SAFE:** Languages not listed.
"""


def part_hashes(path: Path) -> dict[str, str]:
    with zipfile.ZipFile(path) as archive:
        return {
            name: hashlib.sha256(archive.read(name)).hexdigest()
            for name in archive.namelist()
        }


class TargetedCvTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subject = load_subject()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.facts = self.root / "facts.md"
        self.facts.write_text(FACTS.strip() + "\n", encoding="utf-8")
        self.index = self.subject.compile_facts(self.facts)

    def tearDown(self):
        self.temp.cleanup()

    def evidence(self, text: str, section: str | None = None) -> str:
        matches = [
            entry
            for entry in self.index["claims"]
            if text in entry["text"]
            and (section is None or section in entry["section_path"])
        ]
        self.assertEqual(1, len(matches), (text, matches))
        return matches[0]["id"]

    def claim(self, text: str, *evidence_ids: str, **extra):
        return {"text": text, "evidence_ids": list(evidence_ids), **extra}

    def supported_draft(self) -> dict:
        name = self.evidence("Morgan Ibarra")
        base = self.evidence("Lisbon, Portugal")
        email = self.evidence("morgan@example.test")
        phone = self.evidence("+351 000 000 000")
        profile = self.evidence("linkedin.com/in/morgan-example")
        positioning = self.evidence("Platform Engineer.")
        delivery = self.evidence("Reliable cloud delivery")
        chronology = self.evidence("Northstar Labs")
        k8s = self.evidence("Kubernetes services", "4. Northstar Labs — 2021 to Present")
        terraform = self.evidence("Terraform", "4. Northstar Labs — 2021 to Present")
        incidents = self.evidence("35%", "4. Northstar Labs — 2021 to Present")
        deploys = self.evidence("three to twelve", "4. Northstar Labs — 2021 to Present")
        mentoring = self.evidence("Mentored two", "4. Northstar Labs — 2021 to Present")
        python = self.evidence("Python")
        available = self.evidence("Available immediately")
        certificates = self.evidence("Certificates not listed")
        languages = self.evidence("Languages not listed")
        return {
            "schema_version": 1,
            "target": {
                "company": "Acme Orbit",
                "role": "Platform Engineer",
                "job_source": "job-posting.html",
            },
            "identity": {
                "name": self.claim("MORGAN IBARRA", name),
                "tagline": self.claim(
                    "PLATFORM ENGINEER | CLOUD RELIABILITY | INFRASTRUCTURE AUTOMATION",
                    positioning,
                    delivery,
                ),
                "location": self.claim(
                    "Lisbon, Portugal | Available Immediately", base, available
                ),
                "contact": self.claim(
                    "morgan@example.test | +351 000 000 000 | linkedin.com/in/morgan-example",
                    email,
                    phone,
                    profile,
                ),
                "header": self.claim("Morgan Ibarra | Platform Engineer", name, positioning),
            },
            "profile": self.claim(
                "Platform Engineer focused on reliable cloud delivery and infrastructure automation.",
                positioning,
                delivery,
            ),
            "expertise": [
                self.claim("Kubernetes & AWS", k8s, title="Cloud Platforms"),
                self.claim("Terraform infrastructure changes", terraform, title="Infrastructure as Code"),
                self.claim("SLO reviews and incident reduction", incidents, title="Reliability"),
                self.claim("Delivery automation", deploys, title="CI/CD"),
                self.claim("Python", python, title="Automation"),
                self.claim("Incident-response mentoring", mentoring, title="Engineering Influence"),
            ],
            "experience": [
                {
                    "source_section": "4. Northstar Labs — 2021 to Present",
                    "title": "Platform Engineer",
                    "employer": "Northstar Labs",
                    "dates": "2021–Present",
                    "header_evidence_ids": [chronology],
                    "bullets": [
                        self.claim("Operated twelve Kubernetes services on AWS.", k8s),
                        self.claim("Managed infrastructure changes with Terraform.", terraform),
                        self.claim("Reduced paging incidents by 35% after introducing SLO reviews.", incidents),
                        self.claim("Built delivery automation that increased deployments from three to twelve per week.", deploys),
                    ],
                    "environment": self.claim("Kubernetes, AWS, Terraform, Python", k8s, terraform, python),
                }
            ],
            "strengths": [
                self.claim("Reliability: SLO-based incident reduction and actionable operations.", incidents),
                self.claim("Delivery: infrastructure and deployment automation.", terraform, deploys),
            ],
            "skills": [
                self.claim("Kubernetes, AWS, Terraform", k8s, terraform, title="Cloud & Infrastructure"),
                self.claim("Python", python, title="Languages"),
            ],
            "certificates": self.claim("Not listed", certificates),
            "languages": self.claim("Not listed", languages),
            "availability": self.claim("Based in Lisbon; available immediately.", base, available),
        }

    def test_build_preserves_all_noneditable_package_parts(self):
        draft = self.supported_draft()
        output = self.root / "cv.docx"
        ledger = self.root / "ledger.json"

        result = self.subject.build_cv(
            facts_path=self.facts,
            draft=draft,
            template_path=TEMPLATE,
            contract_path=CONTRACT,
            output_path=output,
            ledger_path=ledger,
        )

        self.assertEqual("built", result["status"])
        self.assertTrue(output.is_file())
        self.assertTrue(ledger.is_file())
        before = part_hashes(TEMPLATE)
        after = part_hashes(output)
        self.assertEqual(set(before), set(after))
        editable = {"word/document.xml", "word/footer1.xml"}
        for name in before.keys() - editable:
            self.assertEqual(before[name], after[name], name)
        with zipfile.ZipFile(output) as archive:
            text = archive.read("word/document.xml").decode("utf-8")
            footer = archive.read("word/footer1.xml").decode("utf-8")
        self.assertIn("MORGAN IBARRA", text)
        self.assertIn("Platform Engineer - Northstar Labs", text)
        self.assertIn("Reduced paging incidents by 35%", text)
        self.assertNotIn("<w:tab", text)
        self.assertIn("Morgan Ibarra | Platform Engineer | Page ", footer)
        self.assertIn(" PAGE ", footer)
        self.assertNotIn("{{", text)
        verified = self.subject.verify_output(
            draft=draft,
            output_path=output,
            ledger_path=ledger,
            contract_path=CONTRACT,
        )
        self.assertEqual("verified", verified["status"])

    def test_do_not_claim_evidence_is_rejected(self):
        draft = self.supported_draft()
        forbidden = self.evidence("Go production experience")
        draft["skills"].append(
            self.claim("Go production experience", forbidden, title="Languages")
        )

        with self.assertRaisesRegex(self.subject.ValidationError, "DO_NOT_CLAIM"):
            self.subject.validate_draft(draft, self.index)

    def test_explicit_internal_status_is_rejected_as_evidence(self):
        internal = self.evidence("compensation expectations")
        self.assertEqual(
            "INTERNAL",
            next(entry["status"] for entry in self.index["claims"] if entry["id"] == internal),
        )
        draft = self.supported_draft()
        draft["availability"] = self.claim("Compensation details available.", internal)
        with self.assertRaisesRegex(self.subject.ValidationError, "INTERNAL"):
            self.subject.validate_draft(draft, self.index)

    def test_role_bullet_cannot_borrow_another_employers_evidence(self):
        draft = self.supported_draft()
        cedar = self.evidence("Linux infrastructure", "5. Cedar Systems — 2018 to 2021")
        draft["experience"][0]["bullets"].append(
            self.claim("Administered Linux infrastructure and monitoring.", cedar)
        )

        with self.assertRaisesRegex(self.subject.ValidationError, "source_section"):
            self.subject.validate_draft(draft, self.index)

    def test_template_supplied_labels_are_rejected_from_draft_values(self):
        for field, label in (
            ("certificates", "CERTIFICATES"),
            ("languages", "LANGUAGES"),
            ("availability", "AVAILABILITY"),
        ):
            with self.subTest(field=field):
                draft = self.supported_draft()
                draft[field]["text"] = f"{label} | {draft[field]['text']}"

                with self.assertRaisesRegex(
                    self.subject.ValidationError,
                    rf"{field}\.text must omit the template-supplied label",
                ):
                    self.subject.validate_draft(draft, self.index)

    def test_sigabrt_with_empty_stderr_reports_likely_macos_sandbox_restriction(self):
        failed = subprocess.CompletedProcess([], -6, stdout="", stderr="")
        with (
            mock.patch.object(
                self.subject.shutil,
                "which",
                side_effect=["/fake/soffice", "/fake/pdftoppm"],
            ),
            mock.patch.object(self.subject.subprocess, "run", return_value=failed),
        ):
            with self.assertRaisesRegex(
                self.subject.ValidationError,
                "likely a macOS sandbox restriction.*Retry the same render command outside the sandbox",
            ):
                self.subject.render_docx(self.root / "cv.docx", self.root / "rendered")

    def test_placeholder_template_contains_no_fixture_candidate_data(self):
        with zipfile.ZipFile(TEMPLATE) as archive:
            visible = self.subject.extract_docx_text(TEMPLATE)
            names = set(archive.namelist())
            document = archive.read("word/document.xml").decode("utf-8")
            footer = archive.read("word/footer1.xml").decode("utf-8")
            package_text = "\n".join(
                archive.read(name).decode("utf-8", errors="ignore")
                for name in archive.namelist()
                if name.endswith((".xml", ".rels"))
            )
        allowed_words = {
            "profile", "role", "relevant", "expertise", "professional",
            "experience", "environment", "selected", "engineering",
            "strengths", "technical", "skills", "certificates", "languages",
            "availability", "full", "name", "tagline", "location", "and",
            "contact", "details", "summary", "title", "detail", "employer",
            "dates", "achievement", "strength", "skill", "group", "target",
            "page",
        }
        words = set(re.findall(r"[A-Za-z]+", visible.lower()))
        self.assertLessEqual(words, allowed_words, words - allowed_words)
        self.assertIn("{{FULL_NAME}}", package_text)
        self.assertIn("{{ROLE_ACHIEVEMENT}}", package_text)
        self.assertIn("Targeted CV Skill", package_text)
        self.assertNotIn("Mykola", package_text)
        self.assertNotIn("Riverty", package_text)
        self.assertIn("word/footer1.xml", names)
        self.assertNotIn("word/header1.xml", names)
        self.assertFalse(any(name.startswith("word/fonts/") for name in names))
        self.assertIn('w:ascii="Arial"', document)
        self.assertIn("<w:caps", document)
        self.assertIn('w:fill="F5F6F7"', document)
        self.assertIn("{{FULL_NAME}} | {{TARGET_ROLE}} | Page ", footer)
        self.assertIn(" PAGE ", footer)

    def test_public_cli_build_and_verify_the_same_artifact(self):
        draft_path = self.root / "draft.json"
        output = self.root / "application" / "cv.docx"
        ledger = self.root / "audit" / "claim-ledger.json"
        draft_path.write_text(
            json.dumps(self.supported_draft(), ensure_ascii=False), encoding="utf-8"
        )

        build = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "build",
                "--facts",
                str(self.facts),
                "--draft",
                str(draft_path),
                "--template",
                str(TEMPLATE),
                "--contract",
                str(CONTRACT),
                "--output",
                str(output),
                "--ledger",
                str(ledger),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(0, build.returncode, build.stderr)
        self.assertEqual("built", json.loads(build.stdout)["status"])

        verify = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "verify",
                "--draft",
                str(draft_path),
                "--output",
                str(output),
                "--ledger",
                str(ledger),
                "--contract",
                str(CONTRACT),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(0, verify.returncode, verify.stderr)
        self.assertEqual("verified", json.loads(verify.stdout)["status"])


if __name__ == "__main__":
    unittest.main()
