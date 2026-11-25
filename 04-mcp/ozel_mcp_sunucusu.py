"""
CUSTOM_MCP_SERVER.PY — TAM ÇALIŞAN ÖRNEK
Slayt 35 — Özel MCP Sunucusu (FastMCP ile minimal boilerplate)
"""
import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sirket-erp-sunucusu")

ERP_URL = os.environ.get("ERP_URL", "https://erp.example.com")
ERP_TOKEN = os.environ.get("ERP_TOKEN", "")


@mcp.tool()
def get_inventory(urun_id: str) -> dict:
    """Ürün stok bilgisini ERP'den al"""
    response = requests.get(
        f"{ERP_URL}/inventory/{urun_id}",
        headers={"Authorization": f"Bearer {ERP_TOKEN}"},
    )
    return response.json()


if __name__ == "__main__":
    mcp.run()

# 1. pip install fastmcp
# 2. Araçları tanımla
# 3. Config'e ekle
# 4. Test et
