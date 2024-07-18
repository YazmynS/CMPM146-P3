import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
from math import sqrt, ceil

def compute_distance(origin, target):
    
    #Calculate the Euclidean distance between two planets.
    
    dx = origin.x - target.x
    dy = origin.y - target.y
    return ceil(sqrt(dx * dx + dy * dy))

def engage_weakest_enemy(state):

    #Attack the weakest enemy planet from our strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_enemy_planet = min(state.enemy_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_enemy_planet:
        return False

    if strongest_planet.num_ships > weakest_enemy_planet.num_ships + 10:
        return issue_order(state, strongest_planet.ID, weakest_enemy_planet.ID, strongest_planet.num_ships // 2)

    return False

def expand_to_weakest_neutral(state):
    
    #Spread to the weakest neutral planet from our strongest planet.

    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_neutral_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_neutral_planet:
        return False

    return issue_order(state, strongest_planet.ID, weakest_neutral_planet.ID, weakest_neutral_planet.growth_rate + 1)

def expand_to_best_neutral(state):
    
    #Spread to the best neutral planet considering the growth rate and number of ships.
    
    if len(state.my_fleets()) > 0:
        return False

    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    neutral_planets_sorted = sorted(state.neutral_planets(), key=lambda p: (p.num_ships * (1 + 1/p.growth_rate)))
    best_neutral_planet = neutral_planets_sorted[0] if neutral_planets_sorted else None

    if not strongest_planet or not best_neutral_planet:
        return False

    return issue_order(state, strongest_planet.ID, best_neutral_planet.ID, best_neutral_planet.num_ships + 1)

def expand_to_adjacent_weakest(state):
    
    #Spread to the adjacent weakest planet (neutral or enemy).
    
    if len(state.my_planets()) < 1:
        return False

    adjacent_weakest_planet = None
    minimal_distance = float('inf')

    for our_planet in state.my_planets():
        for target_planet in state.not_my_planets():
            dist = compute_distance(our_planet, target_planet)
            if dist < minimal_distance and our_planet.num_ships > target_planet.num_ships + 10:
                minimal_distance = dist
                adjacent_weakest_planet = target_planet

    if adjacent_weakest_planet:
        nearest_our_planet = min(state.my_planets(), key=lambda p: compute_distance(p, adjacent_weakest_planet), default=None)
        if nearest_our_planet.num_ships > adjacent_weakest_planet.num_ships + 20:
            return issue_order(state, nearest_our_planet.ID, adjacent_weakest_planet.ID, adjacent_weakest_planet.num_ships + 20)

    return False

def defend_vulnerable_planet(state):
    
    #Defend our weakest planet that is under attack.

    planets_under_threat = [fleet.destination_planet for fleet in state.enemy_fleets() if fleet.destination_planet in [planet.ID for planet in state.my_planets()]]
    if not planets_under_threat:
        return False

    weakest_threatened_planet = min([planet for planet in state.my_planets() if planet.ID in planets_under_threat], key=lambda p: p.num_ships, default=None)
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    if not weakest_threatened_planet or not strongest_planet or strongest_planet.num_ships <= weakest_threatened_planet.num_ships:
        return False

    return issue_order(state, strongest_planet.ID, weakest_threatened_planet.ID, strongest_planet.num_ships // 2)

