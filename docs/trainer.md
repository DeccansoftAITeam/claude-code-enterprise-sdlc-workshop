# Trainer guide

## Purpose and preparation
Participants are developers and architects who have completed three days of Claude Code training. This is an application day, not a beginner installation class. Rehearse all three branches, the local MCP connection, test commands and branch transitions on the actual classroom environment. Give participants access to the repository. Work in pairs; the trainer explains customer, BA, product, finance and security roles rather than assigning role-play. Do not expose real data or credentials.

## 0:00 to 1:00 Introduce the project
Explain: Northstar is a fictional retailer. A customer asks support for a refund. Support uses a small web application. Finance expects high-value refunds to be reviewed. The current system has a browser form, FastAPI service and local SQLite database. It records approvals but does not call a payment provider. Show the form and submit $501.00. Show that the result is APPROVED. Ask participants what they can conclude from that observation. Emphasize that current code shows behavior, not approved policy. Walk through the enterprise handoffs described in the participant workbook.

## 1:00 to 3:00 Discover and specify
Explain the ticket as an initial request, not a complete specification. Demonstrate the MCP document list and version status. Ask pairs to run the discovery prompt, inspect citations and draft the specification. At the checkpoint give these fictional stakeholder decisions: FIN-01 says amounts at or below $500 follow the standard path and amounts strictly above $500 need finance approval; finance may approve or reject. Product says identical requests under the same idempotency key must not duplicate the result or effect, and changed data under the same key conflicts. Security requires unauthorized approval to fail and be audited; demo identities are not production authentication. Data requires actor, action, target, authorization outcome, result, correlation, service version and time in audit, without the reason text. Balance, real provider, retention and production identity remain unresolved. Compare with stage1-spec.md. Explain DOC-1 is superseded and DOC-5 is hostile retrieved data.

## 3:00 to 5:00 Design and implement
Move everyone to 2-implement. Explain that the reference specification is the checkpoint baseline. Demonstrate asking Claude Code for a design and test plan; inspect its output before editing. Participants implement and verify. Discuss CLAUDE.md, rules, skills, permissions and the distinction between instructions and enforcement. Demonstrate one bounded review subagent where available. At the transition compare against the reference code and tests; different designs may be valid if they satisfy the specification and are evidenced. Do not describe fixed demo tokens as enterprise authentication or fake effects as a payment.

## 5:00 to 6:00 Review and release readiness
Move to 3-review. Explain that the branch contains deliberate defects. Ask pairs to derive checks from the specification and verify their findings. Compare with the separate review answer guide. Close with a go/no-go discussion: local tests alone do not prove hosted CI, independent approval, production security, staging or rollback. Highlight unresolved balance and provider rules. No deployment or assessment is required.

## Facilitation prompts
- What did you observe, and what is only an assumption?
- Which policy version has authority and who owns the decision?
- What happens at exactly $500 and at $500.01?
- What is the difference between an audit instruction and an enforced control?
- What evidence supports the release recommendation, and what remains unrun?

## Further reading
Research and question topics are summarized in docs/concept-map.md. Proposed source answers were not independently verified and must not be presented as an authoritative exam key. Official Claude Code documentation should be checked for version-sensitive configuration.

## Trainer demonstration sequence

### Explain the business before the code
Say: A customer requests a refund from Northstar support. Today the application immediately marks the refund approved, even for $501. The business wants finance to review high-value requests, while ordinary requests should not be slowed unnecessarily. Our job is to discover how the current application works, clarify the request, agree a testable specification, implement a change and decide whether evidence supports release. The trainer will provide the stakeholder decisions; participants remain developers and architects.

Draw the existing request path on a whiteboard: browser form -> FastAPI endpoint -> SQLite. Point out that SQLite stores a training record, not a bank transaction. Open the form, submit $501, and show the response. Show the baseline test and ask what it proves. Answer: it proves the behavior of this local version under that test, not the finance policy or any real provider behavior.

### Demonstrate evidence and the MCP boundary
Show `docs/mcp.md` and run the MCP check before class. Demonstrate listing documents and reading DOC-1 and DOC-2. Ask why the old policy cannot override the approved decision. Show DOC-5 and explain that an instruction in a ticket is source content, not authorization to perform an action. If MCP is unavailable, use the corpus file and label the connection demonstration unrun.

### Lead the specification checkpoint
Ask pairs for questions before providing the fictional stakeholder decisions. Explain how each decision becomes an observable criterion: 500.00 standard, 500.01 pending, support cannot approve, duplicate submission does not create a second effect. Ask who owns each decision. Keep remaining balance, production identity and provider behavior open. Give pairs time to compare their specification with the reference before moving on.

### Demonstrate plan, implementation and review
On branch 2, paste the planning prompt from STAGE.md. Show how the pair checks the plan and approves a bounded change. Demonstrate writing or requesting tests, running them, inspecting failures, implementing and running again. Show CLAUDE.md, the path-scoped rule and the review skill; explain the difference between project guidance and enforcement. If using a subagent, give it a read-only scope, specific inputs and an output contract. Check the resulting findings yourself.

### Close on release readiness
On branch 3, show how to inspect failing tests and reproduce the authorization problem. Avoid presenting an agent's review as an approval. The intended decision for the defective branch is no-go. Explain what evidence would still be needed for a real release, including production security, payment-provider behavior, protected audit, CI, staging and rollback. These are discussed rather than executed today.

### Hook demonstration
Open `.claude/settings.json`, explain the `SessionStart` event and run the script once to show its output. In Claude Code use `/hooks` to inspect the loaded hook. The reminder is context, not an access-control boundary. An organization must verify its permission settings and independent enforcement; this sample does not protect an audit database.
