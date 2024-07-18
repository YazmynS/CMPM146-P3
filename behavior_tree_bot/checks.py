def neutral_planet_exists(state):
    """
    Check if there are any neutral planets available to capture.
    """
    return any(state.neutral_planets())

def all_neutral_planets_captured(state):
    """
    Check if there are no neutral planets available to capture.
    """
    return not any(state.neutral_planets())

def own_largest_fleet(state):
    """
    Check if we have the largest fleet compared to the enemy.
    """
    our_fleet_size = sum(planet.num_ships for planet in state.my_planets()) + sum(fleet.num_ships for fleet in state.my_fleets())
    enemy_fleet_size = sum(planet.num_ships for planet in state.enemy_planets()) + sum(fleet.num_ships for fleet in state.enemy_fleets())
    return our_fleet_size > enemy_fleet_size

def is_under_attack(state):
    """
    Check if any of our planets are under attack.
    """
    return any(fleet.destination_planet in [planet.ID for planet in state.my_planets()] for fleet in state.enemy_fleets())
