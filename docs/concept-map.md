# Online research: agentic SDLC and Claude Code

Research date: 2026-11-04. Inputs: enterprise_agentic_ai_engineering_guide.md and the 95-item claude-code-sdlc-questions-answers.json. The source discussions in the JSON are scraped certification-question discussions, not evidence that the questions appeared on a certification exam. Their answer keys and confidence percentages are claims made by the scraper, not independently validated. This report maps external material to question themes; a theme match does not establish the exact answer to every multiple-choice option.

## 1. Brownfield discovery and business logic

**Guide connection:** Parts 1?2 and coding-agent internals; existing ERP logic, evidence gathering, RAG, and locating code. Related dataset: CCA-F-068, 075, 078, 088, 089, 091, 093, 132.

- [From Code to Requirements: Agentic Reverse Engineering of Business Rules at Enterprise Scale](https://arxiv.org/abs/2609.22719) ? research on extracting business requirements from existing software. Useful for story-writing agents; treat extracted rules as hypotheses requiring evidence and domain-owner validation.
- [AgentModernize: Behavioral Specification Graphs](https://arxiv.org/abs/2605.17535) ? proposes an inspectable intermediate representation for preserving legacy business behavior. A research proposal, not proof of universal behavioral equivalence.
- [Legacy System Modernization with Coding Agents: A Case Study](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7397283) ? reports a corporate ERP VB6-to-C# migration case. Read for task boundaries and empirical limitations, not as a blanket enterprise performance guarantee.
- [Practitioner discussion: legacy Java codebases](https://www.reddit.com/r/LLMDevs/comments/1wycs9b/how_are_teams_making_coding_agents_useful_in/) ? practitioners discuss stale conventions and cross-service business contracts; anecdotal, useful as questions to investigate rather than verified outcomes.

Practical synthesis: trace claims from stories to code, configuration, existing tests and SME review; use characterization tests and independently check behavioral changes. MCP access to tickets alone does not establish complete business context.

## 2. Context, memory, sessions and long-running work

**Guide connection:** Parts 3?4. Related: CCA-F-054, 060, 067, 068, 071, 072, 077, 078, 079, 091, 132; CCAR-P-119, 121; CCDV-F-026, 028, 029, 038.

- [Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) ? context curation, just-in-time retrieval, compaction, notes and subagent isolation.
- [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) ? incremental work, durable progress artifacts and session reorientation. This is a demonstrated design, not a universal solution.
- [Claude Code memory](https://code.claude.com/docs/en/memory) ? current documentation on instruction files, imports and path-specific rules.

Key distinction: a compacted conversation, a resumed session and durable version-controlled project state are different mechanisms. Re-read changed files and verify repository state when resuming; a summary may omit facts. Avoid assuming one universal token threshold.

## 3. Orchestration, tools and parallel work

**Guide connection:** Part 5. Related: CCA-F-070, 073, 074, 080, 115, 133; CCAR-P-037; CCDV-F-013, 017.

- [How Anthropic built its multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) ? delegation, tool design and trade-offs. The article cautions that dependent coding tasks are less naturally parallel than independent research.
- [Building a C compiler with parallel Claudes](https://www.anthropic.com/research/building-c-compiler) ? practical long-running parallel coding experiment with tests and coordination; its substantial cost and setup limit generalization.
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents) ? current capabilities, tool restrictions, delegation, isolated context and resume.
- [Writing effective tools for agents](https://www.anthropic.com/research/writing-tools-for-agents) ? tool descriptions, interfaces and evaluation.

Practical synthesis: define scope, inputs, outputs and permissions for each worker; parallelize independent tasks; combine and verify outputs centrally. Better tool descriptions can help selection but are not a substitute for enforced access control.

## 4. Permissions, hooks and security

**Guide connection:** Part 6. Related: CCA-F-052, 061, 127; CCAR-P-045, 049, 065, 068, 113, 116, 123; CCDV-F-009, 016, 040.

- [Claude Code permissions](https://code.claude.com/docs/en/permissions) ? permission rules, compound commands, shell wrappers and coverage limitations.
- [Claude Code hooks reference](https://code.claude.com/docs/en/hooks) ? event-specific hook behavior, exit codes, timeouts and failure handling.
- [OWASP secure coding with AI](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html) ? risks across AI-assisted coding, repository content and tool use.
- [OWASP prompt injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) ? layered mitigations, authorization and action-specific approval.
- [OWASP MCP tool poisoning](https://community.owasp.org/attacks/MCP_Tool_Poisoning) ? risks from untrusted tool servers and tool responses.

Important qualification for CCA-F-061: instructions are behavioral guidance, while permissions and hooks can enforce particular actions when correctly configured. A file-tool deny rule alone may not cover every shell, process or network route. Test the actual configuration, failures, and bypass paths; use independent OS and backend controls where the risk requires them.

## 5. Review, tests, evaluation and delivery

**Guide connection:** Parts 1 and 6. Related: CCA-F-055, 063, 065, 073, 086, 089, 117?130; CCAR-P-023, 025, 040, 041, 046, 085, 108; CCDV-F-003, 004, 010, 024, 025, 039, 041, 045, 053. Ranges indicate the retained questions in that interval only.

- [Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) ? representative tasks, grading, repeated trials and regression checks.
- [Agentic Engineering](https://www.martinfowler.com/bliki/AgenticEngineering.html) ? engineering oversight, code review and feedback loops.
- [OWASP AI agent security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) ? structured security testing after changes to agent components.

Keep independent regression and security checks, human responsibility for risk decisions, and a way to roll back. An AI review or a passing test suite is evidence, not proof of correctness. Evaluate prompt/model changes against downstream contracts, representative examples and risk-specific failures.

## 6. Requirements, design, rollout and change

**Guide connection:** Part 1 and end-to-end implementation. Related: CCA-F-064, 087, 088; CCAR-P-075, 081, 087, 092, 093, 098, 102, 103, 104, 112, 118, 124; CCDV-F-011, 042, 048, 053.

- [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) ? translates broad goals into small, testable work with durable progress.
- [Agentic Engineering](https://www.martinfowler.com/bliki/AgenticEngineering.html) ? human direction and evaluation throughout delivery.

Use the guide's intake ? evidence ? specification ? design ? implementation ? independent verification ? approved release ? observation/rollback sequence as a working architecture, not an industry standard proven by a single source. For requirements, ADR and change-management questions, these articles offer background rather than a direct answer to each exam choice; further targeted evidence is needed.

## Research limitations and next pass

This is a topic-level first pass across the 95-item dataset, not a source-by-source validation of all 95 answers. Some questions concern specific CLI options, API behavior or project configuration whose current details require direct verification in the relevant product documentation. The JSON's proposed answers and numerical confidence scores should not be considered validated by this report. The interview transcript adds scenarios absent from the certification set, especially enterprise RAG and extracting business logic; the guide supplies a useful synthesis but should itself be checked against implementation evidence.

Next: make a per-question evidence table with exact IDs, specific passage links, source publication/version dates, and statuses: directly supported, partially supported, conflicting, or not yet verified.
