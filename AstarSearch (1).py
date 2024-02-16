# The import random will help in creating a randomly generated world every time the program runs
import random

class Node:
    def __init__(self, x, y, blocked):
        self.x = x
        self.y = y
        self.blocked = blocked
        self.parent = None
        self.g = 0 
        self.h = 0

    def f(self):
        return self.g + self.h

"""
The world size helps construct the 15x15 world
the blocked chance represents the percentage of 10% of the world to have randomly generated blocked nodes
""" 
world_size = 15
blocked_chance = 0.1

# Creates a tile based world with the nodes within it 
def create_world():
    world = [[None for _ in range(world_size)] for _ in range(world_size)]
    for x in range(world_size):
        for y in range(world_size):
            # This method will radnomly determine if the node will be unpathable or not based on the blocked_chance percentage of 10% of the 15x15 world
            blocked = random.random() < blocked_chance
            world[x][y] = Node(x, y, blocked)
    return world

# This method will use manhattan to find the distance between the two nodes that are selected
def find_manhattan_distance(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

# This method gets the available nodes that are for a node
def get_neighbors(node):
    neighbors = []
    if node.x > 0:
        neighbors.append(world[node.x - 1][node.y]) 
    if node.x < world_size - 1:
        neighbors.append(world[node.x + 1][node.y])
    if node.y > 0:
        neighbors.append(world[node.x][node.y - 1])
    if node.y < world_size - 1:
        neighbors.append(world[node.x][node.y + 1])
    return neighbors

# This method is the most important in using the astar algorithm in order to find the path from the starting node to the goal node
def a_star(start, goal):
    open_list = [start]
    closed_list = set()

    # The while loop will keep going until all of the available paths have been visited 
    while open_list:
        current_node = min(open_list, key=lambda node: node.f())
        open_list.remove(current_node)
        closed_list.add(current_node)

        # If statement checks when the goal is found recreate that path that was used to find the goal node
        if current_node == goal:
            return recreate_path(current_node)
        
        for neighbor in get_neighbors(current_node):
            if neighbor.blocked or neighbor in closed_list:
                continue

            tmp_g = current_node.g + 1
            # This if statement will changes the values based on the neighbor being in the open list
            if neighbor not in open_list or tmp_g < neighbor.g:
                neighbor.g = tmp_g
                neighbor.h = find_manhattan_distance(neighbor, goal)
                neighbor.parent = current_node
                if neighbor not in open_list:
                    open_list.append(neighbor)
    return None

# THis method will recreate the path that was used from the starting node to goal reversed 
def recreate_path(node):
    path = []
    while node is not None:
        path.append([node.x, node.y])
        node = node.parent
    return list(reversed(path))

# THis method will show the world itself based on the characters provided in the method
def display_world(world):
    for x in range(world_size):
        for y in range(world_size):
            node = world[x][y]
            if node.blocked:
                print("[X]", end="")
            else:
                print(" • ", end="")
        print()
              


if __name__ == "__main__":
    world = create_world()

while True:
    display_world(world)

    # Sets up a scanner to ask what the user wants the starting position and the goal position will be inside the created world
    start_x, start_y = map(int, input("Please enter a starting node (x y): ").split())
    goal_x, goal_y = map(int, input("Please enter a goal node (x y): ").split())

    start_node = world[start_x][start_y]
    goal_node = world[goal_x][goal_y]

    path = a_star(start_node, goal_node)

    if path:
        print("A path has been found!")
        for node in path:
            print(node) 
    else:
         print("Sorry! no path was able to be found")