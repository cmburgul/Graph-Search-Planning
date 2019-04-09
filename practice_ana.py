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

# Global variables
G = 99999999
E = 99999999


class node:
    def __init__(self, x, y):
        self.color = None
        self.x = x
        self.y = y
        self.e = 99999999  # a very high value
        self.f = None
        self.g = 99999999  # a very high value
        self.h = 99999999  # use Euclidean distance as heuristic
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
    return (math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)))

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


def is_goal(i, j, x2, y2, grid):
    if ((grid[i][j].x == x2) & (grid[i][j].y == y2)):
        return 1
    else:
        return 0


def print_node_info(a, b, grid):
    print("(%i, %i)" % (grid[a][b].x, grid[a][b].y))
    print("g : ", grid[a][b].g)
    print("h : ", grid[a][b].h)
    print("e : ", grid[a][b].e)
    print("parent_x :", grid[a][b].parent_x)
    print("parent_y : ", grid[a][b].parent_y)
    print("flag : ", grid[a][b].flag)


def trace_path(start_x, start_y, end_x, end_y, grid):
    global path
    path = []
    path.append(grid[end_x][end_y])
    c = end_x
    d = end_y
    while (not (is_goal(start_x, start_y, c, d, grid))):
        a = grid[c][d].parent_x
        b = grid[c][d].parent_y
        path.append(grid[a][b])
        c = a
        d = b

    for z in path:
        maze[z.x][z.y] = 5
        print("(%i, %i) --> " % (z.x, z.y))


def improve_solution():
    global x1
    global y1
    global x2
    global y2
    global G
    global E
    global open_list
    global grid
    global path

    print("improve_solution started")

    # Following the algorithm
    # Initialize the s = 0
    s = (0, 0)

    while (len(open_list) != 0):


        #print("Before E : ", E)
        max_e = open_list[0].e
        for index in range(len(open_list)):
            if (open_list[index].e >= max_e):
                E = open_list[index].e
                s = (open_list[index].x, open_list[index].y)

        open_list.remove(grid[s[0]][s[1]])
        #print("Removed node from the open_list (%i, %i)"%(grid[s[0]][s[1]].x, grid[s[0]][s[1]].y))

        #print("After E : ", E)

        # Check if s is a goal
        if (is_goal(grid[s[0]][s[1]].x, grid[s[0]][s[1]].y, x2, y2, grid)):
            trace_path(x1, y1, s[0], s[1], grid)
            success = True
            print("Reached Goal")
            G = grid[s[0]][s[1]].g

        #print(grid[s[0]][s[1]].x, grid[s[0]][s[1]].y, " Not a goal")

        directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]

        #print("All neighbors")
        for dir_index in range(len(directions)):
            #print(grid[s[0]][s[1]].x + directions[dir_index][0], grid[s[0]][s[1]].y + directions[dir_index][1])

            if (is_valid(grid[s[0]][s[1]].x + directions[dir_index][0], grid[s[0]][s[1]].y + directions[dir_index][1]) == 1):
                if (is_empty(grid[s[0]][s[1]].x + directions[dir_index][0], grid[s[0]][s[1]].y + directions[dir_index][1])  == 1):
                    if (grid[grid[s[0]][s[1]].x + directions[dir_index][0]][grid[s[0]][s[1]].y + directions[dir_index][1]].flag == False ):
                        i = grid[s[0]][s[1]].x + directions[dir_index][0]
                        j = grid[s[0]][s[1]].y + directions[dir_index][1]
                        #print ("valid")
                        #print("Parent g value", grid[s[0]][s[1]].g + 1)
                        #print("Child g value", grid[i][j].g)
                        if  (( int(grid[s[0]][s[1]].g + 1) ) <  int(grid[i][j].g) ):
                            grid[i][j].g = grid[s[0]][s[1]].g + 1
                            grid[i][j].h = cal_dist(grid[i][j].x, grid[i][j].y, grid[x2][y2].x, grid[x2][y2].y)
                            grid[i][j].parent_x = grid[s[0]][s[1]].x
                            grid[i][j].parent_y = grid[s[0]][s[1]].y
                            grid[i][j].flag = True
                            if ( (grid[i][j].g + grid[i][j].h) < G ):
                                open_list.append(grid[i][j])
                                maze[i][j] = 2
        #print("New node : ", i, j)
        #print_node_info(i, j, grid)



