## ANA* Algorithm

# import libraries
from sys import version_info
if version_info.major == 2:
    # We are using Python 2.x
    from Tkinter import *
    import ttk
elif version_info.major == 3:
    # We are using Python 3.x
    from tkinter import *
    from tkinter import ttk

import time as t
import numpy as np

'''
Define the color scheme for visualization. You may change it but I recommend using the same colors
'''
# white (0) is an unvisited node, black(1) is a wall, blue(2) is a visited node
# yellow(3) is for start node, green(4) is for exit node, red (5) is a node on the completed path
colors = {5: "red", 4: "green", 3: "yellow", 2: "blue", 1: "black", 0: "white"}


'''
Opens the maze file and creates tkinter GUI object
'''
# load maze
with open("easy.txt") as text:
    maze = [list(line.strip()) for line in text]
[col, row] = np.shape(maze)

# create map
root = Tk()
size = 700 / row
canvas = Canvas(root, width=(size*row), height=(size*col))
root.title("ANA* Algorithm")


G = 99999999
E = 99999999
optimal_path = []
exapnded_nodes = []

path_length = 0
total_no_exapnded_nodes = 0

class node:
    def __init__(self, val, x, y):
        self.color = val
        self.x = x
        self.y = y
        self.e = None
        self.f = None
        self.g = 99999999  # a very high value
        self.h = None  # use Euclidean distance as heuristic
        self.parent = None

    def update(self, val, f, g, h, parent):
        self.color = val
        self.f = f
        self.g = g
        self.h = h
        self.parent = parent

    def isGoal(self, goal):
        if self.x == goal.x and self.y == goal.y:
            return True
        else:
            return False

    def get_neighbors(self, open_list, maze):
        four_connected = ((-1,0), (0,-1), (1,0), (0,1))
        neighbors = []
        for dir1 in four_connected:
            #print(dir1)
            x = self.x + dir1[0]
            y = self.y + dir1[1]
            #print("---------------------")
            #print(x,y)
            if x < 0 or y < 0 or x > (len(maze)-1) or y > (len(maze[0])-1): # If out of bound block.
                continue
            elif int(maze[x][y].color) == 1:    # Visited node or obstacle, then dont add to neighbor
                continue

            neighbors.append(maze[x][y])  # Add node as neighbor of the cell

        return neighbors

    def in_open_list(self, x, y, open_list):
        for item in open_list:  # Check if node is already in open list
                if item.x == x and item.y == y:
                    return True
        return False


def draw_path(start, goal, maze1):
    global optimal_path
    if dist(start, goal) == 0:
        return maze1
    while(dist(start, goal) != 0):
        (x, y) = maze1[goal.x][goal.y].parent
        new_goal = maze1[x][y]
        maze1[x][y].color = 5
        optimal_path.append(maze1[x][y])
        return draw_path(start, new_goal, maze1)

def dist(a, goal):
    return np.sqrt((a.x - goal.x)**2 + (a.y - goal.y)**2) # Euclidean distance
    #return np.absolute(a.x - goal.x) + np.absolute(a.y - goal.y)

def draw_canvas(canvas, maze):
    '''
    Change this according to the data structure of your maze variable.
    If you are using a node class like the one mentioned below,
    You may have to change fill=colors[int(maze[i][j])] to fill=colors[int(maze[i][j].color)]
    '''
    for i in range(0, col):
        for j in range(0, row):
            canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill=colors[int(maze[i][j].color)])
    canvas.pack()


def erase_old_path():
    global maze1
    for i in range(len(maze1)):
        for j in range(len(maze1[0])):
            if maze1[i][j].color == 5:
                maze1[i][j].color = 0

def improve_solution():
    # Note: calculate G, h
    global G
    global E
    global maze1
    global open_list
    global goal
    global start
    global optimal_path
    global exapnded_nodes
    global total_no_exapnded_nodes

    exapnded_nodes = []
    while len(open_list) != 0:
        s = 0
        max = open_list[0].e
        for i in range(len(open_list)):
            if open_list[i].e > max:
                max = open_list[i].e
                s = i

        current = open_list.pop(s)
        maze1[current.x][current.y].color = 2
        exapnded_nodes.append(current)

        if current.e < E:
            E = current.e
        if current.isGoal(goal):
            G = current.g
            print("goal reached!")
            # Display current solution
            optimal_path = []
            maze1 = draw_path(start, goal, maze1)
            total_no_exapnded_nodes += len(exapnded_nodes)
            print("optimal_path length", len(optimal_path))
            print("no of exapnded_nodes: ", len(exapnded_nodes))
            optimal_path = []
            draw_canvas(canvas, maze1)
            root.update()
            t.sleep(2)
            return
        neighbors = current.get_neighbors(open_list, maze1)
        for neighbor in neighbors:
            if current.g + cost < neighbor.g:
                neighbor.g = current.g + cost
                maze1[neighbor.x][neighbor.y].g = current.g + cost
                maze1[neighbor.x][neighbor.y].parent = (current.x, current.y)
                neighbor.h = dist(neighbor, goal)
                if neighbor.h == 0.0:
                    neighbor.h = 0.000001
                if neighbor.g + neighbor.h < G:
                    neighbor.e = (G - neighbor.g)/neighbor.h
                    neighbor.parent = (current.x, current.y)
                    if neighbor.in_open_list(neighbor.x, neighbor.y, open_list):    # Check if node is already in open list
                        continue
                    open_list.append(neighbor)



def ana_star(maze, start_node, exit_node):
    # This visualizes the grid. You may remove this and use the functions as you wish.
    maze[start_node[0]][start_node[1]] = 3
    maze[exit_node[0]][exit_node[1]] = 4

    #draw_canvas(canvas, maze)
    #root.update()

    #-------------------------------------------YOUR CODE HERE--------------------------------------------------
    global G
    global E
    global maze1
    global start
    global goal
    global total_no_exapnded_nodes
    maze1 = [[node(maze[i][j], i, j) for j in range(len(maze[0]))] for i in range(len(maze))]
    goal = node(4, exit_node[0], exit_node[1])
    start = node(3, start_node[0], start_node[1])
    g = 0
    h = dist(start, goal)
    f = g+h
    start.update(3, f, g, h, None)
    start.e = (G - start.g)/start.h
    global open_list
    open_list = []
    closed_list = []
    open_list.append(start)
    global cost
    cost = 1
    count = 0

    while True:
        if len(open_list) == 0:     # If no more nodes to expand, and goal not reached
            print("total expanded nodes:", total_no_exapanded_nodes)
            return


        improve_solution()

        erase_old_path() # Make red nodes white

        if len(open_list) == 0:
            print("total expanded nodes:", total_no_exapnded_nodes)
            print("open_list is empty, COMPLETED ALL SEARCH")
            return
        for i, Open in enumerate(open_list):
            Open.g = maze1[Open.parent[0]][Open.parent[1]].g + cost
            Open.e = (G - Open.g)/Open.h
            if Open.g + Open.h >= G:
                open_list.pop(i)

        count = count + 1
        print(count)




    #-----------------------------------------------------------------------------------------------------------

    return


def main():

    '''
    Define start and goal node. You may change how to define the nodes.
    '''
    entrance_node = (row-1, 1)
    exit_node = (0, col-2)

    # If you are using a node class, you may want to convert each maze node to its class here
    '''
    global nodes
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            nodes.append(node(int(maze[i][j]), j, i))
    '''
    '''
    Run your ana_star algorithm function. You may choose to change the function or not use it.
    '''
    # run the ana_star algorithm
    ana_star(maze, entrance_node, exit_node)

    root.mainloop()

if __name__ == '__main__':
    main()