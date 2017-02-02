import time


class Node:

    def __init__(self, value, cords):
        self.value = value
        self.parent = None
        self.cords = cords
        self.g = 0
        self.h = 0


def children(node, map):
    x, y = node.cords
    adjacent = [map[offset[0]][offset[1]] for offset in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]]
    return [neighbor for neighbor in adjacent if neighbor.value != '1']


def heuristic(from_node, to_node):
    return abs(from_node.cords[0] - to_node.cords[0]) + abs(from_node.cords[1] - to_node.cords[1])


def a_star(start, goal, grid):
    open_set = set()
    closed_set = set()
    current = start
    open_set.add(current)
    while open_set:
        current = min(open_set, key=lambda o: o.g + o.h)
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        open_set.remove(current)
        closed_set.add(current)
        for node in children(current, grid):
            if node in closed_set:
                continue
            if node in open_set:
                new_g = current.g + 1
                if node.g > new_g:
                    node.g = new_g
                    node.parent = current
            else:
                node.g = current.g + 1
                node.h = heuristic(node, goal)
                node.parent = current
                open_set.add(node)
    raise ValueError('No path found')


def find_path(start, goal, grid):
    for x in xrange(len(grid)):
        for y in xrange(len(grid[x])):
            grid[x][y] = Node(grid[x][y], (x, y))
    x_s, y_s = start
    x_g, y_g = goal

    start_time = time.time()
    path = a_star(grid[x_s][y_s], grid[x_g][y_g], grid)
    print('Time of running a* search: %.5f' % (time.time() - start_time))

    print len(path) - 1

    for node in path:
        x, y = node.cords
        if grid[x][y].value == 'S' or grid[x][y].value == 'T':
            continue
        grid[x][y].value = '.'

    with open('maze_solved.txt', 'w') as os:
        for x in xrange(len(grid)):
            for y in xrange(len(grid[x])):
                if grid[x][y].value == '1':
                    grid[x][y].value = 'X'
                if grid[x][y].value == '0':
                    grid[x][y].value = ' '
                os.write(grid[x][y].value)
            os.write('\n')


def main():
    grid = []
    with open('maze.txt', 'r') as f:
        for line in f:
            grid.append(list(line.strip()))

    start_cords = (-1, -1)
    end_cords = (-1, -1)

    for x in xrange(len(grid)):
        for y in xrange(len(grid[x])):
            if grid[x][y] == 'S':
                start_cords = (x, y)
            if grid[x][y] == 'F':
                end_cords = (x, y)

    find_path(start_cords, end_cords, grid)


if __name__ == "__main__":
    main()
    input()
