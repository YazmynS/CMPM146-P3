import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
from math import sqrt, ceil

def calculate_distance(source, destination):
    dx = source.x - destination.x
    dy = source.y - destination.y
    return ceil(sqrt(dx * dx + dy * dy))

def attack_weakest_enemy_planet(state):
    my_strongest = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_enemy = min(state.enemy_planets(), key=lambda p: p.num_ships, default=None)

    if not my_strongest or not weakest_enemy:
        return False

    if my_strongest.num_ships > weakest_enemy.num_ships + 10:
        return issue_order(state, my_strongest.ID, weakest_enemy.ID, my_strongest.num_ships // 2)

    return False

def spread_to_weakest_neutral_planet(state):
    my_strongest = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_neutral = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not my_strongest or not weakest_neutral:
        return False

    return issue_order(state, my_strongest.ID, weakest_neutral.ID, weakest_neutral.growth_rate + 1)

def spread_to_best_neutral_planet(state):
    if len(state.my_fleets()) > 0:
        return False

    my_strongest = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    neutral_planets = sorted(state.neutral_planets(), key=lambda p: (p.num_ships * (1 + 1/p.growth_rate)))
    best_neutral = neutral_planets[0] if neutral_planets else None

    if not my_strongest or not best_neutral:
        return False

    return issue_order(state, my_strongest.ID, best_neutral.ID, best_neutral.num_ships + 1)

def spread_to_closest_weakest_planet(state):
    if len(state.my_planets()) < 1:
        return False

    closest_planet = None
    shortest_distance = float('inf')

    for my_planet in state.my_planets():
        for not_my_planet in state.not_my_planets():
            dist = calculate_distance(my_planet, not_my_planet)
            if dist < shortest_distance and my_planet.num_ships > not_my_planet.num_ships + 10:
                shortest_distance = dist
                closest_planet = not_my_planet

    if closest_planet:
        closest_my_planet = min(state.my_planets(), key=lambda p: calculate_distance(p, closest_planet), default=None)
        if closest_my_planet.num_ships > closest_planet.num_ships + 20:
            return issue_order(state, closest_my_planet.ID, closest_planet.ID, closest_planet.num_ships + 20)

    return False
