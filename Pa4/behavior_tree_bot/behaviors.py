# //order of opperations [protect near planets, attack center planet, attack rest of the planets]
# //protect near planets distance based
# //attack center planet we must overload the planet
# //attacking the rest of the planets lowest health points and nearest distance


import sys

sys.path.insert(0, '../')
from planet_wars import issue_order


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


# ADDED
def sort_player_planets(state):
    sort_player_planets = sorted(state.my_planets(), key=lambda shipobj: shipobj.num_ships)
    iter_player_planets = iter(sort_player_planets)
    return iter_player_planets


# ADDED
def sort_neutral_planets(state):
    num_planets = [planet for planet in state.neutral_planets() if
                   not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    num_planets.sort(key=lambda shipObj: shipObj.num_ships)
    return num_planets


# ADDED
def spread_to_closest_planet(state):
    # Sort player and neutral planets
    my_planets = sort_player_planets(state)
    neutral_planets = sort_neutral_planets(state)

    planets_to_target = iter(neutral_planets)

    try:
        my_planet = next(my_planets)
        if len(neutral_planets) > 0:
            target_planet = find_closest_planet(state, neutral_planets, my_planet)
        else:
            target_planet = next(planets_to_target)
        while True:
            ships_to_deploy = target_planet.num_ships + 1

            if my_planet.num_ships > ships_to_deploy:
                issue_order(state, my_planet.ID, target_planet.ID, ships_to_deploy)
                my_planet = next(my_planets)
                if len(neutral_planets) > 0:
                    target_planet = find_closest_planet(state, neutral_planets, my_planet)
                else:
                    target_planet = next(target_planet)
            else:
                my_planet = next(my_planets)
    except StopIteration:
        return False


# ADDED
def find_closest_planet(state, target_planets, my_planet):
    closest_dst = state.distance(target_planets[0].ID, my_planet.ID)
    closest_planet = target_planets[0]
    for planet in target_planets:
        temp = state.distance(planet.ID, my_planet.ID)
        curr_minimum = closest_dst
        if temp < curr_minimum:
            closest_dst = temp
            closest_planet = planet

    return closest_planet

#ADDED
def defend_weakest_planet(state):
    my_planets = sort_player_planets(state)
    low_ship_num = 10
    strong_planets = []
    for planet in my_planets:
        if planet.num_ships <= low_ship_num:
            target_planet = planet
        elif planet.num_ships >= 30:
            strong_planets.append(planet)
    try:
        strong_target_planet = find_closest_planet(state,strong_planets, target_planet)
        ships_to_deploy = (strong_target_planet.num_ships - target_planet.num_ships) * 0.5
        issue_order(state, strong_target_planet.ID, target_planet.ID, ships_to_deploy)
    except ValueError:
        pass
