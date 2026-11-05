# Stage 3 Review and release readiness

## Inputs
This branch contains a completed-looking training implementation with deliberate defects. Read `docs/approved-spec.md`, inspect the implementation and run the tests. It is intentionally unsafe and must not be deployed.

## Tasks
1. Derive independent checks for boundary, authorization, idempotency and audit from the specification.
2. Ask Claude Code to use a bounded read-only subagent to inspect the implementation. Verify claims by reading the cited code and running focused tests.
3. Write findings with the requirement, evidence, impact and release disposition. Record what you did not test.
4. Decide whether the implementation is release-ready. Compare with `solutions/stage3-review.md` at the end.

Copyable prompt:

```text
Review this branch against docs/approved-spec.md without modifying files. Use a read-only subagent to examine authorization and state transitions while you examine boundaries, retries and audit. Report concrete findings with file locations, impact and a way to reproduce each. Distinguish verified findings from hypotheses and state what was not tested. Do not treat a passing test suite as proof of production readiness.
```

Expected output: evidence-based findings and release recommendation. No deployment is required.
