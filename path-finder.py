import numpy as np
import tkinter as tk
from PIL import Image
from iterative_algo import IterativeAlgo
from astar_algo import AStarAlgo
from my_pygame import *

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# maze-picture generator https://keesiemeijer.github.io/maze-generator/


def quit_callback():
    close_screen()


root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", quit_callback)
root.title("Path Finder")

root.geometry("400x300")
main_dialog = tk.Frame(root)
main_dialog.pack()
# set_tk_root(main_dialog)

ITERATIVE = 0
A_STAR = 1
delay = 1

method = ITERATIVE
method = A_STAR

# import maze image
img = Image.open("./samples/m1.png")
W = 12
rows = img.height
cols = img.width

# get data in form of 2d array from image
maze = np.array(img)
maze = np.delete(maze, 3, axis=2)
maze = np.round(maze.mean(axis=2)/255)

path_line_color = '#202177'
visited_color = closed_set_color = '#F25D52'
open_set_color = 'lime'


def setup():
    global start, end
    size(cols*W, rows*W)
    title("Maze")
    start = None
    for j in range(cols):
        for i in range(rows):
            if (i == 0 or i == rows-1 or j == 0 or j == cols-1) and maze[i, j]:
                if start is None:
                    start = (i, j)
                else:
                    end = (i, j)
                    break
    # framerate(60)
    # no_loop()
    if method == ITERATIVE:  # normal path-finder with iterative method
        IterativeAlgo.initialize(maze, start, end)
    elif method == A_STAR:  # A* path-finder
        AStarAlgo.initialize(maze, start, end)

    background(255)
    fill('black')
    no_stroke()
    for j in range(cols):
        for i in range(rows):
            if not maze[i, j]:
                square((j*W, i*W), W)


def draw():
    # draw the maze on canvas
    no_stroke()
    fill('blue')
    square((start[1]*W, start[0]*W), W)
    fill('lime')
    square((end[1]*W, end[0]*W), W)

    if method == ITERATIVE:
        path = IterativeAlgo.find_path()
        if IterativeAlgo.finished():
            no_loop()
            print("FINISHED")

        fill(visited_color)
        for v in IterativeAlgo.visited_list:
            square((v[1]*W, v[0]*W), W)

        for v in range(1, len(path)):
            i, j = path[v]
            pi, pj = path[v-1]

            w = (j-pj)*W/2
            h = (i-pi)*W/2

            ci, cj = (i+pi+1)*W/2, (j+pj+1)*W/2
            stroke(path_line_color)
            stroke_weight(W*.4)
            line(cj-w, ci-h, cj+w, ci+h)

    elif method == A_STAR:
        path = AStarAlgo.find_path()
        if AStarAlgo.finished():
            no_loop()
            print("FINISHED")

        fill(open_set_color)
        for o in AStarAlgo.open_set:
            square((o.j*W, o.i*W), W)

        fill(closed_set_color)
        for c in AStarAlgo.closed_set:
            square((c.j*W, c.i*W), W)

        for v in range(1, len(path)):
            i, j = path[v]
            pi, pj = path[v-1]

            w = (j-pj)*W/2
            h = (i-pi)*W/2

            ci, cj = (i+pi+1)*W/2, (j+pj+1)*W/2
            stroke(path_line_color)
            stroke_weight(W*.4)
            line(cj-w, ci-h, cj+w, ci+h)


run(setup=setup, draw=draw)
