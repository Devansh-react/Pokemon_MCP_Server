# main.py
from mcp.server.fastmcp import FastMCP
from server.resources import get_pokemon_handler
from server.tools import battle_simulation_handler

app = FastMCP("Pokémon MCP Server")

@app.resource(
    uri="pokemon://data/{name}",
    description="Fetch Pokémon data including stats, types, and moves."
)
async def get_pokemon_resource(name: str):
    """Handle Pokémon data fetching."""
    return await get_pokemon_handler(name)

@app.tool(
    description="Simulate a Pokémon battle between two Pokémon."
)
async def simulate_battle(pokemon_a: dict, pokemon_b: dict, seed: int | None = None):
    """Use the imported battle simulation handler."""
    return await battle_simulation_handler(pokemon_a, pokemon_b, seed)

if __name__ == "__main__":
    import sys
    sys.stderr.write("Starting Pokemon MCP Server...\n")
    app.run(transport="stdio")
