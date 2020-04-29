#!/usr/bin/env python
# coding: utf-8


import heapq
import math
import sys
from enum import Enum

EMPTY = 'WHITE'
PEDESTRIAN = 'RED'
TARGET = 'YELLOW'
OBSTACLE = 'BLACK'


class System:
    #A collection of cells
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(i, j) for i in range(rows)] for j in range(cols)]
        self.pedestrian = []
        self.target = None
        self.obstacle = []
        
    def add_pedestrian(self, pedestrian):
        #mark a pedestrian in the grid 
        self.grid[pedestrian[0]][pedestrian[1]].state = PEDESTRIAN
        self.pedestrian.append(pedestrian)
        
    def remove_pedestrian(self, pedestrian):
        #remove a pedestrian from the grid 
        if pedestrian in self.pedestrian:
            self.grid[pedestrian[0]][pedestrian[1]].state = EMPTY
            self.pedestrian.remove(pedestrian)
        else:
            print("No pedestrian found!")
        
    def add_target(self, target):
        #set the target of the grid, limit of 1 target
        if self.target is not None:
            self.grid[self.target[0]][self.target[1]].state = EMPTY
        self.target = target
        self.grid[target[0]][target[1]].state = TARGET
        return self.grid[target[0]][target[1]]
        
    def remove_target(self, target = None):
        #remove the target from the grid
        if target is not None:
            if self.target == target:
                self.target = None
            else:
                print("No such target found!")
        else:
            self.target = None
        
    def add_obstacle(self, obs):
        #add obstacle in the grid
        self.grid[obs[0]][obs[1]].state = OBSTACLE
        self.obstacle.append(obs)
        
def euclidean_distance(x, y):
    #this one has some problems
    #distance between a tuple of two coordinates
    return math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)
    
    
class Cell:
    #details of a cell
    #state of cell
    # EMPTY : empty
    # PEDESTRIAN : pedestrian
    # TARGET : target
    # OBSTACLE : obstacle
    def __init__(self, row, col, state = EMPTY):
        self.visited = False
        self.state = state
        self.row = row
        self.col = col
        self.distanceFromTarget = sys.maxsize
        self.adjacent_cells = []
        self.fmm_state = -1
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.row == other.row and self.col == other.col and self.state == other.state
        else:
            return False

    def __lt__(self, other):
        return self.distanceFromTarget < other.distanceFromTarget

    def set_distance(self, dist: int):
        self.distanceFromTarget = dist

    def get_distance(self):
        return self.distanceFromTarget

    def set_visited(self):
        self.visited = True

    def set_previous(self, cell):
        self.previous_cell = cell
        
        
def get_weight(cell: Cell):
    if cell.state == OBSTACLE:
        return sys.maxsize
    elif cell.state == TARGET:
        return 0
    elif cell.state == PEDESTRIAN:
        return 5
    return 1


def get_adjacent(cell, system):
    """
    Returns list of all the adjacent cells
    :param: Cell, System:
    :return: --> Cell
    """
    rows = system.rows
    cols = system.cols
    row = cell.row
    col = cell.col
    adjacent_cell = []
    if rows != (row+1):
        adjacent_cell.append(system.grid[row+1][col])
        if col + 1 != cols:
            adjacent_cell.append(system.grid[row+1][col+1])
        if col - 1 >= 0:
            adjacent_cell.append(system.grid[row+1][col-1])
    if row - 1 >= 0:
        adjacent_cell.append(system.grid[row-1][col])
        if col + 1 != cols:
            adjacent_cell.append(system.grid[row-1][col+1])
        if col - 1 >= 0:
            adjacent_cell.append(system.grid[row-1][col-1])
    if col + 1 != cols:
        adjacent_cell.append(system.grid[row][col+1])
    if col - 1 >= 0:
        adjacent_cell.append(system.grid[row][col-1])
        
    return adjacent_cell


def evaluate_cell_distance(system: System, target: Cell):
    target.set_distance(0)
    unvisited_queue = [(target.get_distance(), target)]

    while len(unvisited_queue):
        unvisited = heapq.heappop(unvisited_queue)
        current_cell = unvisited[1]
        # current_cell = heapq.heappop(unvisited_queue)
        current_cell.set_visited()

        for next_cell in get_adjacent(current_cell, system):
            if next_cell.visited:
                continue
            new_dist = current_cell.get_distance() + get_weight(next_cell)

            if new_dist < next_cell.get_distance():
                next_cell.set_distance(new_dist)
                next_cell.set_previous(current_cell)

        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)

        for row in system.grid:
            for cell in row:
                if not cell.visited:
                    unvisited_queue.append((cell.get_distance(), cell))
        heapq.heapify(unvisited_queue)



