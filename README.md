# Northstar enterprise SDLC workshop

Northstar is a fictional online retailer. Support agents submit customer refunds; finance should review high-value requests. The current application immediately approves any positive amount. This workshop uses a single change to practice Claude Code and spec-driven development across an enterprise delivery flow.

## Route

| Step | Stage | Branch | Output |
|---|---|---|---|
| 1 | Understand the project and read the issue | 1-discover | Baseline observation |
| 2 | Discovery and specification | 1-discover | Rule register and specification |
| 3 | Design and implementation | 2-implement | Change and test evidence |
| 4 | Review and release readiness | 3-review | Findings and go/no-go rationale |

Each branch is a stand-alone starting point. Save your work before changing branches: `git switch -c my-work` creates a local branch. To begin another stage, commit your work locally, then `git switch 2-implement` (or `3-review`) and make another local branch. Compare against the solutions at each transition. Business roles (support, finance, product, security, data) are represented by the documents in `policy-docs/`.

`main`, `1-discover` and `2-implement` contain the baseline that approves any positive amount. `3-review` contains a completed-looking implementation with two deliberate defects; follow its `STAGE.md`, and expect the included tests to fail until you find and fix them. No branch deploys anything.

## Get set up

You need Git, Python 3.10+, Claude Code and the GitHub CLI (`gh`). Run the commands below in a terminal (PowerShell, Terminal or bash). A free GitHub account is enough; the repository is public.

**1. Install `gh`** (https://cli.github.com)

```bash
winget install --id GitHub.cli     # Windows
brew install gh                    # macOS
```

On Linux, follow https://github.com/cli/cli/blob/trunk/docs/install_linux.md. Open a new terminal afterwards so `gh` is on your PATH, and check it with `gh --version`.

**2. Sign in to GitHub** (once per machine)

```bash
gh auth login
```

Choose **GitHub.com**, then **HTTPS**, answer **Yes** to authenticate Git with your GitHub credentials, then choose **Login with a web browser**. Copy the one-time code, press Enter, paste it in the browser and authorize. Confirm with `gh auth status`.

**3. Clone the repository and move into it**

```bash
gh repo clone DeccansoftAITeam/claude-code-enterprise-sdlc-workshop
cd claude-code-enterprise-sdlc-workshop
git switch 1-discover
```

(`git clone https://github.com/DeccansoftAITeam/claude-code-enterprise-sdlc-workshop.git` works too.) Everything else in this workshop happens inside this folder. `gh` reads the clone's `origin` remote, so inside this folder it already knows which repository to use; no `--repo` flag is needed.

**4. Read the issue, your entry point**

In the terminal, from the repository folder:

```bash
gh issue view 1
```

Or start Claude Code in the same folder (`claude`) and either ask it "Read GitHub issue 1 with gh and summarise it", or type `! gh issue view 1` to run the command yourself. Claude Code uses the same `gh` sign-in as your terminal. If it asks permission to run `gh`, allow it. Either way, you get the same text. The issue links to the documents in `policy-docs/`, which are already in your clone.

**No `gh`?** Open https://github.com/DeccansoftAITeam/claude-code-enterprise-sdlc-workshop/issues/1 in a browser and paste the text into Claude Code.

**GitHub MCP server (optional)** If your organization already uses it, `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` and authenticate when prompted, then ask Claude Code to read issue 1. It is not required.

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

Open the GitHub issue **Refund approval for high-value refunds** (`gh issue view 1`). It links to the synthetic policy documents in [`policy-docs/`](policy-docs/README.md); check each document's status before relying on it. Copy `docs/spec-template.md` to `docs/spec.md` (problem, stories, EARS criteria, open questions, plan, risk and gates), write and grill the spec in Claude Code plan mode, and review with the built-in `/code-review`.

See `STAGE.md` for the current stage and `docs/participant.md` for the guided workbook.
