#!/usr/bin/env python3
"""Compile CV facts, validate provenance, and build the retained DOCX."""

from __future__ import annotations

import argparse
from copy import deepcopy
from io import BytesIO
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"
XML_NS = "http://www.w3.org/XML/1998/namespace"
W = f"{{{W_NS}}}"
W14 = f"{{{W14_NS}}}"

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_TEMPLATE = SKILL_DIR / "assets" / "targeted-cv-template.docx"
DEFAULT_CONTRACT = SKILL_DIR / "assets" / "template-contract.json"

ALLOWED_STATUSES = {"SAFE", "QUALIFIED", "APPLICATION_SPECIFIC"}
REJECTED_STATUSES = {
    "DO_NOT_CLAIM",
    "NEEDS_CONFIRMATION",
    "INTERNAL",
    "UNCLASSIFIED",
}


class ValidationError(ValueError):
    """The facts, draft, template, or output violates the CV contract."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_digest(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def clean_markdown(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"\[(.*?)\]\([^)]*\)", r"\1", value)
    return re.sub(r"\s+", " ", value).strip()


def explicit_status(value: str) -> str | None:
    upper = value.upper().replace("_", " ")
    if any(
        marker in upper
        for marker in ("DO NOT CLAIM", "DO NOT INVENT", "DO NOT REDUCE THIS TO")
    ):
        return "DO_NOT_CLAIM"
    if "NEEDS CONFIRMATION" in upper:
        return "NEEDS_CONFIRMATION"
    if re.match(
        r"^INTERNAL(?:\s+(?:ONLY|FACT|PREFERENCE|STATUS))?\s*(?:[—:-]|$)",
        clean_markdown(upper),
    ) or any(
        marker in upper
        for marker in (
            "INTERNAL ONLY",
            "INTERNAL FACT",
            "INTERNAL PREFERENCE",
            "INTERNAL STATUS",
        )
    ):
        return "INTERNAL"
    if "APPLICATION-SPECIFIC" in upper:
        return "APPLICATION_SPECIFIC"
    if any(
        marker in upper
        for marker in ("QUALIFIED", "IMPORTANT QUALIFIER", "POC ONLY", "POC:")
    ):
        return "QUALIFIED"
    if "SAFE" in upper:
        return "SAFE"
    return None


def heading_status(headings: list[str]) -> str:
    joined = " / ".join(headings).lower()
    current = headings[-1].lower() if headings else ""
    if any(marker in current for marker in ("do not claim", "avoid")):
        return "DO_NOT_CLAIM"
    if any(
        marker in current
        for marker in (
            "poc / introductory / limited",
            "real but smaller / supporting / historical",
        )
    ):
        return "QUALIFIED"
    if "strong commercial / production" in current:
        return "SAFE"
    if current.startswith("safe ") or current.startswith("safe") or "safe to use" in current:
        return "SAFE"
    if "known unresolved" in current:
        return "NEEDS_CONFIRMATION"
    if "source-history" in current:
        return "INTERNAL"
    if "important exclusions" in joined:
        return "DO_NOT_CLAIM"
    return "UNCLASSIFIED"


def claim_id(status: str, section_path: list[str], text: str, occurrence: int) -> str:
    seed = "\n".join([status, *section_path, text, str(occurrence)])
    return "FC-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]


def compile_facts(path: Path) -> dict:
    path = Path(path).resolve()
    lines = path.read_text(encoding="utf-8").splitlines()
    headings: list[str] = []
    inherited_by_indent: dict[int, str] = {}
    seen: dict[tuple[str, tuple[str, ...], str], int] = {}
    claims: list[dict] = []

    def add_claim(raw: str, status: str, line_number: int) -> None:
        text = clean_markdown(raw)
        if not text:
            return
        key = (status, tuple(headings), text)
        occurrence = seen.get(key, 0) + 1
        seen[key] = occurrence
        claims.append(
            {
                "id": claim_id(status, headings, text, occurrence),
                "status": status,
                "text": text,
                "source_text": raw.strip(),
                "section_path": list(headings),
                "line": line_number,
            }
        )

    for line_number, line in enumerate(lines, start=1):
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            headings = headings[: level - 1]
            headings.append(clean_markdown(heading.group(2)))
            inherited_by_indent.clear()
            continue

        bullet = re.match(r"^(\s*)[-*]\s+(.+?)\s*$", line)
        if bullet:
            indent = len(bullet.group(1).expandtabs(2))
            raw = bullet.group(2)
            status = explicit_status(raw)
            if status is None:
                parents = [key for key in inherited_by_indent if key < indent]
                status = (
                    inherited_by_indent[max(parents)]
                    if parents
                    else heading_status(headings)
                )
            inherited_by_indent = {
                key: value for key, value in inherited_by_indent.items() if key < indent
            }
            inherited_by_indent[indent] = status
            add_claim(raw, status, line_number)
            continue

        if line.startswith("|") and line.endswith("|"):
            cells = [clean_markdown(cell) for cell in line.strip("|").split("|")]
            if not cells or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            if all(cell.lower() in {"period", "company / activity", "company", "safe title"} for cell in cells):
                continue
            status = "SAFE" if any("employment chronology" in h.lower() for h in headings) else heading_status(headings)
            add_claim(" | ".join(cells), status, line_number)
            continue

        stripped = line.strip()
        if stripped and (explicit_status(stripped) is not None):
            add_claim(stripped, explicit_status(stripped) or "UNCLASSIFIED", line_number)

    ids = [entry["id"] for entry in claims]
    if len(ids) != len(set(ids)):
        raise ValidationError("compiled fact IDs are not unique")
    return {
        "schema_version": 1,
        "source": str(path),
        "source_sha256": sha256_file(path),
        "claims": claims,
    }


def require_mapping(value: object, path: str) -> dict:
    if not isinstance(value, dict):
        raise ValidationError(f"{path} must be an object")
    return value


def require_list(value: object, path: str, *, nonempty: bool = True) -> list:
    if not isinstance(value, list) or (nonempty and not value):
        suffix = " a non-empty array" if nonempty else " an array"
        raise ValidationError(f"{path} must be{suffix}")
    return value


def require_text(value: object, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{path} must be a non-empty string")
    if re.search(r"\{\{|\}\}|\[(?:REQUIRED|OPTIONAL)\]|\b(?:TBD|TODO)\b", value, re.I):
        raise ValidationError(f"{path} contains an unresolved placeholder")
    return value.strip()


def validate_evidence(
    item: dict,
    path: str,
    facts_by_id: dict[str, dict],
    *,
    required_section: str | None = None,
) -> tuple[list[dict], list[str]]:
    evidence_ids = require_list(item.get("evidence_ids"), f"{path}.evidence_ids")
    if any(not isinstance(item_id, str) or not item_id for item_id in evidence_ids):
        raise ValidationError(f"{path}.evidence_ids must contain strings")
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValidationError(f"{path}.evidence_ids contains duplicates")

    evidence: list[dict] = []
    for evidence_id in evidence_ids:
        if evidence_id not in facts_by_id:
            raise ValidationError(f"{path} cites unknown evidence {evidence_id}")
        entry = facts_by_id[evidence_id]
        status = entry["status"]
        if status not in ALLOWED_STATUSES:
            raise ValidationError(
                f"{path} cites {status} evidence {evidence_id}: {entry['text']}"
            )
        text_for_qualification = " ".join(
            str(item.get(key, "")) for key in ("title", "text")
        ).lower()
        if status == "QUALIFIED":
            qualification = require_text(item.get("qualification"), f"{path}.qualification")
            if qualification.lower() not in text_for_qualification:
                raise ValidationError(
                    f"{path}.qualification must be visible in the rendered claim"
                )
        if status == "APPLICATION_SPECIFIC" and item.get("application_specific") is not True:
            raise ValidationError(
                f"{path} must explicitly allow APPLICATION_SPECIFIC evidence"
            )
        evidence.append(entry)

    if required_section and not any(
        required_section in entry["section_path"] for entry in evidence
    ):
        raise ValidationError(
            f"{path} must cite evidence from source_section {required_section!r}"
        )
    return evidence, list(evidence_ids)


def validate_claim(
    value: object,
    path: str,
    facts_by_id: dict[str, dict],
    *,
    required_section: str | None = None,
    title_key: str | None = None,
) -> dict:
    item = require_mapping(value, path)
    text = require_text(item.get("text"), f"{path}.text")
    fragments = [text]
    rendered = text
    if title_key:
        title = require_text(item.get(title_key), f"{path}.{title_key}")
        fragments = [title, text]
        rendered = f"{title}: {text}"
    evidence, evidence_ids = validate_evidence(
        item, path, facts_by_id, required_section=required_section
    )
    return {
        "path": path,
        "rendered_text": rendered,
        "output_fragments": fragments,
        "evidence_ids": evidence_ids,
        "evidence": evidence,
    }


def validate_draft(draft: dict, facts_index: dict) -> list[dict]:
    draft = require_mapping(draft, "draft")
    if draft.get("schema_version") != 1:
        raise ValidationError("draft.schema_version must equal 1")
    target = require_mapping(draft.get("target"), "target")
    for key in ("company", "role", "job_source"):
        require_text(target.get(key), f"target.{key}")

    facts_by_id = {entry["id"]: entry for entry in facts_index.get("claims", [])}
    if not facts_by_id:
        raise ValidationError("facts index contains no claims")
    ledger: list[dict] = []

    identity = require_mapping(draft.get("identity"), "identity")
    for key in ("name", "tagline", "location", "contact", "header"):
        ledger.append(validate_claim(identity.get(key), f"identity.{key}", facts_by_id))
    ledger.append(validate_claim(draft.get("profile"), "profile", facts_by_id))

    expertise = require_list(draft.get("expertise"), "expertise")
    if len(expertise) != 6:
        raise ValidationError("expertise must contain exactly six entries for the template")
    for index, item in enumerate(expertise):
        ledger.append(
            validate_claim(
                item, f"expertise[{index}]", facts_by_id, title_key="title"
            )
        )

    experience = require_list(draft.get("experience"), "experience")
    for role_index, role_value in enumerate(experience):
        role_path = f"experience[{role_index}]"
        role = require_mapping(role_value, role_path)
        source_section = require_text(
            role.get("source_section"), f"{role_path}.source_section"
        )
        known_sections = {
            heading
            for entry in facts_by_id.values()
            for heading in entry["section_path"]
        }
        if source_section not in known_sections:
            raise ValidationError(f"{role_path}.source_section is not in the facts source")
        title = require_text(role.get("title"), f"{role_path}.title")
        employer = require_text(role.get("employer"), f"{role_path}.employer")
        dates = require_text(role.get("dates"), f"{role_path}.dates")
        header_item = {
            "text": f"{title} — {employer} {dates}",
            "evidence_ids": role.get("header_evidence_ids"),
        }
        header_evidence, header_ids = validate_evidence(
            header_item, f"{role_path}.header", facts_by_id
        )
        ledger.append(
            {
                "path": f"{role_path}.header",
                "rendered_text": header_item["text"],
                "output_fragments": [f"{title} — {employer}", dates],
                "evidence_ids": header_ids,
                "evidence": header_evidence,
            }
        )
        bullets = require_list(role.get("bullets"), f"{role_path}.bullets")
        for bullet_index, bullet in enumerate(bullets):
            ledger.append(
                validate_claim(
                    bullet,
                    f"{role_path}.bullets[{bullet_index}]",
                    facts_by_id,
                    required_section=source_section,
                )
            )
        if role.get("environment") is not None:
            ledger.append(
                validate_claim(
                    role["environment"],
                    f"{role_path}.environment",
                    facts_by_id,
                    required_section=source_section,
                )
            )

    for collection, title_key in (("strengths", None), ("skills", "title")):
        values = require_list(draft.get(collection), collection)
        for index, item in enumerate(values):
            ledger.append(
                validate_claim(
                    item,
                    f"{collection}[{index}]",
                    facts_by_id,
                    title_key=title_key,
                )
            )

    for key, label in (
        ("certificates", "Certificates"),
        ("languages", "Languages"),
        ("availability", "Availability"),
    ):
        item = require_mapping(draft.get(key), key)
        text = require_text(item.get("text"), f"{key}.text")
        if re.match(rf"^{re.escape(label)}\b", text, re.I):
            raise ValidationError(
                f"{key}.text must omit the template-supplied label {label!r}"
            )
        ledger.append(validate_claim(item, key, facts_by_id))
    return ledger


def register_namespaces(xml_bytes: bytes) -> None:
    for _, (prefix, uri) in ET.iterparse(BytesIO(xml_bytes), events=("start-ns",)):
        if prefix == "xml":
            continue
        try:
            ET.register_namespace(prefix, uri)
        except ValueError:
            pass


def paragraph_id(paragraph: ET.Element) -> str | None:
    return paragraph.get(W14 + "paraId")


def paragraph_by_id(root: ET.Element, para_id: str) -> ET.Element:
    matches = [p for p in root.iter(W + "p") if paragraph_id(p) == para_id]
    if len(matches) != 1:
        raise ValidationError(
            f"template expected one paragraph {para_id}, found {len(matches)}"
        )
    return matches[0]


def clear_run_content(run: ET.Element) -> None:
    for child in list(run):
        if child.tag != W + "rPr":
            run.remove(child)


def append_text(run: ET.Element, text: str) -> None:
    node = ET.SubElement(run, W + "t")
    if text[:1].isspace() or text[-1:].isspace():
        node.set(f"{{{XML_NS}}}space", "preserve")
    node.text = text


def runs(paragraph: ET.Element) -> list[ET.Element]:
    found = list(paragraph.findall("./" + W + "r"))
    if not found:
        found = [ET.SubElement(paragraph, W + "r")]
    return found


def set_plain_text(paragraph: ET.Element, text: str) -> None:
    found = runs(paragraph)
    for run in found:
        clear_run_content(run)
    append_text(found[0], text)


def set_role_header(paragraph: ET.Element, role: str, dates: str) -> None:
    found = runs(paragraph)
    while len(found) < 2:
        found.append(ET.SubElement(paragraph, W + "r"))
    for run in found:
        clear_run_content(run)
    append_text(found[0], role)
    ET.SubElement(found[1], W + "tab")
    append_text(found[1], dates)


def set_labeled_text(paragraph: ET.Element, label: str, text: str) -> None:
    found = runs(paragraph)
    while len(found) < 2:
        found.append(ET.SubElement(paragraph, W + "r"))
    for run in found:
        clear_run_content(run)
    append_text(found[0], label + ": ")
    append_text(found[1], text)


def set_bullet_text(paragraph: ET.Element, text: str) -> None:
    set_plain_text(paragraph, "• " + text)


def find_expertise_table(root: ET.Element, title_para_id: str) -> ET.Element:
    for table in root.iter(W + "tbl"):
        if any(paragraph_id(p) == title_para_id for p in table.iter(W + "p")):
            return table
    raise ValidationError("template expertise table was not found")


def assign_unique_paragraph_ids(root: ET.Element, *, start: int = 1) -> None:
    value = start
    for paragraph in root.iter(W + "p"):
        paragraph.set(W14 + "paraId", f"{value:08X}")
        value += 1


def xml_bytes(root: ET.Element) -> bytes:
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def load_contract(contract_path: Path, template_path: Path) -> dict:
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    if contract.get("schema_version") != 1:
        raise ValidationError("template contract schema_version must equal 1")
    expected = contract.get("sha256")
    actual = sha256_file(Path(template_path))
    if expected != actual:
        raise ValidationError(
            f"template SHA-256 mismatch: expected {expected}, found {actual}"
        )
    return contract


def build_document_xml(source: bytes, draft: dict, contract: dict) -> bytes:
    register_namespaces(source)
    root = ET.fromstring(source)
    body = root.find(".//" + W + "body")
    if body is None:
        raise ValidationError("template document has no body")
    slots = contract["body"]
    archetypes = {
        key: deepcopy(paragraph_by_id(root, para_id))
        for key, para_id in slots.items()
        if isinstance(para_id, str)
    }
    expertise_table = deepcopy(
        find_expertise_table(root, slots["expertise_table"]["titles"][0])
    )
    section = next((deepcopy(child) for child in body if child.tag == W + "sectPr"), None)
    if section is None:
        raise ValidationError("template document has no section properties")

    for child in list(body):
        body.remove(child)

    simple_values = (
        ("name", draft["identity"]["name"]["text"]),
        ("tagline", draft["identity"]["tagline"]["text"]),
        ("location", draft["identity"]["location"]["text"]),
        ("contact", draft["identity"]["contact"]["text"]),
    )
    for key, value in simple_values:
        paragraph = deepcopy(archetypes[key])
        set_plain_text(paragraph, value)
        body.append(paragraph)

    body.append(deepcopy(archetypes["profile_heading"]))
    profile = deepcopy(archetypes["profile"])
    set_plain_text(profile, draft["profile"]["text"])
    body.append(profile)
    body.append(deepcopy(archetypes["expertise_heading"]))

    for entry, title_id, description_id in zip(
        draft["expertise"],
        slots["expertise_table"]["titles"],
        slots["expertise_table"]["descriptions"],
    ):
        set_plain_text(paragraph_by_id(expertise_table, title_id), entry["title"])
        set_plain_text(paragraph_by_id(expertise_table, description_id), entry["text"])
    body.append(expertise_table)
    body.append(deepcopy(archetypes["experience_heading"]))

    for role in draft["experience"]:
        header = deepcopy(archetypes["role_header"])
        set_role_header(header, f"{role['title']} — {role['employer']}", role["dates"])
        body.append(header)
        for bullet in role["bullets"]:
            paragraph = deepcopy(archetypes["role_bullet"])
            set_bullet_text(paragraph, bullet["text"])
            body.append(paragraph)
        if role.get("environment") is not None:
            paragraph = deepcopy(archetypes["environment"])
            set_labeled_text(paragraph, "Environment", role["environment"]["text"])
            body.append(paragraph)

    body.append(deepcopy(archetypes["strengths_heading"]))
    for strength in draft["strengths"]:
        paragraph = deepcopy(archetypes["strength_bullet"])
        set_bullet_text(paragraph, strength["text"])
        body.append(paragraph)

    body.append(deepcopy(archetypes["skills_heading"]))
    for skill in draft["skills"]:
        paragraph = deepcopy(archetypes["skill_line"])
        set_labeled_text(paragraph, skill["title"], skill["text"])
        body.append(paragraph)

    body.append(deepcopy(archetypes["spacer"]))
    for key, label in (
        ("certificates", "Certificates"),
        ("languages", "Languages"),
        ("availability", "Availability"),
    ):
        paragraph = deepcopy(archetypes[key])
        set_labeled_text(paragraph, label, draft[key]["text"])
        body.append(paragraph)
    body.append(section)
    assign_unique_paragraph_ids(body)
    return xml_bytes(root)


def build_header_xml(source: bytes, draft: dict) -> bytes:
    register_namespaces(source)
    root = ET.fromstring(source)
    paragraphs = list(root.iter(W + "p"))
    if len(paragraphs) != 1:
        raise ValidationError("template header must contain exactly one paragraph")
    set_plain_text(paragraphs[0], draft["identity"]["header"]["text"])
    assign_unique_paragraph_ids(root, start=0x7FFF0000)
    return xml_bytes(root)


def zip_part_hashes(path: Path) -> dict[str, str]:
    with zipfile.ZipFile(path) as archive:
        return {name: sha256_bytes(archive.read(name)) for name in archive.namelist()}


def write_modified_docx(
    template_path: Path,
    output_path: Path,
    replacements: dict[str, bytes],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.resolve() == template_path.resolve():
        raise ValidationError("output path must differ from the retained template")
    temp_path = output_path.with_name(output_path.name + ".tmp")
    try:
        with zipfile.ZipFile(template_path) as source, zipfile.ZipFile(temp_path, "w") as target:
            for info in source.infolist():
                data = replacements.get(info.filename, source.read(info.filename))
                target.writestr(info, data)
        with zipfile.ZipFile(temp_path) as check:
            bad = check.testzip()
            if bad:
                raise ValidationError(f"generated DOCX has a corrupt part: {bad}")
        os.replace(temp_path, output_path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def build_cv(
    *,
    facts_path: Path,
    draft: dict,
    template_path: Path,
    contract_path: Path,
    output_path: Path,
    ledger_path: Path,
) -> dict:
    facts_path = Path(facts_path).resolve()
    template_path = Path(template_path).resolve()
    contract_path = Path(contract_path).resolve()
    output_path = Path(output_path).resolve()
    ledger_path = Path(ledger_path).resolve()
    contract = load_contract(contract_path, template_path)
    facts_index = compile_facts(facts_path)
    claim_ledger = validate_draft(draft, facts_index)

    with zipfile.ZipFile(template_path) as archive:
        source_document = archive.read("word/document.xml")
        source_header = archive.read("word/header1.xml")
    document = build_document_xml(source_document, draft, contract)
    header = build_header_xml(source_header, draft)
    write_modified_docx(
        template_path,
        output_path,
        {"word/document.xml": document, "word/header1.xml": header},
    )

    template_parts = zip_part_hashes(template_path)
    output_parts = zip_part_hashes(output_path)
    changed_parts = sorted(
        name for name in template_parts if template_parts[name] != output_parts.get(name)
    )
    allowed = sorted(contract["editable_parts"])
    if changed_parts != allowed:
        raise ValidationError(
            f"generated package changed {changed_parts}; expected exactly {allowed}"
        )

    ledger = {
        "schema_version": 1,
        "facts_source": str(facts_path),
        "facts_sha256": facts_index["source_sha256"],
        "draft_sha256": canonical_digest(draft),
        "template": str(template_path),
        "template_sha256": sha256_file(template_path),
        "template_part_sha256": template_parts,
        "editable_parts": allowed,
        "output": str(output_path),
        "output_sha256": sha256_file(output_path),
        "claims": claim_ledger,
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return {
        "status": "built",
        "output": str(output_path),
        "ledger": str(ledger_path),
        "claims": len(claim_ledger),
        "changed_parts": changed_parts,
    }


def extract_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        parts = [archive.read("word/document.xml"), archive.read("word/header1.xml")]
    text: list[str] = []
    for part in parts:
        root = ET.fromstring(part)
        text.extend(node.text or "" for node in root.iter(W + "t"))
    return re.sub(r"\s+", " ", " ".join(text)).strip()


def verify_output(
    *,
    draft: dict,
    output_path: Path,
    ledger_path: Path,
    contract_path: Path,
) -> dict:
    output_path = Path(output_path).resolve()
    ledger = json.loads(Path(ledger_path).read_text(encoding="utf-8"))
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    if ledger.get("draft_sha256") != canonical_digest(draft):
        raise ValidationError("draft does not match the claim ledger")
    if ledger.get("output_sha256") != sha256_file(output_path):
        raise ValidationError("output does not match the claim ledger")
    if sorted(ledger.get("editable_parts", [])) != sorted(contract["editable_parts"]):
        raise ValidationError("ledger editable parts do not match the template contract")

    with zipfile.ZipFile(output_path) as archive:
        if archive.testzip() is not None:
            raise ValidationError("output DOCX is corrupt")
        output_parts = {
            name: sha256_bytes(archive.read(name)) for name in archive.namelist()
        }
    template_parts = ledger.get("template_part_sha256", {})
    if set(output_parts) != set(template_parts):
        raise ValidationError("output package parts differ from the retained template")
    editable = set(contract["editable_parts"])
    changed = sorted(
        name for name in output_parts if output_parts[name] != template_parts[name]
    )
    if changed != sorted(editable):
        raise ValidationError(f"unexpected changed package parts: {changed}")
    for name in output_parts.keys() - editable:
        if output_parts[name] != template_parts[name]:
            raise ValidationError(f"preserve-only package part changed: {name}")

    text = extract_docx_text(output_path)
    if re.search(r"\{\{|\}\}|\[(?:REQUIRED|OPTIONAL)\]|\b(?:TBD|TODO)\b", text, re.I):
        raise ValidationError("output contains unresolved placeholders")
    missing: list[str] = []
    for claim in ledger.get("claims", []):
        for fragment in claim.get("output_fragments", []):
            normalized = re.sub(r"\s+", " ", fragment).strip()
            if normalized not in text:
                missing.append(f"{claim.get('path')}: {normalized}")
    if missing:
        raise ValidationError("output is missing drafted content: " + "; ".join(missing))
    return {
        "status": "verified",
        "output": str(output_path),
        "claims": len(ledger.get("claims", [])),
        "changed_parts": changed,
    }


def render_docx(input_path: Path, output_dir: Path) -> dict:
    input_path = Path(input_path).resolve()
    output_dir = Path(output_dir).resolve()
    office = shutil.which("soffice") or shutil.which("libreoffice")
    rasterizer = shutil.which("pdftoppm")
    missing = [name for name, value in (("LibreOffice/soffice", office), ("pdftoppm", rasterizer)) if value is None]
    if missing:
        raise ValidationError(
            "rendering dependency unavailable: " + ", ".join(missing)
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="targeted-cv-render-") as temp_name:
        temp = Path(temp_name)
        profile = temp / "libreoffice-profile"
        home = temp / "home"
        converted = temp / "converted"
        profile.mkdir()
        home.mkdir()
        converted.mkdir()
        command = [
            str(office),
            "--headless",
            f"-env:UserInstallation={profile.as_uri()}",
            "--convert-to",
            "pdf",
            "--outdir",
            str(converted),
            str(input_path),
        ]
        completed = subprocess.run(
            command,
            env={**os.environ, "HOME": str(home)},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            if completed.returncode == -6 and not completed.stderr.strip():
                raise ValidationError(
                    "LibreOffice conversion failed (-6/SIGABRT) with empty stderr; "
                    "this is likely a macOS sandbox restriction because LibreOffice "
                    "initializes AppKit even in headless mode. Retry the same render "
                    "command outside the sandbox with escalation"
                )
            raise ValidationError(
                f"LibreOffice conversion failed ({completed.returncode}): {completed.stderr.strip()}"
            )
        pdf = converted / (input_path.stem + ".pdf")
        if not pdf.is_file():
            raise ValidationError("LibreOffice did not create the expected PDF")
        raster = subprocess.run(
            [str(rasterizer), "-png", "-r", "144", str(pdf), str(output_dir / "page")],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if raster.returncode != 0:
            raise ValidationError(
                f"pdftoppm failed ({raster.returncode}): {raster.stderr.strip()}"
            )
        shutil.copy2(pdf, output_dir / (input_path.stem + ".pdf"))
    pages = sorted(output_dir.glob("page-*.png"))
    if not pages:
        raise ValidationError("rendering produced no page images")
    return {
        "status": "rendered",
        "input": str(input_path),
        "output_dir": str(output_dir),
        "pages": [str(page) for page in pages],
    }


def read_json(path: Path) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    return require_mapping(value, str(path))


def write_json(path: Path, value: object) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)

    index = subparsers.add_parser("index", help="compile Markdown facts into evidence IDs")
    index.add_argument("--facts", type=Path, required=True)
    index.add_argument("--output", type=Path, required=True)

    validate = subparsers.add_parser("validate", help="validate draft evidence provenance")
    validate.add_argument("--facts", type=Path, required=True)
    validate.add_argument("--draft", type=Path, required=True)

    build = subparsers.add_parser("build", help="build a targeted DOCX")
    build.add_argument("--facts", type=Path, required=True)
    build.add_argument("--draft", type=Path, required=True)
    build.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    build.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--ledger", type=Path, required=True)

    verify = subparsers.add_parser("verify", help="verify output structure and claim ledger")
    verify.add_argument("--draft", type=Path, required=True)
    verify.add_argument("--output", type=Path, required=True)
    verify.add_argument("--ledger", type=Path, required=True)
    verify.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)

    render = subparsers.add_parser("render", help="render DOCX to PDF and PNG pages")
    render.add_argument("--input", type=Path, required=True)
    render.add_argument("--output-dir", type=Path, required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "index":
            result = compile_facts(args.facts)
            write_json(args.output, result)
            summary = {
                "status": "indexed",
                "output": str(args.output.resolve()),
                "claims": len(result["claims"]),
            }
        elif args.command == "validate":
            facts = compile_facts(args.facts)
            ledger = validate_draft(read_json(args.draft), facts)
            summary = {"status": "valid", "claims": len(ledger)}
        elif args.command == "build":
            summary = build_cv(
                facts_path=args.facts,
                draft=read_json(args.draft),
                template_path=args.template,
                contract_path=args.contract,
                output_path=args.output,
                ledger_path=args.ledger,
            )
        elif args.command == "verify":
            summary = verify_output(
                draft=read_json(args.draft),
                output_path=args.output,
                ledger_path=args.ledger,
                contract_path=args.contract,
            )
        else:
            summary = render_docx(args.input, args.output_dir)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
