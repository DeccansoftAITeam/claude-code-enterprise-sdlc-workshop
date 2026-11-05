# Stage 1 reference specification

## Problem
The baseline approves any positive amount, including $501, without finance review. Support needs a reason, finance approval for high-value refunds, audit and protection against duplicate submission.

## Decisions and acceptance criteria
- A positive USD amount at or below $500.00 follows the standard path; $500.01 or more awaits finance.
- A nonempty reason is required. Only a finance identity can approve or reject a pending high-value refund.
- A replay with the same key and same request returns the existing result without a second effect. Changed request data with the same key conflicts.
- Every create or approval attempt is audited with actor, action, target, authorization outcome, result, correlation ID, version and time. Do not log the reason.
- Demo tokens and fake effects are training fixtures, not production authentication or payment.

## Unresolved
Remaining refundable order balance, real payment provider failure semantics, production identity, protected audit storage and retention require owners' decisions. These are release blockers for a real financial service. DOC-1 is superseded by FIN-01; source code documents behavior, not policy.
