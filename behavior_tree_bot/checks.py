def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def no_neutral_planets_available(state):
    return not any(state.neutral_planets())

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
          + sum(fleet.num_ships for fleet in state.my_fleets()) \
          > sum(planet.num_ships for planet in state.enemy_planets()) \
          + sum(fleet.num_ships for fleet in state.enemy_fleets())
