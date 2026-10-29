from collections import Counter
from random import randint

import itertools
import time
import matplotlib.pyplot as plt


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class SteinerTree:

    def __init__(self, terminals: tuple):
        self.terminals = terminals
        self.statistic = {}
        self.solution_graph = ()
        self.all_cases_n = 1

    def start(self):
        import math
        t = time.time()
        n = len(self.terminals)
        points_x = {p[0] for p in self.terminals}
        points_y = {p[1] for p in self.terminals}
        V = list(itertools.product(points_x, points_y))

        INF = float('inf')
        S = [[INF] * len(V) for _ in range(1 << n)]

        for i, terminal in enumerate(self.terminals):
            mask = 1 << i
            for v_idx, v in enumerate(V):
                S[mask][v_idx] = manhattan(terminal, v)

        for size in range(2, n + 1):
            for mask in range(1, 1 << n):
                if mask.bit_count() != size:
                    continue

                submasks = []
                submask = (mask - 1) & mask
                lowest_bit = mask & -mask
                while submask > 0:
                    if submask & lowest_bit:
                        submasks.append(submask)
                    submask = (submask - 1) & mask

                P = [INF] * len(V)
                for v_idx in range(len(V)):
                    min_p = INF
                    for Y in submasks:
                        val = S[Y][v_idx] + S[mask ^ Y][v_idx]
                        if val < min_p:
                            min_p = val
                    P[v_idx] = min_p

                for v_idx in range(len(V)):
                    min_s = INF
                    for q_idx in range(len(V)):
                        val = P[q_idx] + manhattan(V[v_idx], V[q_idx])
                        if val < min_s:
                            min_s = val
                    S[mask][v_idx] = min_s

        full_mask = (1 << n) - 1
        best_weight = min(S[full_mask])

        solution_edges = set()

        def backtrack(mask, v_idx):
            if mask.bit_count() == 1:
                t_idx = mask.bit_length() - 1
                terminal = self.terminals[t_idx]
                if terminal != V[v_idx]:
                    solution_edges.add(tuple(sorted((terminal, V[v_idx]))))
                return

            submasks = []
            submask = (mask - 1) & mask
            lowest_bit = mask & -mask
            while submask > 0:
                if submask & lowest_bit:
                    submasks.append(submask)
                submask = (submask - 1) & mask

            for q_idx in range(len(V)):
                for Y in submasks:
                    if S[Y][q_idx] + S[mask ^ Y][q_idx] + manhattan(V[v_idx], V[q_idx]) == S[mask][v_idx]:
                        if V[v_idx] != V[q_idx]:
                            solution_edges.add(tuple(sorted((V[v_idx], V[q_idx]))))
                        backtrack(Y, q_idx)
                        backtrack(mask ^ Y, q_idx)
                        return

        best_v_idx = -1
        for v_idx in range(len(V)):
            if S[full_mask][v_idx] == best_weight:
                best_v_idx = v_idx
                break

        backtrack(full_mask, best_v_idx)
        self.solution_graph = tuple(solution_edges)

        memo = {}

        def count_paths(mask, v_idx):
            if mask.bit_count() == 1:
                return 1
            if (mask, v_idx) in memo:
                return memo[(mask, v_idx)]

            submasks = []
            submask = (mask - 1) & mask
            lowest_bit = mask & -mask
            while submask > 0:
                if submask & lowest_bit:
                    submasks.append(submask)
                submask = (submask - 1) & mask

            total = 0
            for q_idx in range(len(V)):
                for Y in submasks:
                    if S[Y][q_idx] + S[mask ^ Y][q_idx] + manhattan(V[v_idx], V[q_idx]) == S[mask][v_idx]:
                        total += count_paths(Y, q_idx) * count_paths(mask ^ Y, q_idx)
            memo[(mask, v_idx)] = total
            return total

        best_cases_n = 0
        for v_idx in range(len(V)):
            if S[full_mask][v_idx] == best_weight:
                best_cases_n += count_paths(full_mask, v_idx)

        self.statistic = {best_weight: best_cases_n}

        grid_none_points = [p for p in V if p not in self.terminals]
        self.all_cases_n = sum(math.comb(len(grid_none_points), k) for k in range(6))

        print(time.time() - t, "s")

    def calculate_mst_weight(self):
        if not self.terminals:
            return 0
        n = len(self.terminals)
        visited = [False] * n
        min_edge = [float('inf')] * n
        min_edge[0] = 0
        total_weight = 0
        
        for _ in range(n):
            u = -1
            best = float('inf')
            for i in range(n):
                if not visited[i] and min_edge[i] < best:
                    u = i
                    best = min_edge[i]
            
            visited[u] = True
            total_weight += best
            
            for v in range(n):
                if not visited[v]:
                    d = manhattan(self.terminals[u], self.terminals[v])
                    if d < min_edge[v]:
                        min_edge[v] = d
                        
        return total_weight

    def complexity(self):
        best_case = list(self.statistic.keys())[0]
        best_cases_n = self.statistic[best_case]
        all_cases_n = self.all_cases_n
        
        # Guard against zero division if there are too few points
        ratio = best_cases_n / all_cases_n * 1000000 if all_cases_n > 0 else 0
        
        mst_weight = self.calculate_mst_weight()
        steiner_ratio = best_case / mst_weight if mst_weight > 0 else 1.0
        
        return best_case, best_cases_n, ratio, self.statistic, steiner_ratio

    def manhattan_solution(self, show=False):
        edges = list(self.solution_graph)
        manhattan_edges = []
        for e in self.solution_graph:
            if e[0][0] == e[1][0] or e[0][1] == e[1][1]:
                manhattan_edges += self.line_to_one_lines(e)
                edges.remove(e)

        for e in edges:
            help_p = (e[1][0], e[0][1])
            if randint(0, 1) == 0:
                help_p = (e[0][0], e[1][1])
            if show:
                plt.scatter(help_p[0], help_p[1], c="grey")
            manhattan_edges += self.line_to_one_lines((e[0], help_p))
            manhattan_edges += self.line_to_one_lines((help_p, e[1]))

        if show:
            plt.scatter([x for (x, y) in self.terminals], [y for (x, y) in self.terminals])
            for e in self.solution_graph:
                plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], c="r")
            for e in manhattan_edges:
                plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], c="grey", lw=0.5)
            plt.show()

        return manhattan_edges

    # split horizontal or vertical line to lines with length 1
    @staticmethod
    def line_to_one_lines(edge):
        x1 = edge[0][0]
        x2 = edge[1][0]
        y1 = edge[0][1]
        y2 = edge[1][1]
        if x1 == x2:
            return [[[x1, min(y1, y2) + dy - 1], [x1, min(y1, y2) + dy]] for dy in range(1, abs(y1 - y2) + 1)]
        else:
            return [[[min(x1, x2) + dx - 1, y1], [min(x1, x2) + dx, y1]] for dx in range(1, abs(x1 - x2) + 1)]
