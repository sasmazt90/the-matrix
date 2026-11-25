"""
MY_MCP_SERVER.PY
Slayt 30 — Basit MCP Sunucusu Örneği (Python)
"""
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("dosya-arama-sunucusu")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_files",
            description="Dosyalarda metin ara",
        )
    ]


@server.call_tool()
async def call_tool(name, arguments):
    if name == "search_files":
        results = search(arguments["query"])
        return [TextContent(text=results)]


# Ajan artık search_files() çağırabilir


def search(query: str) -> str:
    """Yer tutucu — gerçek dosya arama implementasyonu projeye bağlıdır."""
    return f"'{query}' için sonuç bulunamadı."
