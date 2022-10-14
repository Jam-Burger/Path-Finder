import numpy as np


def heuristic(a, b):
    # return np.sqrt((a.i-b.i)**2 + (a.j-b.j)**2)
    return abs(a.i-b.i) + abs(a.j-b.j)

 # making a class spot which has f-score, g-score and h-score


class Spot:
    # f-Score represents our current best guess as to how cheap a path could be from start to finish if it goes through n.
    # g-score is the cost of the cheapest path from start to n currently known.
    f = g = h = 0

    # 'previous' is the node immediately preceding it on the cheapest path from start
    previous = None

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.neighbours = []

    def add_neighbours(self, grid):  # adding neighbours
        i, j = self.i, self.j
        if (Spot.is_available(i, j+1)):  # bottom
            self.neighbours.append(grid[i, j+1])
        if (Spot.is_available(i, j-1)):  # top
            self.neighbours.append(grid[i, j-1])
        if (Spot.is_available(i+1, j)):  # right
            self.neighbours.append(grid[i+1, j])
        if (Spot.is_available(i-1, j)):  # left
            self.neighbours.append(grid[i-1, j])

    @staticmethod
    def is_available(i, j):
        return i >= 0 and i < rows and j >= 0 and j < cols and maze[i, j] == 1


class AStarAlgo:
    @staticmethod
    def initialize(m, s, e):
        global maze, rows, cols, start, end, path_lines, grid
        maze = m
        path_lines = []
        rows, cols = maze.shape

        # initializing openset and closedset
        grid = np.full(maze.shape, None)

        # initializing grid of spots
        for i in range(rows):
            for j in range(cols):
                grid[i, j] = Spot(i, j)

        for i in range(rows):
            for j in range(cols):
                grid[i, j].add_neighbours(grid)

        start = grid[s[0], s[1]]
        end = grid[e[0], e[1]]

        AStarAlgo.open_set = [start]
        AStarAlgo.closed_set = []

    @staticmethod
    def find_path():
        global path, start, end, current, grid
        winner = 0
        for i in range(len(AStarAlgo.open_set)):
            if AStarAlgo.open_set[i].f < AStarAlgo.open_set[winner].f:
                winner = i

        current = AStarAlgo.open_set[winner]
        if current == end:
            path = []
            temp = current
            path.append((temp.i, temp.j))
            while temp.previous:
                path.insert(0, (temp.previous.i, temp.previous.j))
                temp = temp.previous
            return path

        AStarAlgo.open_set.remove(current)
        AStarAlgo.closed_set.append(current)

        neighbours = current.neighbours

        for neighbour in neighbours:
            if neighbour in AStarAlgo.closed_set:
                continue

            # temp_g is the distance from start to the neighbor through current
            temp_g = current.g + 1
            if neighbour in AStarAlgo.open_set:
                if temp_g < neighbour.g:
                    neighbour.g = temp_g
            else:
                neighbour.g = temp_g
                AStarAlgo.open_set.append(neighbour)

            neighbour.previous = current
            neighbour.h = heuristic(neighbour, end)
            neighbour.f = neighbour.g+neighbour.h

        path = []
        temp = current
        path.append((temp.i, temp.j))
        while temp.previous:
            path.insert(0, (temp.previous.i, temp.previous.j))
            temp = temp.previous
        # print(len(path))
        return path

    @staticmethod
    def finished():
        return len(AStarAlgo.open_set) == 0 or current == end
