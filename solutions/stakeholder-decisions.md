# Northstar fictional business evidence

Everything in this case is invented for teaching. Do not use real customer information. The baseline code is the repository-root `app.py`; observe it before consulting the reference solution.

## TICKET-101: customer-support request

“Refunds above $500 must be approved by finance. Capture a reason and audit who did what. Customers sometimes double-click the submit button, so prevent duplicate refunds.”

The sponsor wants fewer unauthorized high-value refunds without slowing routine work. No numerical improvement is yet measured. The product owner must define a baseline and agree how to measure it.

## Legacy handbook, version 1 — superseded

“A team lead should review refunds of $500 or more.” This is historical context, not the approved decision for this exercise. It conflicts with the newly approved threshold and role. The handbook is intentionally left in the case so participants must identify the conflict and its version.

## Finance decision record FIN-01 — approved fictional exercise policy

Amounts of $500.00 or less follow the standard path. Amounts strictly above $500.00 require a finance approver. Finance may approve or reject. This decision does not specify an order's remaining refundable balance, payment-provider behavior, exchange rates or real-world compliance requirements; these are open questions, not permission to assume production safety.

## Security decision SEC-01

The classroom uses a fixed local identity mapping for demonstration only. A role value supplied by an arbitrary client is not production authorization. Unauthorized approval must fail and be audited. Real identity, object access and tamper-resistant audit storage require independent design.

## Data decision DATA-01

Use synthetic order identifiers and amounts only. Every creation/approval attempt should record actor, authorization decision, result, target, correlation ID, service version and timestamp. Do not copy reason text or personal data into operational logs.

## Available evidence and missing evidence

The starter's high-value approval behavior can be observed in its characterization test. The reference implementation is a later worked example, not evidence about an existing enterprise system. The starter does not prove how production refunds, providers, databases or staff permissions work. Participants should ask the finance, security and system owners about missing rules before treating the design as production-ready.
