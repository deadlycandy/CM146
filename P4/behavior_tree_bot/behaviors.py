import sys
sys.path.insert(0, '../')
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from planet_wars import issue_order

#Used for attacking the enemy with an agressive strategy
def attack_enemy_planet_aggressive(state):

    if len(state.enemy_planets()) < 1:
        return False

    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    my_planet = find_closest_strong_planet(state, state.my_planets(), weakest_planet)


    if not my_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, my_planet.ID, weakest_planet.ID, my_planet.num_ships * .8)


#Attacks the nearest weak enemy planet
def attack_weakest_near_enemy_planet(state):

    if len(state.enemy_planets()) < 1:
        return False

    #Finds the nearest planet based on an average distance of the players planets

    start_planet = state.my_planets()[0]
    total = 0
    for planet in state.my_planets():
        total += state.distance(start_planet.ID, planet.ID)
    avg = total / len(state.my_planets())

    for planet in state.my_planets():
        for enemy_planet in state.enemy_planets():
            if avg > state.distance(planet.ID, enemy_planet.ID):
                target_planet = enemy_planet

    if not target_planet:
        return False

    #Finds the strongest planet that is near to attack with

    my_planet = find_closest_strong_planet(state, state.my_planets(), target_planet)

    if not my_planet:
        # No legal source or destination
        return False

    if not my_planet or not target_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, my_planet.ID, target_planet.ID, my_planet.num_ships * .75)


#Given/modified
def attack_weakest_enemy_planet(state):

    if len(state.enemy_planets()) < 1:
        return False

    #Finds the best attack pair

    my_planet_1, target_planet =  find_closest_attack_pair_planet(state)

    #checks if there is a stronger planet around

    my_planet_2 = find_closest_strong_planet(state, state.my_planets(), target_planet)

    if not my_planet_1 or not my_planet_2 or not target_planet:
        # No legal source or destination
        return False

    #Determines which of the players planets to choose

    if state.distance(my_planet_1.ID, target_planet.ID) <= state.distance(my_planet_2.ID, target_planet.ID):
        my_planet = my_planet_1
    else:
        my_planet = my_planet_2

    if not my_planet or not target_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, my_planet.ID, target_planet.ID, my_planet.num_ships * .75)


#Given/Modified
def spread_to_weakest_neutral_planet(state):
    if len(state.neutral_planets()) < 1:
        return False

    #Finds the best neutral planet pairing

    my_planet_1, target_planet =  find_closest_neutral_pair_planet(state)

    #Finds the strongest planet around the targeted planet

    my_planet_2 = find_closest_strong_planet(state, state.my_planets(), target_planet)

    if not my_planet_1 or not my_planet_2 or not target_planet:
        # No legal source or destination
        return False

    #selects the players planet

    if state.distance(my_planet_1.ID, target_planet.ID) <= state.distance(my_planet_2.ID, target_planet.ID):
        my_planet = my_planet_1
    else:
        my_planet = my_planet_2

    if not my_planet or not target_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, my_planet.ID, target_planet.ID, target_planet.num_ships * .75)


#Sorts the players planets in weakest to strongest
def sort_player_planets(state):
    sort_player_planets = sorted(state.my_planets(), key = lambda shipobj: shipobj.num_ships)
    iter_player_planets = iter(sort_player_planets)
    return iter_player_planets


