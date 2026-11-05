# Stage 2 Design and implement

## Inputs
The baseline application, `docs/approved-spec.md`, `docs/refund-contract.md`, and the trainer checkpoint. Start the local app and run the baseline test first. The contract is the exercise target; its staging and deployment items are outside today's release-readiness scope.

## Tasks
1. Ask Claude Code for a small implementation plan and identify changes to the UI, API, persistence, authorization and audit. Review before editing.
2. Add tests for $500.00, $500.01, missing reason, authorization and duplicate requests. Run and record the failing results.
3. Implement the specification with Claude Code in small steps. Run tests, inspect the diff and verify changes yourself.
4. Use `/refund-review` or a bounded read-only subagent to review the change. Confirm its findings with code or tests.
5. Record commands, outcomes, known gaps and the next owner's handoff. Compare with `solutions/reference_app.py` and `solutions/reference_tests.py`.

Copyable planning prompt:

```text
Read docs/approved-spec.md and docs/refund-contract.md, then inspect the existing application. Propose a design and small ordered tasks for the refund change, including UI, state, persistence, authorization, idempotency, audit, tests and unresolved risks. Cite file locations. Do not edit files yet. Identify the minimum testable slice and how to verify it.
```

Copyable implementation prompt:

```text
Implement the agreed training specification incrementally. Begin by adding tests that demonstrate the boundary and denial cases; run them and report actual results. Then implement the change, rerun the tests, and summarize the diff, remaining risks and tests not run. Use synthetic data only; never call a real payment provider.
```

Expected output: working local change, meaningful test evidence and an honest handoff. Demo identity and SQLite audit are not production controls.
