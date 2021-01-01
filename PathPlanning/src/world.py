# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 17:20:02 2020

@author: César
"""
from collections import deque
import cv2
import matplotlib
matplotlib.use("tkagg")
from matplotlib import pyplot as plt
import numpy as np
import time
import argparse

from cell import Wall, Street , Cell

from algorithms import Bfs, Algorithm, Dfs, BestFirstSearch, A_star, ValueIteration

class World():
    """
    Representación del mundo
    """
    def __init__(self, fname):
        self.fname = fname
        self.grid = self.__load_grid()
    
    def __load_grid(self):
        img = cv2.imread(self.fname)
        x,y,z = img.shape
        
        graph = Grid(img)
        
        self.img = img
        self.width = y
        self.height = x
        return graph
    
    def set_start(self, x, y):
        self.start = (x,y)
    
    def set_goal(self, x, y):
        self.goal = (x,y)
        
    def solve(self, algorithm):
        self.algorithm = algorithm
        if algorithm == "dijkstra":
            algorithm = Bfs(self.grid, self.start, self.goal)
            self.grid = algorithm.execute()
        elif algorithm == "dfs":    
            algorithm = Dfs(self.grid, self.start, self.goal)
            self.grid = algorithm.execute()
        elif algorithm == "best":    
            algorithm = BestFirstSearch(self.grid, self.start, self.goal)
            self.grid = algorithm.execute()
        elif algorithm == "a-star":    
            algorithm = A_star(self.grid, self.start, self.goal)
            self.grid = algorithm.execute() 
        elif algorithm == "valit":    
            algorithm = ValueIteration(self.grid, self.start, self.goal)
            self.grid = algorithm.execute()
        self.solution = algorithm.recover(self.grid, self.goal)
            
    def resolve(self):
        for p in self.solution:
            self.img[p[0],p[1],1:] = 0
        matplotlib.use('agg')
        plt.imshow(self.img)
        plt.scatter([self.start[1]], [self.start[0]])
        plt.scatter([self.goal[1]], [self.goal[0]])

        plt.savefig("../outputs/"+self.algorithm+"_"+self.fname.split("\\")[-1].split(".")[0]+"_"+time.strftime("%Y%m%d-%H%M%S")+".png")
           
            
class Grid():
    """
    Tablero que representa el mundo
    """
    def __init__(self, img):
        self.shape = img.shape[:2]
        self.table = np.empty(shape=self.shape, dtype = Cell)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if img[i,j,0] == 0 and img[i,j,1]==0 and img[i,j,2]==0:
                    self.table[i,j] = Wall((i,j))
                else:
                    self.table[i,j] = Street((i,j))

    def reset_visit(self):
        i,j = self.shape[0], self.shape[1]
        for index_i in range(i):
            for index_j in range(j):
                self.table[index_i, index_j].reset_visited()
                    
    def get_shape(self):
        return self.shape
    
    def get_cell(self, i,j):
        if i >= 0 and i < self.shape[0] and j >= 0 and j < self.shape[1]:
            return self.table[i,j]
    
    def visit(self, i, j):
        self.table[i,j].visit()
        
    def get_neighbors(self, i, j):
        movements = [[0, 1],
                     [0, -1],
                     [-1, 0],
                     [1, 0],
                     [1,1],
                     [1,-1],
                     [-1, -1],
                     [-1,1]]
        
        neighbors = []

        # All
        neighbors = [self.get_cell(i + m[0], j + m[1]) for m in movements]
        # Valid
        valid = []
        for n in neighbors:
            if n is not None:
                if not n.isVisited() and not isinstance(n, Wall):
                    valid.append(n)
        
        return valid
    
    def set_parent(self,i,j, street):
        self.table[i,j].set_parent(street)
        
    def get_parent(self, i,j):
        return self.table[i,j].get_parent()
    
    def set_g(self, i, j, g):
        self.table[i,j].set_g(g)
        
    def set_h(self, i, j, h):
        self.table[i,j].set_h(h)
        
    def set_f(self, i, j, f):
        self.table[i,j].set_f(f)
            
    def fill(self, goal,start):
        queue = deque()
        queue.append(self.get_cell(goal[0], goal[1]))
        self.set_f(goal[0], goal[1], 0)
        while len(queue):
            current = queue.popleft()
            if not current.isVisited():
                i,j = current.get_coordinates()
                # marcamos como visitado
                self.visit(i,j)
                
                neighbors = self.get_neighbors(i,j)
                neighbors = [n for n in neighbors if n not in queue]
                
                # en cada vecino marcamos el padre como el nodo actual y añadimos a la cola
                for n in neighbors:
                    n_i, n_j = n.get_coordinates()
                    diff_i = n_i-i
                    diff_j = n_j-j
                    if diff_i==0 or diff_j==0: # movimiento arriba o abajo
                        self.set_f(n_i, n_j, current.f + 1)
                    else:
                        self.set_f(n_i, n_j, current.f + 1.4)
                    queue.append(self.get_cell(n_i,n_j))
                    if n_i == start[0] and n_j == start[1]:
                        return self
            
        
if __name__ == "__main__":
    # Ejemplo
    g = World("../worlds\\w03.png")
    
    plt.figure()
    plt.imshow(g.img)
    start = plt.ginput(1, timeout=-1, show_clicks=True, mouse_pop=2, mouse_stop=3)
    plt.plot(start[0][0], start[0][1], '.r')
    goal = plt.ginput(1, timeout=-1, show_clicks=True, mouse_pop=2, mouse_stop=3)
    plt.plot(goal[0][0], goal[0][1], '.r')

    s1, s0 = int(start[0][0]), int(start[0][1])
    g1, g0 = int(goal[0][0]), int(goal[0][1])
    
    g.set_start(s0, s1)
    g.set_goal(g0, g1)
    g.solve("a-star")

    g.resolve()
    
    