class fmm(system):
    #params: system -> grid style layout with pedestrians/obstacles and targets.

    def __init__():
        self.t_grid = [[(sys.maxsize) for i in range(system.rows)] for j in range(system.cols)]
        self.neighbor = []
        self.known = []
        self.system = system
        self.far = [(k.row, k.col) for i in self.grid for j in i]
        self.heap_neighbor = []                                     #heap for storing the neighbors and their calculated time in a tuple
        self.calc_values = []                                       #list containing coords of which the time is already calulated


    def far_to_neighbor(self, coord):
        #to take an element in the 'FAR' list to the 'NEIGHBOR' list
        #param: a tuple consisting of a pair of co-ordinates

        if coord in self.far:
            self.neighbor.append(self.far.pop(self.far.index(coord)))

        else:
            print("Incorrect format/Tuple doesnt exist in 'FAR'")


    def neighbor_to_known(self, coord):
        #to take an element in the 'NEIGHBOR' list to the 'KNOWN' list.
        #param: a tuple consisting of a pair of co-ordinates

        if coord in self.neighbor:
            self.known.append(self.neighbor.pop(self.neighbor.index(coord)))

        else:
            print("Incorrect format/Tuple doesnt exist in 'NEIGHBOR'")


    def add_time(self, time, coord):
        #adds a time to the t_grid matrix.
        #param: time -> time to be added, coord -> tuple of coordinates of the the point
        self.t_grid[coord[0]][coord[1]] = time
        
    
    def calc_time(self, cell):
        #implement this function
        #calculates the time take to go to the next cell
        #returns calculated time for a cell c
        #param: cell -> type(cell) for which the time is to be calculated.

        c = (cell.row, cell.col)
        t1 = max(self.t_grid[c[0]][c[1]] - self.t_grid[c[0] - 1][c[1]], self.t_grid[c[0]][c[1]] - self.t_grid[c[0] + 1][c[1]], 0)
        t2 = max(self.t_grid[c[0]][c[1]] - self.t_grid[c[0]][c[1] - 1], self.t_grid[c[0]][c[1]] - self.t_grid[c[0]][c[1] + 1], 0)
        t = 1/(((t1 ** 2) + (t2 ** 2)) ** 0.5)

        a = min(self.t_grid[c[0] - 1][c[1]], self.t_grid[c[0] + 1][c[1]])
        b = min(self.t_grid[c[0]][c[1] - 1], self.t_grid[c[0]][c[1] + 1])

        #Solving the quadratic equation
        T = None
        if t > abs(a-b):
            T = (a+b+(2*(t**2) - (a-b)**2)**0.5)/2
        else:
            T = t**2 + min(a, b)

        return (T * get_weight(cell), c)

    
    def insert_heap(self, data):
        #param: data - > tuple consisting of time, coordinates in a tuple. eg: (2, (2,25))
        #used to insert data to the heap
        heapq.heappush(self.heap_neighbor, data)

    def delete_heap(self, data):
        #param: data - > tuple consisting of time, coordinates in a tuple. eg: (2, (2,25))
        #used to delete and element from the heap while keeping the heap structure
        temp = list()
        while self.heap_neighbor:
            temp.append(heapq.heappop(self.heap_neighbor))
        temp.remove(data)
        heapq.heapify(temp)
        self.heap_neighbor = temp


    def check_double(self, data):
        #checks if the data is present in the heap or not. if it is, then the value which is lower will be kept.
        #param: data -> tuple with time as the first element and a tuple of coord as the second. eg: (2, (2, 25))
        temp = list()
        while self.heap_neighbor:
            temp.append(heapq.heappop(self.heap_neighbor))
        temp1 = [i[1] for i in temp]
        if data[1] in temp1:
            ind = temp1.index(data[1])
            if temp[ind][0] > data[0]:
                self.delete_heap(temp[ind])
                self.insert_heap(data)
                self.add_time(data[0], data[1])
            else:
                return
        else:
            heapq.heappush(self.heap_neighbor,data)


    def find_values(self, pedestrian = self.system.pedestrian):
        
        #param: pedestrian -> list of cells, the starting points/pedestrians.

        for i in pedestrian:
            row = i.row
            col = i.col
            cell = i

            #set the time for the start point to 0
            self.t_grid[row][col] = 0

            #put the the start point in the known list
            self.known.append((row, col))

            #get the target
            target = self.system.target

            while target not in self.known:
                self.neighbor.append(get_adjacent(cell, self.system))
                new_neighbors = [j for j in self.neighbor if j not in self.calc_values]
                time = self.calc_time(cell)         #time -> (time, (coord)) -> (2, (2, 25))
                self.check_double(time)
                self.calc_values.append(get_adjacent(i, self.system))
                cell = self.system.grid[time[1][0]][time[1][1]]

            self.known.append(heapq.heappop(self.heap_neighbor))

    

    

        