#Sorts the neutral planets in weakest to strongest
def sort_neutral_planets(state):
    num_planets = [planet for planet in state.neutral_planets()
                        if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    num_planets.sort(key = lambda shipObj: shipObj.num_ships)
    return num_planets


#Sorts the enemy planets in weakest to strongest
def sort_enemy_planets(state):
    enemy_planets = [planet for planet in state.enemy_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    #If my bot is not targetting that planet yet then return it
    enemy_planets.sort(key = lambda shipobj: shipobj.num_ships)
    return enemy_planets


#Sorts the enemy fleets by turns remaining
def sort_fleets_enemy(state):
    enemy_fleets_sorted = sorted(state.enemy_fleets(), key = lambda num_turns_left: num_turns_left.turns_remaining)
    iter_enemy_fleets = iter(enemy_fleets_sorted)
    return iter_enemy_fleets


#Finds the closets planet given a pivot point (my_planet)
def find_closest_planet(state, target_planets, my_planet):
    if len(state.my_planets()) < 1:
        return None

    closest_dst = state.distance(target_planets[0].ID, my_planet.ID)
    closest_planet = target_planets[0]
    for planet in target_planets:
        temp = state.distance(planet.ID, my_planet.ID)
        curr_minimum = closest_dst
        if temp < curr_minimum:
            closest_dst = temp
            closest_planet = planet

    return closest_planet


#Finds the strongest and closest planet to the target_planet (pivot point)
def find_closest_strong_planet(state, my_planets, target_planet):
    if len(state.my_planets()) < 1:
        return None

    closest_dst = state.distance(my_planets[0].ID, target_planet.ID)
    closest_planet = my_planets[0]
    ships_needed = target_planet.num_ships
    for planet in my_planets:
        temp = state.distance(planet.ID, target_planet.ID)
        curr_minimum = closest_dst
        curr_has_ships = planet.num_ships
        if temp < curr_minimum and curr_has_ships >= ships_needed:
            closest_dst = temp
            closest_planet = planet

    return closest_planet


#Finds the closet planet that support a planet which is about to be attacked
def find_closest_strong_planet_defense(state, my_planets, target_planet, enemy_fleet):
    if len(state.my_planets()) < 1:
        return None

    #utilizes an avg to distinguish between planets capeable of supporting

    total = 0
    for planet in state.my_planets():
        total += planet.num_ships
    avg  = total / len(state.my_planets())
    above_avg_planets = []
    for planet in state.my_planets():
        if planet.num_ships >= avg:
            above_avg_planets.append(planet)

    closest_dst = state.distance(above_avg_planets[0].ID, target_planet)
    closest_planet = above_avg_planets[0]
    ships_needed = enemy_fleet.num_ships/2

    for planet in above_avg_planets:
        temp = state.distance(planet.ID, target_planet)
        curr_minimum = closest_dst
        curr_has_ships = planet.num_ships
        if temp < curr_minimum and curr_has_ships >= ships_needed:
            closest_dst = temp
            closest_planet = planet

    return closest_planet


#Searchs for the best neutral pair (based on distance)
def find_closest_neutral_pair_planet(state):
    if len(state.my_planets()) < 1:
        return (None, None)

    closest_my_planet = state.my_planets()[0]
    closest_neutral_planet = state.neutral_planets()[0]

    for planet in state.my_planets():
        curr_planet_ships = planet.num_ships
        for neutral_planet in state.neutral_planets():
            ships_needed = neutral_planet.num_ships
            if state.distance(planet.ID, neutral_planet.ID) < state.distance(closest_my_planet.ID, closest_neutral_planet.ID) \
                    and curr_planet_ships >= ships_needed:
                closest_my_planet = planet
                closest_neutral_planet = neutral_planet

    if not closest_neutral_planet or not closest_my_planet:
        # No legal source or destination
        return (None, None)
    else:
        return (closest_my_planet, closest_neutral_planet)


#Searchs for the best attack pair (based on distance)
def find_closest_attack_pair_planet(state):
    if len(state.my_planets()) < 1:
        return (None, None)

    closest_my_planet = state.my_planets()[0]
    closest_enemy_planet = state.enemy_planets()[0]

    for planet in state.my_planets():
        curr_planet_ships = planet.num_ships
        for enemy_planet in state.enemy_planets():
            ships_needed = enemy_planet.num_ships
            if state.distance(planet.ID, enemy_planet.ID) < state.distance(closest_my_planet.ID, closest_enemy_planet.ID) \
                    and curr_planet_ships >= ships_needed:
                closest_my_planet = planet
                closest_enemy_planet = enemy_planet

    if not closest_enemy_planet or not closest_my_planet:
        # No legal source or destination
        return (None, None)
    else:
        return (closest_my_planet, closest_enemy_planet)


#Sends fleets towards a planet with enemy fleets inbound
def defend(state):

    enemy_fleets = sort_fleets_enemy(state)
    my_planets = sort_player_planets(state)

    if not my_planets or not enemy_fleets:
        return

    enemy_fleet = next(enemy_fleets)

    strong_planet = find_closest_strong_planet_defense(state, state.my_planets(), enemy_fleet.destination_planet, enemy_fleet)

    if not strong_planet or not enemy_fleet.destination_planet:
        return
    else:
        return issue_order(state, strong_planet.ID, enemy_fleet.destination_planet, enemy_fleet.num_ships)














