"""
Battle engine implementing Pokémon turn order, damage calculation,
status effects, and reproducible randomization.

This is a simplified model intended for the MCP demo.
"""

import random
import math
import copy
from typing import Dict, Any, Optional
from server.type_chart import TYPE_EFFECTIVENESS


def calc_damage(attacker: Dict[str, Any], defender: Dict[str, Any], move: Dict[str, Any]) -> int:
    """Compute simplified Pokémon damage."""
    level = attacker.get("level", 50)
    power = move.get("power", 50)
    category = move.get("category", "physical")
    attack = attacker["stats"]["attack"] if category == "physical" else attacker["stats"].get("sp_attack", attacker["stats"]["attack"])
    defense = defender["stats"]["defense"] if category == "physical" else defender["stats"].get("sp_defense", defender["stats"]["defense"])
    move_type = move["type"]

    # Basic modifiers
    stab = 1.5 if move_type in attacker["types"] else 1.0
    type_effectiveness = TYPE_EFFECTIVENESS.get((move_type, defender["types"][0]), 1.0)
    random_factor = random.uniform(0.85, 1.0)
    modifier = stab * type_effectiveness * random_factor

    # Standard Pokémon damage formula (simplified)
    base = (((2 * level / 5 + 2) * power * (attack / defense)) / 50) + 2
    damage = math.floor(base * modifier)
    return max(damage, 1)


def apply_status_effect(pokemon: Dict[str, Any]) -> str:
    """Apply status effect damage or skip turn chance."""
    status = pokemon.get("status")
    if not status:
        return ""
    
    notes = ""
    if status == "burn":
        burn_dmg = math.floor(pokemon["stats"]["hp_max"] / 16)
        pokemon["stats"]["hp"] -= burn_dmg
        notes = f"{pokemon['name']} is hurt by its burn (-{burn_dmg})."
    elif status == "poison":
        psn_dmg = math.floor(pokemon["stats"]["hp_max"] / 8)
        pokemon["stats"]["hp"] -= psn_dmg
        notes = f"{pokemon['name']} is hurt by poison (-{psn_dmg})."
    elif status == "paralysis":
        if random.random() < 0.25:
            notes = f"{pokemon['name']} is paralyzed and cannot move!"
            pokemon["skip_turn"] = True
        else:
            pokemon["skip_turn"] = False
    return notes


async def simulate_battle(
    pokemon_a: Dict[str, Any], 
    pokemon_b: Dict[str, Any], 
    seed: Optional[int] = None, 
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Simulate battle and return structured logs.
    
    Args:
        pokemon_a: First Pokémon's data
        pokemon_b: Second Pokémon's data
        seed: Random seed for reproducible battles
        options: Additional battle options
    
    Returns:
        Dictionary containing winner, rounds, and battle log
    """
    if seed is not None:
        random.seed(seed)

    # Copy Pokémon so we don't mutate source
    a = copy.deepcopy(pokemon_a)
    b = copy.deepcopy(pokemon_b)

    # Set up stats for both
    for p in (a, b):
        p["stats"]["hp_max"] = p["stats"]["hp"]
        p["status"] = None
        p["skip_turn"] = False

    logs = []
    turn = 1

    while a["stats"]["hp"] > 0 and b["stats"]["hp"] > 0:
        logs.append({"turn": turn, "events": []})
        events = logs[-1]["events"]

        # Status effects (start of turn)
        for p in (a, b):
            note = apply_status_effect(p)
            if note:
                events.append(note)

        # Speed-based order
        first, second = (a, b) if a["stats"]["speed"] >= b["stats"]["speed"] else (b, a)

        # Two turns per round (if both alive)
        for actor, target in [(first, second), (second, first)]:
            if actor["stats"]["hp"] <= 0 or target["stats"]["hp"] <= 0:
                continue
            
            apply_status_effect(actor)  # apply paralysis check

            if actor.get("skip_turn"):
                events.append(f"{actor['name']} is fully paralyzed and skips the move.")
                continue

            move = actor["moves"][0]
            dmg = calc_damage(actor, target, move)
            target["stats"]["hp"] -= dmg

            # Apply chance for burn/poison/paralysis
            if random.random() < 0.1:  # 10% chance
                new_status = random.choice(["burn", "poison", "paralysis"])
                if not target["status"]:
                    target["status"] = new_status
                    events.append(f"{target['name']} is now {new_status}!")

            # Log the attack
            events.append(f"{actor['name']} used {move['name']} and dealt {dmg} damage.")
            events.append(f"{target['name']} has {max(target['stats']['hp'], 0)} HP remaining.")

            # Check faint
            if target["stats"]["hp"] <= 0:
                events.append(f"{target['name']} fainted!")
                break

        turn += 1

    winner = a["name"] if a["stats"]["hp"] > 0 else b["name"]
    return {"winner": winner, "rounds": turn - 1, "battle_log": logs}
