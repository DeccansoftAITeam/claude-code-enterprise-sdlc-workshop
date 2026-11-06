# Spec: Refund approval for high-value refunds (approved baseline)

Status: approved
Risk tier: 3

## 1. Problem

The baseline approves any positive amount, including $501.00, without finance review. Support has no reason field, nothing records who did what, and a double-clicked submit can create a second refund. Unreviewed high-value refunds cost money and cannot be explained afterwards.

## 2. User stories

- As a support agent, I want to submit a refund with a reason, so that the request is understood.
- As a finance approver, I want to approve or reject refunds above $500.00, so that high-value refunds are reviewed.
- As a support agent, I want a repeated submission to be recognised, so that the customer is not refunded twice.
- As a security reviewer, I want every create and approval attempt audited, so that we can see who did what.

## 3. Acceptance criteria

| ID | Criterion (EARS) | Source | Status |
|---|---|---|---|
| AC-1 | WHEN a refund of $500.00 or less is submitted with a reason, the service SHALL follow the standard path | DOC-2 | todo |
| AC-2 | WHEN a refund above $500.00 (for example $500.01) is submitted, the service SHALL hold it as pending for finance | DOC-2 | todo |
| AC-3 | IF the reason is empty, THEN the service SHALL refuse the request with an error and store nothing | issue | todo |
| AC-4 | WHEN a finance approver approves or rejects a pending refund, the service SHALL record that decision | DOC-2 | todo |
| AC-5 | IF a non-finance identity tries to approve a pending refund, THEN the service SHALL refuse it and audit the attempt | DOC-6 | todo |
| AC-6 | WHEN a request is repeated with the same idempotency key and the same data, the service SHALL return the original result without a second effect | DOC-3 | todo |
| AC-7 | IF a request reuses an idempotency key with different data, THEN the service SHALL refuse it as a conflict | DOC-3 | todo |
| AC-8 | WHEN a create or approval attempt occurs, the service SHALL audit actor, action, target, authorization outcome, result, correlation ID, service version and time, and SHALL NOT log the reason | DOC-7 | todo |

## 4. Open questions

| ID | Question | Owner | Answer |
|---|---|---|---|
| Q-1 | Is exactly $500.00 on the standard path? | Finance | Yes. Only amounts strictly above $500.00 need finance (DOC-2, AC-1, AC-2) |
| Q-2 | Which policy applies, DOC-1 or DOC-2? | Finance | DOC-2. DOC-1 is superseded |
| Q-3 | What is the remaining refundable balance rule? | Finance | Deferred: DOC-8 lists it as open; a release blocker for a real service |
| Q-4 | How is production identity handled? | Security | Deferred: demo identities only (DOC-6); production identity needs its own design |
| Q-5 | How is real provider failure handled? | Platform | Deferred: no provider exists in this exercise (DOC-8) |

## 5. Plan

See `docs/refund-contract.md` for the contract. Design delta: `app.py` (create and approve endpoints, idempotency, audit), `index.html` (reason field), `tests/` (one test per criterion, named `test_ac<n>_...`).

## 6. Risk and gates

Risk tier 3: refunds involve money and authorization, even though the effect here is fake.

| Gate | A person must... | How |
|---|---|---|
| G1 | approve this spec before any test or code is written | You change Status to approved and commit |
| G2 | read the failing tests before the code is written | The build prompt stops after the tests |
| G3 | review the diff before it is committed | `git diff`, `/code-review`, then commit |
| G4 | sign off the release | Recorded in your go/no-go recommendation |
