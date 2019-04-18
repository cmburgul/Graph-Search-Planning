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
import math

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
size = 800 / row
canvas = Canvas(root, width=(size * row), height=(size * col))
root.title("ANA* Algorithm")


class node:
    def __init__(self, x, y):
        self.color = None
        self.x = x
        self.y = y
        self.e = 99999999  # a very high value
        self.f = None
        self.g = 99999999  # a very high value
        self.h = None  # use Euclidean distance as heuristic
        self.parent_x = None
        self.parent_y = None
        self.flag = False

    def _set_color_(self, color_val):
        self.color = color_val

    def update_ghf(self, goal):
        self.g = self.parent.g + 1
        self.h = cel_dist(self.x, self.y, goal.x, goal.y)
        self.f = self.g + self.h


def cal_dist(x1, y1, x2, y2):
    dist = (math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)))
    if (dist == 0):
        return 0.01
    return dist

def draw_canvas(canvas, maze):
    '''
    Change this according to the data structure of your maze variable.
    If you are using a node class like the one mentioned below,
    You may have to change fill=colors[int(maze[i][j])] to fill=colors[int(maze[i][j].color)]
    '''
    for i in range(0, col):
        for j in range(0, row):
            canvas.create_rectangle(j * size, i * size, (j + 1) * size, (i + 1) * size, fill=colors[int(maze[i][j])])
    canvas.pack()


# Global variables
G = 99999999
E = 99999999
grid = []
open_list = []
x1 = 0
y1 = 0
x2 = 0
y2 = 0
start_node = (0, 0)
goal_node = (0, 0)

def is_empty(i, j):
    if (int(maze[i][j]) == 1):
        return 0
    else:
        return 1

def is_valid(i, j):
    if (i >= 0 and i <= row - 1 and j >= 0 and j <= col - 1):
        return 1
    else:
        return 0

def is_goal(i, j, x2, y2):
    global grid
    if ((grid[i][j].x == x2) & (grid[i][j].y == y2)):
        return 1
    else:
        return 0

def print_node_info(a, b):
    global grid
    print("(%i, %i)" % (grid[a][b].x, grid[a][b].y))
    print("g : ", grid[a][b].g)
    print("h : ", grid[a][b].h)
    print("f : ", grid[a][b].f)
    print("parent_x :", grid[a][b].parent_x)
    print("parent_y : ", grid[a][b].parent_y)
    print("flag : ", grid[a][b].flag)


def trace_path(start_x, start_y, end_x, end_y):
    global grid
    path = []
    path.append(grid[end_x][end_y])
    c = end_x
    d = end_y
    while (not (is_goal(start_x, start_y, c, d))):
        a = grid[c][d].parent_x
        b = grid[c][d].parent_y
        path.append(grid[a][b])
        c = a
        d = b

    for z in path:
        maze[z.x][z.y] = 5
        #print("(%i, %i) --> " % (z.x, z.y))

def trace_path_e():
    global G
    global E
    global grid
    global open_list
    global x1, y1, x2, y2
    global success
    global start_node
    global goal_node

    i = x2
    j = y2
    while (i != x1 and j != y1):
        grid[x2][y2]

def prune():
    global G
    global E
    global grid
    global open_list
    global x1, y1, x2, y2
    global success
    global start_node
    global goal_node

    for each_node in open_list:
        r = each_node.x
        s = each_node.y
        if (grid[r][s].g + grid[r][s].h >= G):
            open_list.remove(each_node)


def erase_old_path():
    global grid

    # Iterate through the Grid
    for i in range(row):
        for j in range(col):
            if (maze[i][j] == 5):
                maze[i][j] = 2

def update_e():
    global G
    global E
    global grid
    global open_list
    global x1, y1, x2, y2
    global success
    global start_node
    global goal_node

    for each_node in open_list:
        p = each_node.x
        q = each_node.y
        parent_x = grid[p][q].parent_x
        parent_y = grid[p][q].parent_y
        grid[p][q].g = grid[parent_x][parent_y].g + 1
        grid[p][q].h = cal_dist(p, q, x2, y2)
        grid[p][q].e = (G - grid[p][q].g) / grid[p][q].h

