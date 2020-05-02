#!/usr/bin/env python
# coding: utf-8
import heapq
import math
import sys
import numpy as np
import skfmm
from enum import Enum
from typing import Union, Tuple

EMPTY = 'WHITE'
PEDESTRIAN = 'RED'
TARGET = 'YELLOW'
OBSTACLE = 'BLACK'

R_MAX = 2


class Cell:
    # details of a cell
    def __init__(self, parent, col, row, state):
        self.system = parent
        self.visited = False
        self.state = state
        self.row = row
        self.col = col
        self.next_cell = None
        self.distance_utility = float(sys.maxsize)
        self.pedestrian_utility = 0
        self.adjacent_cells = []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.row == other.row and self.col == other.col and self.state == other.state
        else:
            return False

    def __lt__(self, other):
        return self.distance_utility < other.distance_utility

    def __str__(self):
        return "|(" + str(self.col) + "," + str(self.row) + ") Next Cell: " + str(self.next_cell.col) + "," \
               + str(self.next_cell.row) + ")|"

    def set_distance(self, dist: float):
        self.distance_utility = dist

    def get_utility(self):
        return float(self.distance_utility)

    def set_visited(self):
        self.visited = True

    def set_previous(self, cell):
        self.next_cell = cell

    def get_adjacent(self):
        """
        Returns list of all the adjacent cells
        :param: Cell, System:
        :return: --> Cell
        """
        rows = self.system.rows
        cols = self.system.cols
        row = self.row
        col = self.col
        adjacent_cell = []
        if rows != (row + 1):
            adjacent_cell.append(self.system.grid[row + 1][col])
            if col + 1 != cols:
                adjacent_cell.append(self.system.grid[row + 1][col + 1])
            if col - 1 >= 0:
                adjacent_cell.append(self.system.grid[row + 1][col - 1])
        if row - 1 >= 0:
            adjacent_cell.append(self.system.grid[row - 1][col])
            if col + 1 != cols:
                adjacent_cell.append(self.system.grid[row - 1][col + 1])
            if col - 1 >= 0:
                adjacent_cell.append(self.system.grid[row - 1][col - 1])
        if col + 1 != cols:
            adjacent_cell.append(self.system.grid[row][col + 1])
        if col - 1 >= 0:
            adjacent_cell.append(self.system.grid[row][col - 1])

        return adjacent_cell


