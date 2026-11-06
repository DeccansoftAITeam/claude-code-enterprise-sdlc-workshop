# Northstar enterprise SDLC workshop

Northstar is a fictional online retailer. Support agents submit customer refunds; finance should review high-value requests. The current application immediately approves any positive amount. This workshop uses a single change to practice Claude Code and spec-driven development across an enterprise delivery flow. There is no real payment integration or production authentication.

## Six-hour route

| Time | Stage | Branch | Output |
|---|---|---|---|
| 0:00-1:00 | Understand the project and read the issue | 1-discover | Baseline observation |
| 1:00-3:00 | Discovery and specification | 1-discover | Rule register and specification |
| 3:00-5:00 | Design and implementation | 2-implement | Change and test evidence |
| 5:00-6:00 | Review and release readiness | 3-review | Findings and go/no-go rationale |

Each branch is a stand-alone starting point. Save your work before changing branches: `git switch -c my-work` creates a local branch. To begin another stage, commit your work locally, then `git switch 2-implement` (or `3-review`) and make another local branch. Compare against the solutions at each transition. Business roles (support, finance, product, security, data) are represented by the documents in `policy-docs/`.

`main`, `1-discover` and `2-implement` contain the baseline that approves any positive amount. `3-review` contains a completed-looking implementation with two deliberate defects; follow its `STAGE.md`, and expect the included tests to fail until you find and fix them. No branch deploys anything.

## Start the application

Windows PowerShell from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python -m uvicorn app:app --reload
```

On macOS/Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pytest -q
./.venv/bin/python -m uvicorn app:app --reload
```

Open http://127.0.0.1:8000 and submit $501.00. On the baseline branches the response is approved immediately. On `3-review`, use the review page and `STAGE.md`; a $500.01 request is held for finance approval. Stop the server with Ctrl+C. Use synthetic data only.

`python -m pytest -q` runs the tests under `tests/`.

## Your starting point

Open the GitHub issue **Refund approval for high-value refunds** (`gh issue view 1`). It links to the synthetic policy documents in [`policy-docs/`](policy-docs/README.md); check each document's status before relying on it. Write your spec with `/speckit-specify` using the six-section template (problem, stories, EARS criteria, open questions, plan, risk and gates), plan in Claude Code plan mode, and review with the built-in `/code-review`.

See `STAGE.md` for the current stage and `docs/participant.md` for the guided workbook. Reference code is a teaching solution, not production-ready financial software.
