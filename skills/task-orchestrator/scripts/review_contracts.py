"""Collection, conditional review, finding and acceptance record contracts.

Shape and evidence-reference validation only, using shared record predicates.
Disposition evaluation belongs to acceptance; admission and effects belong to
the application workflows. No manifest, execution or ledger dependency."""

from __future__ import annotations

from typing import Any

from .record_validation import (
    validate_bool,
    validate_exact_object,
    validate_run_relative_reference,
    validate_sha256,
    validate_str,
    validate_str_array,
)


def validate_collection_report(report: dict[str, Any]) -> None:
    """Collection carries evidence, never acceptance or disposition authority."""
    validate_exact_object(report, ('coverage', 'gaps', 'findings', 'rerun_path'), 'collection')
    coverage = report['coverage']
    validate_exact_object(coverage, ('requirements', 'behavior', 'code_quality'), 'collection coverage')
    for category, item in coverage.items():
        validate_exact_object(item, ('status', 'evidence'), category)
        if item['status'] not in {'passed', 'blocked', 'not_run'}:
            raise ValueError('Invalid collection coverage status')
        validate_str(item['evidence'], 'coverage evidence')
    validate_str_array(report['gaps'], 'collection gaps', allow_empty=True)
    if not isinstance(report['findings'], list):
        raise ValueError('collection findings must be an array')
    seen = set()
    for finding in report['findings']:
        validate_exact_object(finding, ('id', 'evidence', 'requirement', 'context', 'exposure'), 'finding')
        for field in ('id', 'requirement', 'context', 'exposure'):
            validate_str(finding[field], 'finding ' + field)
        validate_str_array(finding['evidence'], 'finding evidence')
        if finding['id'] in seen:
            raise ValueError('Duplicate finding identity')
        seen.add(finding['id'])
    if report['rerun_path'] is not None:
        validate_str(report['rerun_path'], 'collection rerun path')


def validate_conditional_review(record):
    validate_exact_object(record, ('stage', 'status', 'candidate_sha256', 'inputs_sha256',
                                  'policy_sha256', 'flow_sha256', 'session_id', 'rationale', 'evidence'), 'conditional review')
    for field in ('stage', 'status', 'session_id', 'rationale'):
        validate_str(record[field], field)
    for field in ('candidate_sha256', 'inputs_sha256', 'policy_sha256', 'flow_sha256'):
        validate_sha256(record[field], field)
    validate_evidence_references(record['evidence'])


def validate_evidence_references(references):
    if not isinstance(references, dict) or not references:
        raise ValueError('Retained evidence references required')
    for path, digest in references.items():
        validate_run_relative_reference(path, 'evidence path')
        validate_sha256(digest, 'evidence digest')


def validate_finding_disposition(item):
    validate_exact_object(item, ('id', 'kind', 'rationale', 'evidence', 'requirement_violation',
                                 'material_risk', 'correction_authorized', 'trigger', 'consequence',
                                 'boundary', 'impact', 'likelihood', 'mitigation', 'compatible_consumers',
                                 'follow_up', 'reassess_when'), 'disposition')
    for field in ('id', 'rationale', 'trigger', 'consequence', 'boundary', 'impact', 'likelihood',
                  'mitigation', 'compatible_consumers', 'follow_up', 'reassess_when'):
        validate_str(item[field], field)
    for field in ('requirement_violation', 'material_risk', 'correction_authorized'):
        validate_bool(item[field], field)
    validate_str_array(item['evidence'], 'disposition evidence')
    if item['kind'] not in {'blocking', 'known_issue', 'observation', 'resolved', 'missing_evidence', 'blocker'}:
        raise ValueError('Invalid finding disposition')


def validate_acceptance_decision(decision):
    validate_exact_object(decision, ('action', 'rationale', 'evidence', 'dispositions', 'unfinished'), 'acceptance decision')
    if decision['action'] not in {'accept', 'correct', 'missing_evidence', 'blocker'}:
        raise ValueError('Invalid acceptance action')
    validate_str(decision['rationale'], 'decision rationale')
    validate_evidence_references(decision['evidence'])
    if not isinstance(decision['dispositions'], list) or not isinstance(decision['unfinished'], list):
        raise ValueError('Disposition and unfinished inventories required')
    seen = set()
    for item in decision['dispositions']:
        validate_finding_disposition(item)
        if item['id'] in seen:
            raise ValueError('Duplicate finding disposition')
        seen.add(item['id'])
    for row in decision['unfinished']:
        validate_exact_object(row, ('owner', 'reason', 'evidence'), 'unfinished evidence row')
        if row['owner'] not in {'verify', 'semantic_review', 'intervene'}:
            raise ValueError('Unknown evidence owner')
        validate_str(row['reason'], 'unfinished reason')
        validate_str_array(row['evidence'], 'unfinished evidence')
