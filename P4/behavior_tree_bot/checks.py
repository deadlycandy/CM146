import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

#Checks for neutral planet
def if_neutral_planet_available(state):
    return any(state.neutral_planets())

#Checks for neutral planet
def if_no_neutral_planet_available(state):
    return (len(state.neutral_planets()) == 0)

#Checks if an enemy planet is within the players planets
def enemy_planets_near(state):
    if len(state.my_planets()) < 1:
        return False

    start_planet = state.my_planets()[0]
    total = 0
    for planet in state.my_planets():
        total += state.distance(start_planet.ID, planet.ID)
    avg = total / len(state.my_planets())

    for planet in state.my_planets():
        for enemy_planet in state.enemy_planets():
            if avg > state.distance(planet.ID, enemy_planet.ID):
                return True
    return False

#Check if the player has the largest fleet
def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
           + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


# Checks whether a enemy fleet is incoming towards a player planet
def check_incoming(state):
    for fleet in state.enemy_fleets():
        for planet in state.my_planets():
            if fleet.destination_planet == planet.ID:
                return True
    return False

