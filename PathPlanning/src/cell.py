# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:41:19 2020

@author: César
"""

class Cell():
    """
    Representación genérica de una celda
    """
    visited = False
    g = 0
    h = 0
    f = 10e8

    def __init__(self, coordinates):
        self.coordinates = coordinates
    
    def is_valid(self):
        pass
    
    def __str__(self):
        pass
    
    def get_coordinates(self):
        return self.coordinates[0], self.coordinates[1]
    
    def __eq__(self, other):
        return self.coordinates == other.coordinates
    
    def __lt__(self, other):
        return self.f < other.f
    
    def set_g(self, g):
        self.g = g
        
    def set_h(self, h):
        self.h = h
        
    def set_f(self, f):
        self.f = f
        
    def increase_f(self, f):
        self.f = self.f + f

    def reset_visited(self):
        self.visited = False
        
    
class Wall(Cell):
    """
    Celda de tipo muro
    """
    f=10e10
    
    def __init__(self, coordinates):
        super().__init__(coordinates)
        
    def is_valid(self):
        return False
    
    def isVisited(self):
        return self.visited
    
    def __str__(self):
        return f"Wall at ({self.coordinates[0]}, {self.coordinates[1]})"
    
class Street(Cell):
    """
    Celda de tipo calle
    """
    parent = None
    
    def __init__(self, coordinates):
        super().__init__(coordinates)
        
    def is_valid(self):
        return True
    
    def __str__(self):
        return f"Street at ({self.coordinates[0]}, {self.coordinates[1]})"

    def isVisited(self):
        return self.visited
    
    def visit(self):
        self.visited = True

    def set_parent(self, street):
        self.parent = street
    
    def get_parent(self):
        return self.parent
        
    
