from mcp.server.fastmcp import FastMCP


mcp = FastMCP("server1")

@mcp.tool(
    name="find_products",           # Custom tool name for the LLM
    description="Search the product catalog with optional category filtering.", # Custom description
)
def tool1_func(query: str, category: str | None = None) -> str:
    return "tool output"