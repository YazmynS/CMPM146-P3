import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack_strongest_enemy(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    if not strongest_planet:
        return False

    # (3) Find the largest beatable enemy planet.
    beatable_enemy_planets = [p for p in state.enemy_planets() if strongest_planet.num_ships > p.num_ships]
    if not beatable_enemy_planets:
        return False

    largest_beatable_enemy = max(beatable_enemy_planets, key=lambda p: p.num_ships)

    # (4) Send half the ships from my strongest planet to the largest beatable enemy planet.
    return issue_order(state, strongest_planet.ID, largest_beatable_enemy.ID, strongest_planet.num_ships / 2)


def attack_weakest_neutral(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my weakest planet.
    weakest_planet = min(state.my_planets(), key=lambda p: p.num_ships, default=None)
    if not weakest_planet:
        return False

    # (3) Sort neutral planets by the number of ships in ascending order.
    neutral_planets_sorted = sorted(state.neutral_planets(), key=lambda p: p.num_ships)
    if not neutral_planets_sorted:
        return False

    # (4) Find the weakest beatable neutral planet and attack.
    for neutral_planet in neutral_planets_sorted:
        if weakest_planet.num_ships > neutral_planet.num_ships:
            return issue_order(state, weakest_planet.ID, neutral_planet.ID, weakest_planet.num_ships / 2)

    return False

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def reinforce_threatened_planet(state):
    my_planets = state.my_planets()
    enemy_fleets = state.enemy_fleets()

    threatened_planet = None
    for planet in my_planets:
        for fleet in enemy_fleets:
            if fleet.destination_planet == planet.ID:
                threatened_planet = planet
                break
        if threatened_planet:
            break

    if threatened_planet:
        # Find the closest planet with available ships to reinforce
        closest_planet = None
        min_distance = float('inf')
        for planet in my_planets:
            if planet.num_ships > 1 and planet.ID != threatened_planet.ID:
                distance = state.distance(planet.ID, threatened_planet.ID)
                if distance < min_distance:
                    closest_planet = planet
                    min_distance = distance

        if closest_planet:
            num_ships_to_send = closest_planet.num_ships // 2  # Send half of the ships
            state.issue_order(closest_planet.ID, threatened_planet.ID, num_ships_to_send)
            return True

    return False


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
