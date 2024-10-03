import itertools
from random import randint

from steiner_tree import SteinerTree
from steiner_tree_vv import SteinerTreeVV
import numpy as np

# points = ((0, 2), (1, 6), (2, 0), (3, 2), (3, 5), (5, 3), (5, 6), (7, 2))
# points = ((2, 3), (1, 9), (3, 5), (4, 1), (5, 4), (6, 5), (7, 9), (10, 2), (10, 8))


def get_points(grid, n):
    points = set()

    for i in range(n):
        points.add(grid[randint(0, len(grid) - 1)])
        grid = [(x, y) for (x, y) in grid if
                ((x not in [x for (x, y) in points]) and (y not in [y for (x, y) in points]))]
        if len(grid) == 0:
            break
    # plt.scatter([x for (x, y) in points], [y for (x, y) in points])
    # plt.show()

    return points


def get_random_points(field_size):
    grid = list(itertools.combinations(range(max(field_size)), 2))
    grid += [(y, x) for (x, y) in grid]
    grid += [(x, x) for x in range(max(field_size))]
    return tuple(get_points(grid.copy(), randint(8, 10)))

def run(field_size, generations_number):
    print("START")


    for n in range(generations_number):
        terminals = get_random_points(field_size)

        steiner_tree = SteinerTree(terminals)
        steiner_tree.start()
        complexity = steiner_tree.complexity()[0]
        time = steiner_tree.time
        steiner_tree.manhattan_solution(title = f'A-Version, Iteration: {n}')


        steiner_tree_vv = SteinerTreeVV(terminals)
        steiner_tree_vv.start()
        solution_vv = steiner_tree_vv.solution_graph.edges
        complexity_vv = len(solution_vv)
        time_vv = steiner_tree_vv.time
        steiner_tree_vv.show_solution(title = f'V-Version, Iteration: {n}')


        print('A:', complexity, 'V:', complexity_vv)
        print('Complexity winner:', ['A', 'V'][np.argmin([complexity, complexity_vv])])
        print('Time winner:', ['A', 'V'][np.argmin([time, time_vv])])

        print("_______________________________________________________")


    print("DONE")

if __name__ == "__main__":
    run(field_size = (5, 5), generations_number = 2)


