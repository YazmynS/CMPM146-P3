# - - - - - - - - - - Nuetral Checks - - - - - - - - - - #

#See if my weakest fleet can beat the weakest nuetral avaiable
# if so attack and move on to the new weakest neutral
# if not repeat the check with my next weakest fleet
def weakest_neutral(state):
    # Sort neutral planets by number of ships in ascending order
    neutral_planets = state.neutral_planets()
    sorted_neutral = sorted(neutral_planets, key=lambda p: p.num_ships)
    return sorted_neutral

def my_weakest(state):
    # Sort my fleets by number of ships in ascending order
    my_fleets = state.my_fleets()
    sorted_my_fleets = sorted(my_fleets, key=lambda f: f.num_ships)
    return sorted_my_fleets

def has_strongest_weak_fleet(state):
    # Get sorted lists of neutral planets and my fleets
    neutral_planets = weakest_neutral(state)
    my_fleets = my_weakest(state)
    
    # Iterate through my fleets starting from the weakest
    for my_fleet in my_fleets:
        if not neutral_planets:
            break  # No neutral planets to attack
        
        # Compare my weakest fleet with the weakest neutral planet
        weakest_neutral = neutral_planets[0]
        if my_fleet.num_ships > weakest_neutral.num_ships:
            # Attack the weakest neutral planet
            state.attack(my_fleet, weakest_neutral)
            return True  # Attack initiated
        else:
            # Remove the neutral planet from the list if the fleet cannot attack
            neutral_planets.pop(0)
    
    return False  # No suitable neutral planet found to attack



# - - - - - - - - - - Enemy Checks - - - - - - - - - - #

#See if my strongest fleet can beat the strongest enemy fleet
# if so attack and move on to the next strongest enemy
# if not repeat the check with the next strongest enemy fleet
def strongest_enemy(state):
  # Combine and sort enemy fleets and planets by number of ships in descending order
    enemy_planets = state.enemy_planets()
    enemy_fleets = state.enemy_fleets()
    
    all_enemies = enemy_planets + enemy_fleets
    sorted_enemies = sorted(all_enemies, key=lambda x: x.num_ships, reverse=True)
    
    return sorted_enemies
    
def my_strongest(state):
  # Find  strongest enemy planet and fleet
  my_strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships)
  my_strongest_fleet = max(state.my_fleets(), key=lambda f: f.num_ships)
    
  # if there are not fleets/ships left return None
  if not my_strongest_planet and not my_strongest_fleet:
    return None
  #if there's no planets return fleets and vis versa
  elif not my_strongest_planet:
    return my_strongest_fleet
  elif not my_strongest_fleet:
    return my_strongest_planet
  #return the strongest fleet or planet
  elif my_strongest_fleet >= my_strongest_planet:
    return my_strongest_fleet
  else: 
    return my_strongest_planet
  
def has_strongest_fleet(state):
  # Identify my strongest fleet or planet
  me = my_strongest(state)
    
  if not me:
    return None  # No forces to attack with
    
  # Iterate through sorted enemy forces
  for enemy in strongest_enemy(state):
    if me.num_ships > enemy.num_ships:
      # Attack the enemy
      state.attack(me, enemy)
      return True  # Attack initiated
    
  return False  # No suitable enemy found to attack

# - - - - - - - - - - Reinforcement Checks - - - - - - - - - - #
def reinforce_weak_planets(state, strongest_fleet):
  # Initialize variables
  threshold = 30
  reinforce_amount = 4
    
  # Look through weakest fleet for fleets under threshold
  my_weakest_fleets = my_weakest(state)
  my_weakest = [fleet for fleet in my_weakest_fleets if fleet.num_ships < threshold]
    
  # No fleets need reinforcement
  if not my_weakest:
    return  

  # Reinforce each weak fleet with a quarter of the strongest fleet's ships
  reinforce_size = strongest_fleet.num_ships // reinforce_amount
    
  # Only transfer if the strongest fleet has more than the reinforcement size
  if strongest_fleet.num_ships > reinforce_size:
    for weak_fleet in my_weakest:
      # Recalculate strongest fleet before each transfer
      strongest_fleet = my_strongest(state)
      # send reinforicements
      state.transfer_ships(strongest_fleet, weak_fleet, reinforce_size)