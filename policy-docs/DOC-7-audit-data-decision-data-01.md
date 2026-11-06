---
id: DOC-7
title: Data decision DATA-01 - audit record
version: 1
status: approved
owner: data
---

# DOC-7: DATA-01 audit record

Use synthetic order identifiers and amounts only. Every create and approval attempt records:

- actor
- action
- target
- authorization outcome
- result
- correlation ID
- service version
- timestamp

Do not copy the reason text or any personal data into operational logs.
