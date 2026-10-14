# Ollama advisory relocation audit

Active skill/runtime: project-local ollama-delegate, .agents/scripts/ollama_delegate.py;
selected reviewer skill senior-code-review; alias glm-flash (glm-5.3-flash:cloud).

The first broad reference scout ended at max_turns=8 with no final conclusion.
It inspected references but is not a completed review or acceptance evidence.
The narrowed read-only audit completed in 4 turns, 6 repository reads, 9.614 s;
usage: 6031 input tokens and 548 output tokens. No shell or edit tools were exposed.

Result: no material findings for the relocation. Reviewed test constants and
provenance pointer handling in tests/test_review_composition.py:25–70,215–235,
the relocated setup_consumer.py, and the 13-path input-mapping.json.
parents[5] correctly resolves the repository root; paths align with the mapping;
the source route fixture is retained. Source .git is excluded, evaluator answers
are removed before building a separate clean consumer Git baseline. The old
nonexistent-receipt string is an intentional negative control.

This is advisory static evidence, not workflow acceptance or behavioral proof.
The local composition/owner tests supply actual staging and negative controls.
The daemon was reachable only via the approved execution path.
