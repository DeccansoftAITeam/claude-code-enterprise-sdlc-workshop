# Training Contract: Refund-Approval Vertical Slice

**Status**: Proposed for lab implementation; not yet implemented or executed  
**Case**: Fictional Northstar order application  
**Implementation**: Python/FastAPI with pytest and local SQLite training persistence

This contract defines the small end-to-end behavior participants must implement and verify. It is not a production API design or a substitute for the organization's authentication, authorization, compliance and finance controls.

## Business rules

| Rule | Required behavior |
|---|---|
| **R1 — Reason required** | Every new refund request contains a non-empty business reason |
| **R2 — Amount validity** | Refund amount is positive and uses the supported training currency |
| **R3 — Standard refund** | A valid refund of **$500 or less** can proceed through the standard path when the actor is authorized |
| **R4 — High-value refund** | A valid refund **above $500** enters `PENDING_FINANCE_APPROVAL`; it is not completed before an authorized finance approval |
| **R5 — Finance approval** | Only an actor with the finance-approver capability can approve a pending high-value refund |
| **R6 — Idempotency** | Repeating the same request with the same idempotency key returns the original outcome without creating another refund or duplicate side effects |
| **R7 — Idempotency conflict** | Reusing the same key for a materially different request is rejected |
| **R8 — Audit** | Every attempted request and approval decision produces an audit event with actor, action, target, authorization outcome, result, correlation ID, service version and timestamp |
| **R9 — Audit protection** | Training agents and ordinary application roles receive no audit-delete or audit-clear capability |
| **R10 — Traceability** | Implementation, tests and review reference R1–R9 and the approved specification/rule identifiers |

## Resources

### Refund

| Field | Meaning |
|---|---|
| `refund_id` | Unique training identifier |
| `order_id` | Existing fictional order being refunded |
| `amount` | Positive decimal value; floating-point money representation is not permitted |
| `currency` | Supported training currency; use one fixed currency in the simple lab |
| `reason` | Non-empty business reason |
| `status` | `STANDARD_APPROVED`, `PENDING_FINANCE_APPROVAL`, `FINANCE_APPROVED` or `REJECTED` |
| `requested_by` | Actor identity supplied by the training authorization layer, not trusted solely from an unverified request field |
| `approved_by` | Finance actor after approval; null before approval |
| `created_at`, `updated_at` | Recorded timestamps |
| `version` | Record/version value used to support state-transition verification |

### AuditEvent

Append-only training record containing `event_id`, `actor_id`, `action`, `target_type`, `target_id`, `authorization_result`, `business_result`, `correlation_id`, `service_version` and `created_at`. Sensitive reason content and unnecessary personal data are not copied into operational logs.

## Endpoints

### `POST /orders/{order_id}/refunds`

Creates the refund decision/request according to R1–R8.

**Headers**: `Idempotency-Key` and `X-Correlation-ID` (or a generated correlation ID). Authentication is supplied by the prepared training adapter; tests must not treat a caller-supplied role string as production-grade identity.

**Request fields**: `amount`, `currency`, `reason`.

**Expected behavior**:

| Condition | Expected result |
|---|---|
| Valid standard refund | HTTP `201`; refund persisted with `STANDARD_APPROVED`; one audit event |
| Valid amount above $500 | HTTP `202`; refund persisted with `PENDING_FINANCE_APPROVAL`; no completion side effect; one audit event |
| Missing/blank reason or invalid amount/currency | HTTP `422`; no refund business record; validation/audit handling is explicit |
| Unknown order | HTTP `404`; no refund business record |
| Authenticated actor lacks refund-request capability | HTTP `403`; denial audit event |
| Same key and same request repeated | HTTP `200` with original refund representation; no duplicate refund or duplicate business side effect |
| Same key with materially different request | HTTP `409`; conflict audit event |

### `POST /refunds/{refund_id}/approval`

Approves a high-value refund according to R4–R8.

**Request fields**: `decision` (`APPROVE` or `REJECT`) and non-empty `decision_reason`.

**Expected behavior**:

| Condition | Expected result |
|---|---|
| Finance approver approves pending high-value refund | HTTP `200`; state becomes `FINANCE_APPROVED`; `approved_by` and audit recorded |
| Finance approver rejects pending request | HTTP `200`; state becomes `REJECTED`; decision reason and audit recorded |
| Non-finance actor attempts approval | HTTP `403`; state unchanged; denial audit recorded |
| Refund is not pending approval | HTTP `409`; no unauthorized state transition |
| Unknown refund | HTTP `404` |

### `GET /refunds/{refund_id}`

Returns the current refund only to an authorized training role. An actor without access to the order/refund receives `403` or the lab's deliberately documented non-enumerating `404`; the choice must be consistent and tested. Every response includes the current status and correlation ID for support/operations.

## State model

```text
new standard request ────────────────> STANDARD_APPROVED

new high-value request ──────────────> PENDING_FINANCE_APPROVAL
                                             ├── APPROVE ──> FINANCE_APPROVED
                                             └── REJECT ───> REJECTED
```

No direct transition from a new high-value request to `FINANCE_APPROVED` is allowed. Duplicate requests do not replay external or financial side effects. The simple lab need not integrate a real payment provider; a deterministic fake side-effect adapter is used and its call count is tested.

## Minimum executable verification

1. Baseline characterization tests demonstrate the relevant pre-change behavior before implementation.
2. Boundary tests cover exactly `$500` and the smallest representable amount above `$500`.
3. Validation covers blank reason, non-positive amount and unsupported currency.
4. Authorization covers requester, finance approver, non-finance approver and unauthorized object access.
5. State tests prove high-value completion cannot occur before finance approval.
6. Idempotency tests prove same-request replay has no duplicate refund/side effect and conflicting reuse returns `409`.
7. Audit tests prove actor/action/target/result/correlation/version are recorded and no agent/ordinary role can clear audit records.
8. CI runs the complete required test suite and selected static/dependency/security checks; failure, skip or timeout blocks release.
9. Staging smoke tests traverse request → authorization → decision → persistence → audit → response.
10. Rollback restores the previous known-good training version and repeats smoke verification.

## Security and scope boundary

The training adapter makes identities and roles deterministic for exercises. It is explicitly **not** production authentication. A production implementation would require organization-approved identity, short-lived credentials, object-level authorization, secure financial side effects, protected audit storage, retention policy, secrets management and deployment-specific review. No such production approval is claimed by this contract.
