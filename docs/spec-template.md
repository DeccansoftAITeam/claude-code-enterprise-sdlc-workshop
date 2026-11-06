# Spec: [FEATURE NAME]

Status: draft
Risk tier: [1 | 2 | 3]

<!--
  Template from Module 14 (Spec-Driven Development). Six sections, one file. Copy it to docs/spec.md and fill it in.
  Sections 1-4 are written by YOU (the spec owner). Claude may draft sections 5 and 6
  in plan mode; you review them. Only a person changes Status to "approved".
  Nothing is built until Status is "approved".
  Source evidence lives in policy-docs/ and in the GitHub issue that points to it.
  Cite document IDs (DOC-n) and the issue number wherever a rule comes from a source.
-->

## 1. Problem

[What is wrong today, for whom, at what cost? No solution yet. 2 to 4 sentences.]

## 2. User stories

- As a [role], I want [goal], so that [benefit].
- As a [role], I want [goal], so that [benefit].

## 3. Acceptance criteria

<!--
  EARS patterns. SHALL marks a promise, not a wish. One trigger, one response, something you can assert.
  Always true:        The [system] SHALL [response]
  Event:              WHEN [trigger], the [system] SHALL [response]
  State:              WHILE [state], the [system] SHALL [response]
  Optional feature:   WHERE [feature is present], the [system] SHALL [response]
  Unwanted behaviour: IF [condition], THEN the [system] SHALL [response]
  Each boundary is its own row (for example, exactly at the limit and just above it).
  Avoid "fast", "easy", "properly". Status starts as todo.
-->

| ID | Criterion (EARS) | Source | Status |
|---|---|---|---|
| AC-1 | [EARS sentence] | [DOC-n or issue] | todo |
| AC-2 | [EARS sentence] | [DOC-n or issue] | todo |

## 4. Open questions

<!--
  Every question has a specific choice, an owner that is a ROLE (never "the team"),
  and an answer that is a decision in a sentence. "TBD" means the spec is not ready.
  If the owner has not decided, defer it with a reason - that is a decision. Do not invent an answer.
  Answers must come from approved sources in policy-docs/, never from DOC-1 (superseded) or DOC-5 (untrusted).
-->

| ID | Question | Owner | Answer |
|---|---|---|---|
| Q-1 | [Specific question] | [Role] | [Decision, or "Deferred: reason"] |

## 5. Plan

<!-- Draft this in Claude Code plan mode, then review it. Do not write code in this section. -->

Design delta (only the files that change):

- [file]: [what changes]

Contract (exact method signatures, routes, data shapes and the errors they raise):

- [contract line]

Tasks:

| ID | Goal | Criteria | Done when |
|---|---|---|---|
| T1 | [Goal] | AC-1 to AC-n | [its tests pass] |

## 6. Risk and gates

Risk tier [n]: [one-sentence reason: what is the worst thing this change can do?]

| Gate | A person must... | How |
|---|---|---|
| G1 | approve this spec before any test or code is written | You change Status to approved and commit the spec |
| G2 | read the failing tests before the code is written | The build prompt stops after the tests |
| G3 | review the diff before it is committed | `git diff`, then `/code-review`, then commit |
