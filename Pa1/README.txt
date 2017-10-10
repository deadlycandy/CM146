********** README **********

Dijkstra in a Dungeon --- CMPM 143 Game AI

Professor Shapiro
TA: J. Osborn

Written By: 
	Rahil Bhatnagar & Sean Woods

This program uses Dijkstra's algorithm with a forward search method to find the shortest path in a text file dungeon.
The walls are noted by X's and the cells are noted with weights (integers). There are waypoints that are lower case letters
and they have a fixed weight of 1. You select an initial position (waypoint or cell), and a destination of the same type.
It will then calculate the most efficient route and display it on the screen. This file also exports the shortest path to a file
along with all the weights to every path possible into a csv file.

p1.py -------------- This file holds the algorithms and main necessary for the program to run.
p1_support --------- Helper functions for reading in the graph (dungeon) and exporting the csv file.
my_maze.txt -------- This is the hand made dungeon, we used larger weights such as 4-5-6 to see how the program would avoid or use these weights.
test_maze_path.txt - The test maze shortest path from a to d. 
my_maze_costs.csv -- Cost to all paths exported into this csv from the intial point 'a' of the test_maze results.