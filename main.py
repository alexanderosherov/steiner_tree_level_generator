import itertools
from random import randint

from steiner_tree import SteinerTree


# points = ((0, 2), (1, 6), (2, 0), (3, 2), (3, 5), (5, 3), (5, 6), (7, 2))
# points = ((2, 3), (1, 9), (3, 5), (4, 1), (5, 4), (6, 5), (7, 9), (10, 2), (10, 8))


import random

def get_points_scattered(grid, n):
    points = set()
    grid_copy = grid.copy()
    for _ in range(n):
        if not grid_copy: break
        p = random.choice(grid_copy)
        points.add(p)
        points_x = {x for (x, y) in points}
        points_y = {y for (x, y) in points}
        grid_copy = [(x, y) for (x, y) in grid_copy if x not in points_x and y not in points_y]
    return points

def get_points_random(grid, n):
    return set(random.sample(grid, n))

def get_points_clustered(grid, n, max_coord):
    num_centers = random.randint(2, 3)
    centers = random.sample(grid, num_centers)
    points = set(centers)
    while len(points) < n:
        c = random.choice(centers)
        dx = random.randint(-2, 2)
        dy = random.randint(-2, 2)
        p = (c[0]+dx, c[1]+dy)
        if 0 <= p[0] < max_coord and 0 <= p[1] < max_coord:
            points.add(p)
    return points

def get_points_symmetric(grid, n, max_coord):
    center_x = (max_coord - 1) / 2
    center_y = (max_coord - 1) / 2
    points = set()
    while len(points) < n:
        p = random.choice(grid)
        points.add(p)
        mx = int(center_x + (center_x - p[0]))
        my = int(center_y + (center_y - p[1]))
        if 0 <= mx < max_coord and 0 <= my < max_coord:
            points.add((mx, my))
            if len(points) >= n: break
    return set(list(points)[:n])


def run(field_size):
    print("START")
    terminals = ((2, 3), (1, 9), (3, 5), (4, 1), (5, 4), (6, 5), (7, 9), (10, 2), (10, 8))
    steiner_tree = SteinerTree(terminals)
    steiner_tree.start()
    complexity = steiner_tree.complexity()
    ideal_complexity = complexity[2]
    print("IDEAL:", ideal_complexity)

    data = []
    size = field_size
    grid = list(itertools.product(range(max(size)), repeat=2))

    for _ in range(50):
        n_terminals = randint(8, 10)
        generator_choice = randint(2, 4)
        if generator_choice == 1:
            terminals = tuple(get_points_scattered(grid.copy(), n_terminals))
        elif generator_choice == 2:
            terminals = tuple(get_points_random(grid.copy(), n_terminals))
        elif generator_choice == 3:
            terminals = tuple(get_points_clustered(grid.copy(), n_terminals, max(size)))
        else:
            terminals = tuple(get_points_symmetric(grid.copy(), n_terminals, max(size)))
            
        steiner_tree = SteinerTree(terminals)
        steiner_tree.start()
        complexity = steiner_tree.complexity()
        steiner_ratio = complexity[4]
        
        if complexity[2] < ideal_complexity * 4 and steiner_ratio < 0.95:
            solution = steiner_tree.manhattan_solution(show=True)

            print("Type of points:", generator_choice)
            print(f"COMPLEXITY: {complexity[:4]} RATIO: {steiner_ratio:.3f}")
            print("POINTS:")
            print([[x, y] for (x, y) in terminals])
            print("SOLUTION:")
            print(solution)
            data.append([[[x, y] for (x, y) in terminals], int(complexity[0]), solution, size[0], complexity[2]])
        print("_______________________________________________________")

    with open("tree.dart", "w") as f:
        data.sort(key=lambda x: x[4], reverse=True)
        f.write("List trees = "+str(data)+";")
    print("DONE")
