#!/usr/bin/env python

import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check
from planet_wars import PlanetWars, finish_turn

def setup_behavior_tree():
    # Root node: High Level Strategy
    strategy_root = Selector(name='High Level Strategy')

    # Offensive Strategy
    offense_strategy = Sequence(name='Offensive Strategy')
    check_largest_fleet = Check(own_largest_fleet)
    check_no_neutral = Check(all_neutral_planets_captured)
    execute_attack = Action(attack_weakest_opponent)
    offense_strategy.child_nodes = [check_largest_fleet, check_no_neutral, execute_attack]

    # Spread Strategy
    spread_strategy = Sequence(name='Spread Strategy')
    check_neutral_planet = Check(neutral_planet_exists)
    execute_spread = Action(expand_to_best_neutral)
    spread_strategy.child_nodes = [check_neutral_planet, execute_spread]

    # Closest Weakest Spread Strategy
    closest_weakest_strategy = Sequence(name='Spread Closest Strategy')
    execute_closest_weakest_spread = Action(expand_to_closest_weakest)
    closest_weakest_strategy.child_nodes = [execute_closest_weakest_spread]

    # Defensive Strategy
    defense_strategy = Sequence(name='Defensive Strategy')
    check_under_attack = Check(is_under_attack)
    execute_defense = Action(defend_vulnerable_planet)
    defense_strategy.child_nodes = [check_under_attack, execute_defense]

    # Adding strategies to root node
    strategy_root.child_nodes = [offense_strategy, spread_strategy, closest_weakest_strategy, defense_strategy]

    logging.info('\n' + strategy_root.tree_to_string())
    return strategy_root

def do_turn(state):
    behavior_tree.execute(state)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)
    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
