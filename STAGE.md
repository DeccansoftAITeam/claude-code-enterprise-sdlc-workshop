# Stage 2 Design and implement

## Inputs
The baseline application, `docs/approved-spec.md`, `docs/refund-contract.md`. You work independently; the approved decisions are in `policy-docs/` and the GitHub issue (`gh issue view 1`). Start the local app and run the baseline test first. The contract is the exercise target; its staging and deployment items are outside today's release-readiness scope.

## Tasks
1. In plan mode (`claude --permission-mode plan`), ask Claude Code to draft sections 5 and 6 of the spec (design delta, contract, tasks, risk tier and gates) and identify changes to the UI, API, persistence, authorization and audit. Review before approving. Approve the spec yourself (gate G1) by changing its Status to approved.
2. Add tests for $500.00, $500.01, missing reason, authorization and duplicate requests. Run and record the failing results.
3. Implement the specification with Claude Code in small steps. Run tests, inspect the diff and verify changes yourself.
4. Run the built-in `/code-review` (and `/security-review` for the approval path) on the change. Confirm its findings with code or tests.
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
