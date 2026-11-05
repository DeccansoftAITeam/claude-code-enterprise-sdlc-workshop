import asyncio, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command=sys.executable, args=['mcp/server.py'])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert {t.name for t in tools.tools} == {'list_documents', 'read_document'}
            for doc, expected in [('TICKET-101', 'double-click'), ('DOC-1', 'superseded'), ('DOC-2', 'FIN-01'), ('DOC-5', 'malicious')]:
                result = await session.call_tool('read_document', {'document_id': doc})
                assert expected.lower() in result.content[0].text.lower(), (doc, result)
            print('MCP stdio: tool discovery and four documents passed')
asyncio.run(main())
