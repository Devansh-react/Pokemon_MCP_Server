import asyncio
from server.battle_engine import simulate_battle
import json
import os

# Load pokemon_seed from the actual seed file
seed_path = os.path.join(os.path.dirname(__file__), "../seeds/pokemon_seed.json")
with open(seed_path, "r") as f:
    pokemon_seed = json.load(f)

pikachu = pokemon_seed["pokemon"][0]
charmander = pokemon_seed["pokemon"][1]

def test_battle_result():
    result = asyncio.run(simulate_battle(pikachu, charmander))
    assert "winner" in result
    assert len(result["battle_log"]) > 0
