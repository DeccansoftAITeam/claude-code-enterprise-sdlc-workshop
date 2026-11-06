---
id: DOC-6
title: Security decision SEC-01 - approval authorization
version: 1
status: approved
owner: security
---

# DOC-6: SEC-01 approval authorization

- Unauthorized approval must fail and the attempt must be audited.
- The classroom uses a fixed local identity mapping for demonstration only. A role value supplied by an arbitrary client is not production authorization.
- Real identity, object-level access and tamper-resistant audit storage need an independent design. They are out of scope for this exercise.
