#!/usr/bin/env python3
import httpx
from fastmcp import FastMCP

# Create an HTTP client for your API
client = httpx.AsyncClient(
    base_url="http://localhost:8000/",
    headers={
        "X-API-Key": "tH5j_Mp2U8ibvh_-3OH7EwgtE7SzlnNrCsnzzgr3F2Q",
    },
)

# Load your OpenAPI spec
openapi_spec = httpx.get("http://localhost:8000/openapi.json").json()

# Create the MCP server
mcp = FastMCP.from_openapi(openapi_spec=openapi_spec, client=client, name="API Server")

if __name__ == "__main__":
    mcp.run()
