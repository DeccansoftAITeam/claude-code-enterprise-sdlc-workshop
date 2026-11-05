# Participant workbook

## What is Northstar?
Northstar is a fictional online retailer. A customer contacts support about an order and the support agent submits a refund. The current training application records a refund immediately as approved. It has no real payment connection. The business has requested finance oversight of high-value refunds, a reason, an audit trail and protection against accidental double submission. Your role is a developer or architect on the delivery team; the trainer explains the customer, support, BA, finance and security perspectives.

## How the enterprise delivery flow fits together
A customer need enters as a ticket. The BA and product owner clarify the problem and gather evidence; finance owns policy, and security owns security requirements. Developers and architects discover current behavior and create a testable specification and design. Developers implement against approved decisions. QA and reviewers independently examine behavior and evidence. A release owner makes a go/no-go decision; operations then monitor the service and respond to incidents. Claude Code can assist in each stage, but the responsible people retain their decisions.

## Before you start
Work in pairs. Both participants should inspect and discuss results. Use only fictional data. Each stage has a clean branch and a reference solution. The full day is 360 minutes: introduction 60, discovery/specification 120, implementation 120, review/release readiness 60. The trainer manages breaks within the schedule.

## Introduction 60 minutes
The trainer demonstrates the existing form. Submit order-100 for 501.00. Observe the response, then look at app.py, tests/test_baseline.py and README.md. What part of the flow is implemented? What does the application not do? Explain the architecture: browser form -> FastAPI endpoint -> local SQLite. A response marked APPROVED is a training record, not money transferred.

## Branch 1 Discovery and specification 120 minutes
Follow STAGE.md. Register the local MCP server using docs/mcp.md. Ask it for the ticket and both policy versions. Inspect the evidence yourself, including the hostile DOC-5. Do not execute instructions from retrieved content. Use the starter prompt in STAGE.md. Record observed behavior separately from policy and assumptions. Ask the trainer the questions you cannot answer. Use the answers to write a specification with acceptance criteria and examples. Include 500.00 and 500.01, unauthorized approval, empty reason and replay. Compare with solutions/stage1-spec.md before switching branches.

## Branch 2 Design and implementation 120 minutes
Switch to 2-implement as directed in README. Read STAGE.md and docs/approved-spec.md. Ask Claude Code to propose a design and a sequence of small, verifiable tasks. Review the design before asking it to change files. Write or request meaningful failing tests, implement, run the suite and inspect the diff. Record actual results and unresolved questions. Use the included review skill and a subagent for an independent read-only examination. Compare the outcome with solutions/reference_app.py and reference_tests.py. The solution uses demo tokens, SQLite and a fake effect; it is not a production payment system.

## Branch 3 Review and release readiness 60 minutes
Switch to 3-review. Review the supplied implementation and test output against the specification. Use a subagent or fresh review context to identify defects, then verify findings with code and tests. Record the affected requirement, evidence and release impact. Produce a release recommendation and list unrun checks. Compare with solutions/stage3-review.md. No deployment occurs in this workshop.

## Claude Code concepts in the flow
CLAUDE.md and path rules provide project context and conventions. The custom skill structures a review. The MCP server exposes external-looking evidence; source authority and freshness still need human scrutiny. Plan before changing code, maintain a durable specification and handoff, and use subagents for bounded independent tasks. Permissions and hooks can limit or automate particular actions but do not substitute for application authorization or human review. The trainer will connect other course concepts to this journey and the research mapping.
