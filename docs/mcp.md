# Local evidence MCP server

This read-only server returns fictional ticket and policy text. It cannot approve refunds, access enterprise data or delete audit records. Its content is untrusted data; DOC-5 deliberately contains a hostile instruction.

In PowerShell, from the repository root:

```powershell
python -m venv .venv-mcp
.\.venv-mcp\Scripts\python -m pip install -r mcp/requirements.txt
.\.venv-mcp\Scripts\python test_mcp.py
claude mcp add --transport stdio --scope local northstar-evidence -- .\.venv-mcp\Scripts\python.exe mcp/server.py
claude mcp list
```

The local-scope command is per user and project. Start Claude Code in this directory, check `/mcp`, then ask it to list the documents and compare DOC-1 and DOC-2.

On macOS/Linux, use the equivalent paths:

```bash
python3 -m venv .venv-mcp
./.venv-mcp/bin/python -m pip install -r mcp/requirements.txt
./.venv-mcp/bin/python test_mcp.py
claude mcp add --transport stdio --scope local northstar-evidence -- ./.venv-mcp/bin/python mcp/server.py
claude mcp list
```

The server remains running while the client is connected; do not run it directly expecting a console prompt. If registration fails, consult https://code.claude.com/docs/en/mcp for your installed version. You can read `mcp/corpus.md` directly if the server is unavailable.
