import p1_support
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    # Initialize dictionaries and priority queque
    pq = []
    dist = {}
    prev = {}

    # Push all the coordinates into pq and sets distance to None
    for v in graph['walls']:
        heappush(pq, v)
        dist[v] = +inf
        prev[v] = None
    for v in graph['spaces']:
        heappush(pq, v)
        dist[v] = +inf
        prev[v] = None
    for v in graph['waypoints'].values():
        heappush(pq, v)
        dist[v] = +inf
        prev[v] = None

    # Starting point distance
    dist[initial_position] = 0

    # Runs till nothing left in pq
    while len(pq) != 0:
        # Find the neighbors around current vertex
        u = heappop(pq)
        adj = navigation_edges(graph, u)

        if u == destination:
            path = []
            path.append(destination)
            _visit = prev[destination]
            while _visit != initial_position:
                path.append(_visit)
                _visit = prev[_visit]
            path.append(initial_position)
            path.reverse()
            return path

        # Run through the distances
        for v in adj:
            newDist = v[1] + dist[u]
            if newDist < dist[v[0]]:
                dist[v[0]] = newDist
                prev[v[0]] = u

    return None


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    # Initialize dictionaries and priority queue
    pq = []
    dist = {}
    prev = {}

    # Starting point distancw
    prev[initial_position] = None
    heappush(pq, (0, [initial_position,None, 0]))
    dist[initial_position] = 0
    # u = heappop(pq)
    # print(u[0])
    # print(u[1])
    # print(u[1])
    for v in graph['spaces']:
        heappush(pq, (+inf, [v, None, graph["spaces"][v]]))
        dist[v] = +inf
    for v in graph['waypoints'].values():
        heappush(pq, (+inf, [v, None, 1]))
        dist[v] = +inf

    while len(pq) > 0:
    # for i in range(3):
        # Find the neighbors around current vertex
        u = heappop(pq)
        # print(u)
        # print('\n U: ', u,"\n")
        adj = navigation_edges(graph, u[1][0])
        # Run through the distances
        for v in adj:
            newDist = v[1] + u[0]
            # print('V[1]:', v[1], '\n')
            # print('u[0]:', u[0], '\n')
            # print('NewDist:', newDist, '\n')
            if v[0] in dist:
                if newDist < dist[v[0]]:
                    heappush(pq, (newDist, [v[0],u[1][0],v[1]]))
                    dist[v[0]] = newDist
    return dist


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    waypointWeight = 1
    x = cell[0]
    y = cell[1]
    adj = []

    if cell in level['spaces'] or cell in level['waypoints'].values():

        neighbors = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1),
                     (x, y - 1)]
        for i in range(len(neighbors)):
            if i % 2 == 0:  # Calculates the diagonal edges
                if neighbors[i] in level['spaces']:
                    weight = (sqrt(2) * 0.5 * level['spaces'][cell]) + (sqrt(2) * 0.5 * level['spaces'][neighbors[i]])
                    adj.append((neighbors[i], weight))
                elif neighbors[i] in level['walls']:
                    weight = +inf
                    adj.append((neighbors[i], weight))
                else:
                    weight = (sqrt(2) * 0.5) * level['spaces'][cell] + (sqrt(2) * 0.5) * waypointWeight
                    adj.append((neighbors[i], weight))
            else:  # Calculates Non-Diagonal edges
                if neighbors[i] in level['spaces']:
                    weight = (0.5 * level['spaces'][cell]) + (0.5 * level['spaces'][neighbors[i]])
                    adj.append((neighbors[i], weight))
                elif neighbors[i] in level['walls']:
                    weight = +inf
                    adj.append((neighbors[i], weight))
                else:
                    weight = (0.5 * level['spaces'][cell]) + (0.5 * waypointWeight)
                    adj.append((neighbors[i], weight))
    else:
        adj.append((cell, +inf))
    return adj


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = p1_support.load_level(filename)
    p1_support.show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        # Creating output text file
        outputFile = open("test_maze_path.txt", "w")
        string = str(path).strip('[]')
        outputFile.write(string)
        outputFile.close()
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """

    # Load and display the level.
    level = p1_support.load_level(filename)
    # p1_support.show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]

    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    p1_support.save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'example.txt', 'a', 'e'
    # level = p1_support.load_level(filename)
    # p1_support.show_level(level)
    # print(navigation_edges(level, (7,7)))

    # Use this function call to find the route between two waypoints.
    # test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_maze_costs.csv')
