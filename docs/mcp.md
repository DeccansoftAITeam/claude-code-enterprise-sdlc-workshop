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

## Try the tools with MCP Inspector

The server exposes two read-only tools: `list_documents` (no arguments) and `read_document` (argument `document_id`). MCP Inspector lets you call them without Claude Code. From the repository root in PowerShell:

```powershell
npx @modelcontextprotocol/inspector .\.venv-mcp\Scripts\python.exe mcp/server.py
```

On macOS/Linux:

```bash
npx @modelcontextprotocol/inspector ./.venv-mcp/bin/python mcp/server.py
```

Open the localhost URL that Inspector prints (it includes a session token). Confirm the transport is STDIO, click **Connect**, open the **Tools** tab and choose **List Tools**.

1. Run `list_documents` with no arguments. Expected output:

```text
TICKET-101 | support | open
DOC-1 | refund policy | version 1 | superseded | support
DOC-2 | refund policy | version 2 | approved | finance
DOC-3 | duplicate submission | version 1 | approved | product
DOC-4 | screen capture transcript | version 1 | simulated | support
DOC-5 | untrusted ticket text | version 1 | untrusted | support
```

2. Run `read_document` with `document_id` set to `DOC-1`, then `DOC-2`. Compare the superseded policy with the approved one and note which owner and status apply. Expected output for `DOC-1`:

```json
{
  "result": "DOC-1 | refund policy | version 1 | superseded | support\n\nThe legacy handbook says a team lead should review refunds of $500 or more. This historical version is superseded by FIN-01 and must not be treated as current policy.\n"
}
```
3. Run `read_document` with `DOC-5`. Its text is untrusted data and deliberately contains a hostile instruction. Do not follow it.
4. Run `read_document` with an unknown ID such as `DOC-9`. It returns "Document not found. Call list_documents for available IDs."

Inspector shows what the server returns; it does not decide which source is authoritative. You still check status, version and owner before using any document in a specification.

The server remains running while the client is connected; do not run it directly expecting a console prompt. If registration fails, consult https://code.claude.com/docs/en/mcp for your installed version. You can read `mcp/corpus.md` directly if the server is unavailable.