def ana_star(maze, start_node, exit_node):
    global G
    global E
    # Iniatilising success flag
    success = False

    # Initialize the Grid
    global grid
    grid = []
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
    global x1
    global y1
    global x2
    global y2
    x1 = start_node[0]
    y1 = start_node[1]
    x2 = exit_node[0]
    y2 = exit_node[1]

    grid[x1][y1] = node(x1, y1)
    grid[x1][y1]._set_color_(3)
    grid[x2][y2] = node(x2, y2)
    grid[x2][y2]._set_color_(4)

    # start._set_color_(3) in maze
    maze[x1][y1] = 3
    # goal._set_color_(4) in maze
    maze[x2][y2] = 4

    # Initialize start node
    grid[x1][y1].g = 0
    grid[x1][y1].h = cal_dist(grid[x1][y1].x, grid[x1][y1].y, grid[x2][y2].x, grid[x2][y2].y)
    grid[x1][y1].e = (G - grid[x1][y1].g) / (grid[x1][y1].h)
    grid[x1][y1].parent_x = x1
    grid[x1][y1].parent_y = y1
    grid[x1][y1].flag = True

    global open_list
    open_list = []
    i = x1
    j = y1
    open_list.append(grid[i][j])


    print("Node added in open_list (%i, %i)" % (i, j))

    # open_list.remove(grid[i][j])
    print ("-----Start-------")
    while (len(open_list) > 0):
        improve_solution()
        print ("Suboptimal G : %i"%G)

        # Pruning
        for i in path:
            if ( (i.g + i.h) >= G ):
                print("Yes Prune it at (%i, %i)" %(i.x, i.y))


        """
        open_list.remove(grid[i][j])
        # print("Node removed from open_list (%i, %i)" %(i, j))
        
        # front node i, j+1
        if (is_valid(i, j + 1) == 1):
            if (grid[i][j + 1].flag == False):
                # print ("Node valid (%i, %i)" %(i, j+1))
                if (is_empty(i, j + 1) == 1):
                    # print("Is added to open_list")
                    # print ("Node is_empty (%i, %i)" %(i, j+1))
                    if (is_goal(i, j + 1, x2, y2, grid)):
                        # print ("Write the trace path code")
                        trace_path(x1, y1, i, j, grid)
                        success = True
                    else:
                        grid[i][j + 1] = node(i, j + 1)
                        g = grid[i][j].g + 1
                        if (g < grid[i][j + 1].g):
                            grid[i][j + 1].g = grid[i][j].g + 1
                        grid[i][j + 1].h = cal_dist(grid[i][j + 1].x, grid[i][j + 1].y, grid[x2][y2].x, grid[x2][y2].y)
                        grid[i][j + 1].e = (G - grid[i][j + 1].g) / grid[i][j + 1].h
                        if (grid[i][j + 1].e < E):
                            E = grid[i][j + 1].e
                        grid[i][j + 1].parent_x = i
                        grid[i][j + 1].parent_y = j
                        grid[i][j + 1].color = 2
                        grid[i][j + 1].flag = True
                        open_list.append(grid[i][j + 1])
                        maze[i][j + 1] = 2
                        # print_node_info(i, j+1, grid)

        # top node i-1, j
        if (is_valid(i - 1, j) == 1):
            if (grid[i - 1][j].flag == False):
                # print ("Node valid (%i, %i)" %(i-1, j))
                if (is_empty(i - 1, j) == 1):
                    # print("Is added to open_list")
                    if (is_goal(i - 1, j, x2, y2, grid)):
                        # print ("Write the trace path code")
                        trace_path(x1, y1, i, j, grid)
                        success = True
                    else:
                        grid[i - 1][j] = node(i - 1, j)
                        g = grid[i][j].g + 1
                        if (g < grid[i - 1][j].g):
                            grid[i - 1][j].g = grid[i][j].g + 1
                        grid[i - 1][j].h = cal_dist(grid[i - 1][j].x, grid[i - 1][j].y, grid[x2][y2].x, grid[x2][y2].y)
                        grid[i - 1][j].e = (G - grid[i - 1][j].g) / grid[i - 1][j].h
                        if (grid[i - 1][j].e < E):
                            E = grid[i - 1][j].e
                        grid[i - 1][j].parent_x = i
                        grid[i - 1][j].parent_y = j
                        grid[i - 1][j].color = 2
                        grid[i - 1][j].flag = True
                        open_list.append(grid[i - 1][j])
                        maze[i - 1][j] = 2
                        # print_node_info(i-1, j, grid)

        # left node i, j-1
        if (is_valid(i, j - 1) == 1):
            if (grid[i][j - 1].flag == False):
                # print ("Node valid (%i, %i)" %(i, j-1))
                if (is_empty(i, j - 1) == 1):
                    # print("Is added to open_list")
                    if (is_goal(i, j - 1, x2, y2, grid)):
                        # print ("Write the trace path code")
                        trace_path(x1, y1, i, j, grid)
                        success = True

                    else:
                        grid[i][j - 1] = node(i, j - 1)
                        g = grid[i][j].g + 1
                        if (g < grid[i][j - 1].g):
                            grid[i][j - 1].g = grid[i][j].g + 1
                        grid[i][j - 1].h = cal_dist(grid[i][j - 1].x, grid[i][j - 1].y, grid[x2][y2].x, grid[x2][y2].y)
                        grid[i][j - 1].e = (G - grid[i][j - 1].g) / grid[i][j - 1].h
                        if (grid[i][j - 1].e < E):
                            E = grid[i][j - 1].e
                        grid[i][j - 1].parent_x = i
                        grid[i][j - 1].parent_y = j
                        grid[i][j - 1].color = 2
                        grid[i][j - 1].flag = True
                        open_list.append(grid[i][j - 1])
                        maze[i][j - 1] = 2
                        # print_node_info(i, j-1, grid)

        # bottom node i+1, j
        if (is_valid(i + 1, j) == 1):
            if (grid[i + 1][j].flag == False):
                # print ("Node valid (%i, %i)" %(i+1, j))
                if (is_empty(i + 1, j) == 1):
                    # print("Is added to open_list")
                    if (is_goal(i + 1, j, x2, y2, grid)):
                        # print ("Write the trace path code")
                        trace_path(x1, y1, i + 1, j, grid)
                        success = True
                    else:
                        grid[i + 1][j] = node(i + 1, j)
                        g = grid[i][j].g + 1
                        if (g < grid[i + 1][j].g):
                            grid[i + 1][j].g = grid[i][j].g + 1
                        grid[i + 1][j].h = cal_dist(grid[i + 1][j].x, grid[i + 1][j].y, grid[x2][y2].x, grid[x2][y2].y)
                        grid[i + 1][j].e = (G - grid[i + 1][j].g) / grid[i + 1][j].h
                        if (grid[i + 1][j].e < E):
                            E = grid[i + 1][j].e
                        grid[i + 1][j].parent_x = i
                        grid[i + 1][j].parent_y = j
                        grid[i + 1][j].color = 2
                        grid[i + 1][j].flag = True
                        open_list.append(grid[i + 1][j])
                        maze[i + 1][j] = 2
                        # print_node_info(i+1, j, grid)

        if (len(open_list) == 0):
            print("\nOpen list is empty\n")

        if (success == True):
            break

        print("nodes in the open_list")
        for z in open_list:
            print("(%i, %i)" % (z.x, z.y))

        print ('\n')
        print("-------Iteration------")

        print("Parent node :(%i, %i)" % (open_list[0].x, open_list[0].y))

        # Set Parent node
        i = open_list[0].x
        j = open_list[0].y
        """

    # This visualizes the grid. You may remove this and use the functions as you wish.
    maze[start_node[0]][start_node[1]] = 3
    maze[exit_node[0]][exit_node[1]] = 4
    draw_canvas(canvas, maze)
    root.update()

    return


def main():
    '''
    Define start and goal node. You may change how to define the nodes.
    '''
    entrance_node = (row - 1, 1)
    exit_node = (0, col - 2)

    print ("Start node : (%i, %i)" % (row - 1, 1))
    print ("Goal node : (%i, %i)" % (0, col - 2))

    start = t.clock()
    # run the ana_star algorithm
    ana_star(maze, entrance_node, exit_node)
    end = t.clock()
    print("Total time taken : ", end - start)

    root.mainloop()


if __name__ == '__main__':
    main()