

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

#ADDED
def weak_planet_exists(state):
    low_ship_num = 10
    for planet in state.my_planets():
        if planet.num_ships <= low_ship_num:
            return True
    return False

# def centeral_planet_status(state):

