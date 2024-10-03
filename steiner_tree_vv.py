from random import randint

import networkx as nx
import itertools
import time
import matplotlib.pyplot as plt

from v_algorithm import repetitive_shortest_path


class SteinerTreeVV:

    def __init__(self, terminals: tuple):
        # init terminals
        self.terminals = terminals
        points_x = [x for (x, y) in terminals]
        points_y = [y for (x, y) in terminals]

        # init grid
        grid = list(itertools.combinations(range(max(max(points_x), max(points_y))+1), 2))
        grid += [(y, x) for (x, y) in grid]
        grid += [(x, x) for x in range(max(max(points_x), max(points_y))+1)]

        # init grid where could be steiner points
        span_grid = grid#[(x, y) for (x, y) in grid if ((x in points_x) and (y in points_y))]

        # init graph with terminals
        self.graph = nx.Graph()
        self.graph.add_nodes_from(span_grid)


        for p1 in span_grid:
            for p2 in span_grid:
                if (abs(p1[0]-p2[0])==1 and abs(p1[1]-p2[1])==0) or (abs(p1[0]-p2[0])==0 and abs(p1[1]-p2[1])==1):
                    self.graph.add_edge(p1, p2, weight=1)

        self.solution_graph = None
        self.time = None

    def repetitive_shortest_path(self):
        graph, terminals = self.graph, self.terminals
        # compute the shortest paths from terminals to all nodes

        return repetitive_shortest_path(graph, terminals)

    def start(self):

        t = time.time()

        self.solution_graph = self.repetitive_shortest_path()[0]

        self.time = time.time() - t

    def show_solution(self, title = None):
        edges = self.solution_graph.edges
        manhattan_edges = []

        for e in edges:
            help_p = (e[1][0], e[0][1])
            if randint(0, 1) == 0:
                help_p = (e[0][0], e[1][1])
            plt.scatter(help_p[0], help_p[1], c="black")

        plt.scatter([x for (x, y) in self.terminals], [y for (x, y) in self.terminals], c="r")
        for e in edges:
            plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], c="black", lw=0.5)

        if title is not None:
            plt.title(title)

        plt.show()

        return manhattan_edges