def improve_solution():

    global G
    global E
    global grid
    global open_list
    global x1, y1, x2, y2
    global success
    global start_node
    global goal_node

    while (len(open_list) > 0):

        # Assign max e(s) from all open list nodes as s

        max_e = -1
        for node_ in open_list:
            #print node_.e
            if (node_.e > max_e):
                max_e = node_.e
                i = node_.x
                j = node_.y

        #print "Selected node with maximum of e(s) from open list is (%i, %i)"%(i, j)

        open_list.remove(grid[i][j])
        # print("Node removed from open_list (%i, %i)" %(i, j))

        if (grid[i][j].e < E):
            E = grid[i][j].e

        if (is_goal(i, j ,x2, y2)):
            G = grid[i][j].g
            trace_path(x1, y1, i, j)
            success = True

        # Successors of grid[i][j]

        # front node i, j+1
        if (is_valid(i, j + 1) == 1):
            if (grid[i][j + 1].flag == False):
                if (is_empty(i, j + 1) == 1):

                    # Initialize the node(i, j+1)
                    grid[i][j + 1] = node(i, j + 1)

                    if ( (grid[i][j].g + 1) < grid[i][j + 1].g):
                        grid[i][j + 1].g = grid[i][j].g + 1

                        grid[i][j + 1].parent_x = i
                        grid[i][j + 1].parent_y = j
                        grid[i][j + 1].color = 2
                        grid[i][j + 1].flag = True
                        grid[i][j + 1].h = cal_dist(grid[i][j + 1].x, grid[i][j + 1].y, grid[x2][y2].x, grid[x2][y2].y)
                        grid[i][j + 1].e = (G - grid[i][j + 1].g) / grid[i][j + 1].h

                        if (grid[i][j+1].g + grid[i][j+1].h < G):
                            open_list.append(grid[i][j + 1])
                    maze[i][j + 1] = 2

        # top node i-1, j
        if (is_valid(i - 1, j) == 1):
            if (grid[i - 1][j].flag == False):
                if (is_empty(i - 1, j) == 1):

                    # Initialize the node(i-1)(j)
                    grid[i - 1][j] = node(i - 1, j)

                    if ( (grid[i][j].g + 1) < grid[i - 1][j].g):
                        grid[i - 1][j].g = grid[i][j].g + 1

                        grid[i - 1][j].parent_x = i
                        grid[i - 1][j].parent_y = j
                        grid[i - 1][j].color = 2
                        grid[i - 1][j].flag = True
                        grid[i - 1][j].h = cal_dist(grid[i - 1][j].x, grid[i - 1][j].y, grid[x2][y2].x, grid[x2][y2].y)
                        grid[i - 1][j].e = (G - grid[i - 1][j].g) / grid[i - 1][j].h

                        if (grid[i-1][j].g + grid[i-1][j].h < G):
                            open_list.append(grid[i - 1][j])
                    maze[i - 1][j] = 2

        # left node i, j-1
        if (is_valid(i, j - 1) == 1):
            if (grid[i][j - 1].flag == False):
                if (is_empty(i, j - 1) == 1):

                    # Initialize the node(i)(j-1)
                    grid[i][j - 1] = node(i, j - 1)

                    if ( (grid[i][j].g + 1) < grid[i][j - 1].g):
                        grid[i][j - 1].g = grid[i][j].g + 1

                        grid[i][j - 1].parent_x = i
                        grid[i][j - 1].parent_y = j
                        grid[i][j - 1].color = 2
                        grid[i][j - 1].flag = True
                        grid[i][j - 1].h = cal_dist(grid[i][j - 1].x, grid[i][j - 1].y, grid[x2][y2].x, grid[x2][y2].y)
                        grid[i][j - 1].e = (G - grid[i][j - 1].g) / grid[i][j - 1].h

                        if (grid[i][j - 1].g + grid[i][j-1].h < G):
                            open_list.append(grid[i][j - 1])
                    maze[i][j - 1] = 2

        # bottom node i+1, j
        if (is_valid(i + 1, j) == 1):
            if (grid[i + 1][j].flag == False):
                if (is_empty(i + 1, j) == 1):

                    # Initialize the node(i+1)(j)
                    grid[i + 1][j] = node(i + 1, j)

                    if ( (grid[i][j].g + 1) < grid[i + 1][j].g):
                        grid[i + 1][j].g = grid[i][j].g + 1

                        grid[i + 1][j].parent_x = i
                        grid[i + 1][j].parent_y = j
                        grid[i + 1][j].color = 2
                        grid[i + 1][j].flag = True
                        grid[i + 1][j].h = cal_dist(grid[i + 1][j].x, grid[i + 1][j].y, grid[x2][y2].x, grid[x2][y2].y)
                        grid[i + 1][j].e = (G - grid[i + 1][j].g) / grid[i + 1][j].h

                        if (grid[i + 1][j].g  + grid[i + 1][j].h < G):
                            open_list.append(grid[i + 1][j])
                    maze[i + 1][j] = 2

        if (success == True):
            break
        """    
        print("nodes in the open_list")
        for z in open_list:
            print("(%i, %i)" % (z.x, z.y))
        
        print ("E = ", E)

        print ('\n')
        print("-------Iteration------")

        print("Parent nodes :(%i, %i)" % (open_list[0].x, open_list[0].y))
        """
        # Set Parent node
        i = open_list[0].x
        j = open_list[0].y


    # This visualizes the grid. You may remove this and use the functions as you wish.
    maze[start_node[0]][start_node[1]] = 3
    maze[goal_node[0]][goal_node[1]] = 4
    draw_canvas(canvas, maze)
    root.update()

    return E

