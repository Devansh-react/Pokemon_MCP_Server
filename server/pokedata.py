import json
import os

async def get_pokemon_data(name: str):
    """Load Pokémon data from local JSON seed."""
    seed_path = os.path.join(os.path.dirname(__file__), "../seeds/pokemon_seed.json")
    with open(seed_path, "r") as f:
        data = json.load(f)

    for p in data["pokemon"]:
        if p["name"].lower() == name.lower():
            return p
    return {"error": f"Pokémon '{name}' not found"}
