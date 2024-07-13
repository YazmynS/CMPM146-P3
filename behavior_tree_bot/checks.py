          #Nuetral Checks
#Confirm there is a nuetral planet to take over
def if_neutral_planet_available(state):
    return any(state.neutral_planets())

#See if my weakest fleet can beat the weakest nuetral avaiable
# if so attack and move on to the new weakest neutral
# if not repeat the check with my next weakest fleet
def have_stronger_weak_fleet(state):
  return

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