def ana_star(maze):
    global G
    global E
    global grid
    global open_list

    global x1, y1, x2, y2
    global success

    print ("G : ", G)
    print ("E : ", E)
    print ("OPEN List : ", len(open_list))

    global start_node
    global goal_node

    # Iniatilising success flag
    success = False

    # Initialize the Grid
    for i in range(row):
        x_row = []
        for j in range(col):
            node_ = node(i, j)
            x_row.append(node_)
        grid.append(x_row)

    """
    # Print the grid
    for i in range(row):
        for j in range(col):
            print("node_info : (%i, %i) "% (grid[i][j].x, grid[i][j].y))
    """

    # Set the start and goal node
    x1 = start_node[0]
    y1 = start_node[1]
    x2 = goal_node[0]
    y2 = goal_node[1]

    # Initialize start node
    grid[x1][y1] = node(x1, y1)
    grid[x1][y1].g = 0
    grid[x1][y1].h = cal_dist(grid[x1][y1].x, grid[x1][y1].y, grid[x2][y2].x, grid[x2][y2].y)
    grid[x1][y1].e = (G - grid[x1][y1].g) / (grid[x1][y1].h)
    grid[x1][y1].parent_x = x1
    grid[x1][y1].parent_y = y1
    grid[x1][y1].flag = True
    grid[x1][y1]._set_color_(3)

    grid[x2][y2] = node(x2, y2)
    grid[x2][y2]._set_color_(4)

    print ("Start Node : ")
    print_node_info(x1, y1)

    # start._set_color_(3)
    maze[x1][y1] = 3
    # goal._set_color_(4)
    maze[x2][y2] = 4

    # Initilize i, j as x1, y1
    i = x1
    j = y1
    open_list.append(grid[i][j])

    print("Node added in open_list (%i, %i)" % (i, j))
    # print(is_valid(i, j+1))

    print ("-----Start-------")

    count = 0
    while (len(open_list) != 0):
        improve_solution()
        t.sleep(0.05)
        t.sleep(0.05)
        print ("E-suboptimal : ", E)
        print ("pruning...")
        update_e()
        prune()
        #erase_old_path()
        count = count + 1
        print ("Improve Solution Count : ", count)
        print ("Length Open List : ", len(open_list))
    trace_path(x1, y1, x2, y2)



    return


def main():
    '''
    Define start and goal node. You may change how to define the nodes.
    '''
    global start_node
    global goal_node

    start_node = (row - 1, 1)
    goal_node = (0, col - 2)

    print ("Start node : (%i, %i)" % (row - 1, 1))
    print ("Goal node : (%i, %i)" % (0, col - 2))

    start = t.process_time()
    # run the ana_star algorithm
    ana_star(maze)
    end = t.process_time()
    print("Total time taken : ", end - start)


    # Print the grid
    for i in range(row):
        for j in range(col):
            print ("node_info : (%s, %s) " %(str(grid[i][j].x), str(grid[i][j].y)))
            print  ("Parent of node (%s, %s)" %(str(grid[i][j].parent_x), str(grid[i][j].parent_y)))

    print(goal_node)

    root.mainloop()



if __name__ == '__main__':
    main()