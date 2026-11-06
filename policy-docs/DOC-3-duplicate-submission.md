---
id: DOC-3
title: Duplicate submission behaviour
version: 1
status: approved
owner: product
---

# DOC-3: Duplicate submission

Customers sometimes double-click the submit button.

- Repeating a request with the same idempotency key and the same request data must not create another refund or repeat a side effect. The original result is returned.
- Reusing an idempotency key with different request data is a conflict and must be refused.
