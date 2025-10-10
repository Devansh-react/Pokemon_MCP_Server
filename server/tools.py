from typing import Dict, Any, Optional
from server.battle_engine import simulate_battle


async def battle_simulation_handler(
    pokemon_a: Dict[str, Any], 
    pokemon_b: Dict[str, Any], 
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Handler for Pokémon battle simulation tool.
    
    Args:
        pokemon_a: First Pokémon's stats and moves
        pokemon_b: Second Pokémon's stats and moves
        seed: Optional random seed for reproducibility
    
    Returns:
        Battle result with winner, rounds, and detailed log
    """
    return await simulate_battle(pokemon_a, pokemon_b, seed)
