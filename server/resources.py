async def get_pokemon_handler(name: str) -> dict:
    """Fetch Pokémon data from API or database."""
    return {"name": name, "stats": {}, "types": [], "moves": []}