class System:
    # A collection of cells
    def __init__(self, cols, rows):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(self, i, j, EMPTY) for i in range(cols)] for j in range(rows)]
        self.pedestrian = []  # Stores tuples of coordinate in the form (x: col, y: row)
        self.target: Cell = None
        self.obstacle = []  # Stores tuples of coordinate in the form (x: col, y: row)

    def __str__(self):
        for row in self.grid:
            print("\n")
            for cell in row:
                print(str(cell))

    def print_utilities(self):
        for row in self.grid:
            for cell in row:
                print("{:05.2f}".format(cell.distance_utility), end="  ")
            print()

    def add_pedestrian_at(self, coordinates: tuple):
        # mark a pedestrian in the grid
        cell: Cell = self.grid[coordinates[0]][coordinates[1]]
        self.pedestrian.append(cell)
        cell.state = PEDESTRIAN

    def remove_pedestrian_at(self, coordinates: tuple):
        # remove a pedestrian from the grid
        cell: Cell = self.grid[coordinates[0]][coordinates[1]]
        self.pedestrian.remove(cell)
        cell.state = EMPTY

    def add_target_at(self, coordinates: tuple):
        # set the target of the grid, limit of 1 target
        cell: Cell = self.grid[coordinates[0]][coordinates[1]]
        self.target = cell
        cell.state = TARGET
        return cell

    # def remove_target_at(self, coordinates: tuple):
    #     # remove the target from the grid
    #     cell = self.grid[coordinates[0]][coordinates[1]]
    #     self.target = cell
    #     cell.state = EMPTY

    def add_obstacle_at(self, coordinates: tuple):
        # add obstacle in the grid
        cell: Cell = self.grid[coordinates[0]][coordinates[1]]
        self.obstacle.append(cell)
        cell.state = OBSTACLE

    def no_obstacle_avoidance_update_sys(self):
        for cell in self.pedestrian:
            if cell is not None:
                for adjacent in cell.get_adjacent():
                    if adjacent.distance_utility < cell.distance_utility:
                        cell.next_cell = adjacent
                if cell.next_cell is None:
                    continue
            else:
                print('stuck')
            self.pedestrian.remove(cell)
            self.pedestrian.append(cell.next_cell)
            cell.state = EMPTY
            cell.next_cell.state = PEDESTRIAN

    def update_sys(self):
        for ped in self.pedestrian:
            if ped.next_cell == self.target:
                continue
            self.pedestrian.remove(ped)
            self.pedestrian.append(ped.next_cell)
            ped.state = EMPTY
            ped.next_cell.state = PEDESTRIAN

    def update_sys_fmm(self):
        for p in self.pedestrian:
            #print("reached here")
            path = self.calc_fmm((p.row, p.col))
            print((p.row, p.col), " --> ", path[0])
            if self.grid[path[0][0]][path[0][1]] == self.target:
                continue
            self.remove_pedestrian_at((p.row, p.col))
            self.add_pedestrian_at(path[0])
            print("reached here")
            #print(self.grid[self.pedestrian[0][0]][self.pedestrian[0][1]].state)

    def calc_fmm(self, p):
        t_grid = np.array(np.ones_like(self.grid), dtype=np.double)
        mask = np.array(0 * np.ones_like(self.grid), dtype=bool)
        t_grid[self.target.row, self.target.col] = -1
        for i in self.obstacle:
            mask[i.row][i.col] = True
        phi = np.ma.MaskedArray(t_grid, mask)
        d = skfmm.distance(phi)

        # print(d)

        return self.calc_fmm_path(d, p)

    def calc_fmm_path(self, distance, p):

        #print(p)
        path = []
        p_adj_cell = self.grid[p[0]][p[1]].get_adjacent()
        p_adj = [(i.row, i.col) for i in p_adj_cell]
        p_copy = p_adj

        p_adj = np.asarray(p_adj)
        row_idx = p_adj[:, 0]
        col_idx = p_adj[:, 1]
        d = distance[row_idx, col_idx]
        
        idx = np.where(distance == np.amin(d))
        idx = tuple(zip(idx[0], idx[1]))
        idx = [i for i in idx if i in p_copy]

        path.append(idx[0])

        return path

    def evaluate_cell_utilities(self):
        self.target.set_distance(0)
        unvisited_queue = [(self.target.get_utility(), self.target)]

        while len(unvisited_queue):
            unvisited = heapq.heappop(unvisited_queue)
            current_cell = unvisited[1]
            # current_cell = heapq.heappop(unvisited_queue)
            current_cell.set_visited()

            for next_cell in current_cell.get_adjacent():
                if next_cell.visited:
                    continue
                new_dist = current_cell.get_utility() + get_distance_utilities(current_cell, next_cell)

                if new_dist < next_cell.get_utility():
                    next_cell.set_distance(new_dist)
                    next_cell.set_previous(current_cell)
                    heapq.heappush(unvisited_queue, (next_cell.get_utility(), next_cell))

    def no_obstacle_avoidance(self):
        for row in self.grid:
            for cell in row:
                cell.distance_utility = get_euclidean_distance(cell, self.target)
                if cell.state == OBSTACLE:
                    cell.distance_utility = sys.maxsize


# def get_pedestrian_utilities(cell: Cell):


def get_euclidean_distance(x: Cell, y: Cell):
    # distance between two cells
    return math.sqrt((x.row - y.row) ** 2 + (x.col - y.col) ** 2)


def get_distance_utilities(current_cell: Cell, next_cell: Cell):
    if next_cell.state == OBSTACLE:
        return float(sys.maxsize)
    elif next_cell.state == TARGET:
        return 0.0
    elif next_cell.state == PEDESTRIAN:
        return 5.0
    return get_euclidean_distance(current_cell, next_cell)

