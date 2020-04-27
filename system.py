#!/usr/bin/env python
# coding: utf-8



import math




class System:
    #A collection of cells
    def __init__(self, rows, cols):
        self.grid = [[Cell(i, j) for i in range(rows)] for j in range(cols)]
        self.pedastrian = []
        self.target = None
        self.obstacle = []
        
    def add_pedastrian(pedastrian):
        #mark a pedastrian in the grid 
        self.grid[pedastrian[0]][pedastrian[1]].state = 1
        self.pedastrian.append(pedastrian)
        
    def remove_pedastrian(pedastrian):
        #remove a pedastrian from the grid 
        if self.pedastrian has pedastrian:
            self.grid[pedastrian[0]][pedastrian[1]].state = 0
            self.pedastrian.remove(pedastrian)
        else:
            print("No pedastrian found!")
        
    def add_target(target):
        #set the target of the grid, limit of 1 target
        if self.target is not none:
            self.grid[self.target[0]][self.target[1]].state = 0
        self.target = target
        self.grid[target[0]][target[1]].state = 2
        
    def remove_target(target = self.target):
        #remove the target from the grid
        if self.target == target:
            self.target = None
        else:
            print("No such target found!")
        
    def add_obstacle(obs):
        #add obstacle in the grid
        self.grid[obs[0]][obs[1]].state = 3
        self.obstacle.append(obs)
        
    def euclidean_distance(x, y):
        #distance between a tuple of two coordinates
        return math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)
    
    
class Cell:
    #details of a cell
    #state of cell
    # 0 : empty
    # 1 : pedastrian
    # 2 : target
    # 3 : obstacle
    def __init__(self, row, col, state = 0):
        self.state = state
        self.row = row
        self.col = col
        





