from collections import deque
import numpy as np

class Algorithm():
    """
    Clase genérica para los algoritmos.
    """
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        
    def recover(self, grid, goal):
        path = [goal]
        current = goal
        while grid.get_parent(current[0], current[1]) is not None:
            parent = grid.get_parent(current[0], current[1])
            current = parent.get_coordinates()
            path.append((current[0], current[1]))
        return path
    
class ValueIteration(Algorithm):
    """
    Clase del algoritmo Value Iteration
    """
    def execute(self):
        start = self.start
        goal = self.goal
        # primera parte: rellenamos tablero
        self.grid.fill(goal, start)
        self.grid.reset_visit()
        # segunda parte: recorremos desde el comienzo hasta la meta siempre por el camino más corto
        current = start
        lowerVal = 10e8
        lower = None
        
        while(current[0] != goal[0] or current[1] != goal[1]):
            neighbors = self.grid.get_neighbors(current[0], current[1])
            self.grid.visit(current[0],current[1])
            for n in neighbors:
                if n.f < lowerVal:
                    lowerVal = n.f
                    lower = n
            lowerPos = lower.get_coordinates()
            self.grid.set_parent(lowerPos[0], lowerPos[1], self.grid.get_cell(current[0], current[1]))
            current = [lowerPos[0], lowerPos[1]]
            
        return self.grid    

class Bfs(Algorithm):
    """
    Clase para Dijkstra o Breadth First Search
    """
    def execute(self):
        queue = deque()
        start = self.start
        goal = self.goal
        # añadimos comienzo
        queue.append(self.grid.get_cell(start[0], start[1]))
        
        while len(queue):
            to_visit = queue.popleft()
            if not to_visit.isVisited():
                i,j = to_visit.get_coordinates()
                # marcamos como visitado
                self.grid.visit(i,j)
                
                neighbors = self.grid.get_neighbors(i,j)
                neighbors = [n for n in neighbors if n not in queue]
                
                # en cada vecino marcamos el padre como el nodo actual y añadimos a la cola
                for n in neighbors:
                    n_i, n_j = n.get_coordinates()
                    self.grid.set_parent(n_i,n_j, to_visit)
                    queue.append(self.grid.get_cell(n_i,n_j))
                    if n_i == goal[0] and n_j == goal[1]:
                        return self.grid
                    
class Dfs(Algorithm):
    """
    Clase para Depth First Search
    """
    def execute(self):
        queue = deque()
        start = self.start
        goal = self.goal
        # añadimos comienzo
        queue.append(self.grid.get_cell(start[0], start[1]))
        
        while len(queue):
            to_visit = queue.pop()
            if not to_visit.isVisited():
                i,j = to_visit.get_coordinates()
                # marcamos como visitado
                self.grid.visit(i,j)
                
                neighbors = self.grid.get_neighbors(i,j)
                neighbors = [n for n in neighbors if n not in queue]
                
                # en cada vecino marcamos el padre como el nodo actual y añadimos a la cola
                for n in neighbors:
                    n_i, n_j = n.get_coordinates()
                    self.grid.set_parent(n_i,n_j, to_visit)
                    queue.append(self.grid.get_cell(n_i,n_j))
                    if n_i == goal[0] and n_j == goal[1]:
                        return self.grid
                    
class BestFirstSearch(Algorithm):
    """
    Class for Best First Search
    """
    def execute(self):
        queue = deque()
        start = self.start
        goal = self.goal
        # añadimos comienzo
        queue.append(self.grid.get_cell(start[0], start[1]))
        
        while len(queue):
            queue = list(queue)
            queue.sort()
            queue = deque(queue)
            to_visit = queue.popleft()
            if not to_visit.isVisited():
                i,j = to_visit.get_coordinates()
                # marcamos como visitado
                self.grid.visit(i,j)
                
                neighbors = self.grid.get_neighbors(i,j)
                neighbors = [n for n in neighbors if n not in queue]
                
                # en cada vecino marcamos el padre como el nodo actual y añadimos a la cola
                for n in neighbors:
                    n_i, n_j = n.get_coordinates()
                    self.grid.set_parent(n_i,n_j, to_visit)
                    self._set_values(n_i,n_j, start, goal)
                    queue.append(self.grid.get_cell(n_i,n_j))
                    if n_i == goal[0] and n_j == goal[1]:
                        return self.grid
    
    def _set_values(self, i, j, start, goal):
        #g
        g = np.sqrt(np.square(i-start[0])+np.square(j-start[1]))
        self.grid.set_g(i,j,g)
        #h
        h = np.sqrt(np.square(i-goal[0])+np.square(j-goal[1]))
        self.grid.set_h(i,j,h)
        #f
        f = h
        self.grid.set_f(i,j,f)
        
class A_star(BestFirstSearch):
    """
    Clase para A*: simplemente redefiniendo el método set_values.
    """
    def _set_values(self, i, j, start, goal):
        #g
        g = np.sqrt(np.square(i-start[0])+np.square(j-start[1]))
        self.grid.set_g(i,j,g)
        #h
        h = np.sqrt(np.square(i-goal[0])+np.square(j-goal[1]))
        self.grid.set_h(i,j,h)
        #f
        f = g + h
        self.grid.set_f(i,j,f)
        
        
                
    
    
                
        
            
            
                    
        
    