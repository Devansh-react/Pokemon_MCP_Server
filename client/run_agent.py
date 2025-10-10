from mcp.server.fastmcp import FastMCP
from server.resources import get_pokemon_handler
from server.tools import battle_simulation_handler

mcp = FastMCP("Pokémon MCP Server")
@mcp.resource(
    uri="pokemon://data/{name}",
    description="Fetch Pokémon data including stats, types, and moves."
)
async def get_pokemon_data(name: str) -> dict:
    """Fetch Pokémon data by name."""
    return await get_pokemon_handler(name)

@mcp.tool(
    description="Simulate a Pokémon battle between two Pokémon."
)
async def pokemon_battle(pokemon_a: dict, pokemon_b: dict, seed: int | None = None) -> dict:
    """Simulate a battle between two Pokémon."""
    return await battle_simulation_handler(pokemon_a, pokemon_b, seed)


if __name__ == "__main__":
    import sys

    sys.stderr.write("Starting Pokemon MCP Server...\n")
    mcp.run(transport="stdio")
