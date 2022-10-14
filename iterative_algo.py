import numpy as np


class IterativeAlgo:
    @staticmethod
    def initialize(m, s, e):
        global maze, path, rows, cols, visited, start, end, current, path_lines, last_len, rects
        maze = m
        rows, cols = maze.shape
        visited = np.zeros(maze.shape)
        start = s
        end = e
        current = start
        last_len = 0

        path = []
        path_lines = []
        IterativeAlgo.visited_list = []
        rects = []

    @staticmethod
    def finished():
        return path[-1] == end

    @staticmethod
    def find_path():
        global path, visited, start, end, current, visited_list
        # path = []
        if current == end:
            path.append(current)
            return path
        # mark current cell as visited
        visited[current[0], current[1]] = 1
        IterativeAlgo.visited_list.append(current)
        # print(visited_list)
        i, j = current

        # add all neighbours if available
        neighbours = []
        if (IterativeAlgo.is_available(i, j+1)):  # bottom
            neighbours.append((i, j+1))
        if (IterativeAlgo.is_available(i, j-1)):  # top
            neighbours.append((i, j-1))
        if (IterativeAlgo.is_available(i+1, j)):  # right
            neighbours.append((i+1, j))
        if (IterativeAlgo.is_available(i-1, j)):  # left
            neighbours.append((i-1, j))

        if (len(neighbours) > 0):  # there are any neighbors
            # add current location to path
            path.append(current)

            # make the first neighbour current cell
            current = neighbours[0]
        else:  # no neighbor available
            # pop the last cell from the path and make it current cell
            current = path.pop()

            if (current == start):  # the current cell is start
                print("path is not available")
        return path

    @staticmethod
    def is_available(i, j):
        return i >= 0 and i < rows and j >= 0 and j < cols and maze[i, j] == 1 and not visited[i, j]
