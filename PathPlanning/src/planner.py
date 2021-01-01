# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 20:01:54 2020

@author: César
"""
from world import World
import argparse
import time
from matplotlib import pyplot as plt

def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("maze", type=str, help="maze path")
    parser.add_argument("-a", "--algorithm", action='append', help="algorithms you want to test")
    
    args = parser.parse_args()
    
    return args

if __name__ == '__main__':
    print("###########################################################")
    print("Starting path planning algorithm")
    print("-----------------------------------------------------------")
    time.sleep(1)
    
    args = load_args()
       
    algorithms = args.algorithm
    path = args.maze
    
    world = World(path)
    print("-----------------------------------------------------------")
    print("Modelo cargado...")
    time.sleep(1)
    print("-----------------------------------------------------------")
    print("Escoge dos puntos de la imagen con el botón izquierdo del ratón...")
    time.sleep(1)


    plt.figure()
    plt.imshow(world.img)
    start = plt.ginput(1, timeout=-1, show_clicks=True, mouse_pop=2, mouse_stop=3)
    plt.plot(start[0][0], start[0][1], '.r')
    goal = plt.ginput(1, timeout=-1, show_clicks=True, mouse_pop=2, mouse_stop=3)
    plt.plot(goal[0][0], goal[0][1], '.r')
    plt.show()

    s1, s0 = int(start[0][0]), int(start[0][1])
    g1, g0 = int(goal[0][0]), int(goal[0][1])
    print("-----------------------------------------------------------")
    print(f"Inicio = ({s0}, {s1})")
    print(f"Meta = ({g0}, {g1})")
    print("-----------------------------------------------------------")
    time.sleep(1)

    for algorithm in algorithms:
        print("Ejecutando "+algorithm)
        world.set_start(s0, s1)
        world.set_goal(g0, g1)
        start = time.time()
        world.solve(algorithm)
        end = time.time()
        world.resolve()
        print("Finalizando "+algorithm)
        print(f"Tiempo de ejecución = {end-start} s")
        world = World(path)
        print("-----------------------------------------------------------")
    time.sleep(1)
    print("Compruebe la carpeta outputs, se han generado correctamente las soluciones.")
    print("###########################################################")
