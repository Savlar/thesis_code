import time

import random

from symmetries_app.symmetries_code.gap import get_non_isomorphic_trees
from symmetries_app.symmetries_code.graph import Graph


# functions that generate certain types of graphs, only creates the graph, does not calculate symmetries


def generate_petersen():
    return Graph({1: {3, 4, 6}, 2: {4, 5, 7}, 3: {1, 5, 8}, 4: {1, 2, 9}, 5: {2, 3, 10},
                  6: {1, 7, 10}, 7: {2, 6, 8}, 8: {3, 7, 9}, 9: {4, 8, 10}, 10: {5, 6, 9}}, aut_group=set())


def generate_complete_graph(size):
    data = dict()
    for key in range(1, size + 1):
        data[key] = set(i for i in range(1, size + 1) if i != key)
    return Graph(data, aut_group=set())


def generate_non_isomorphic_trees(nodes):
    return get_non_isomorphic_trees(nodes)


def generate_star(nodes):
    data = {i: {nodes} if i != nodes else set(range(1, nodes)) for i in range(1, nodes + 1)}
    return Graph(data, aut_group=set())


def generate_random_graph(v, density=None):
    data = {key: set() for key in range(1, v + 1)}
    edges = random.randint(v, ((v * (v - 1)) // 2) - v) if density is None else density * ((v * (v - 1)) // 2)
    while sum(len(data[key]) for key in data.keys()) // 2 < edges:
        start = random.randrange(1, v + 1)
        end = random.randrange(1, v + 1)
        if start != end:
            data[start].add(end)
            data[end].add(start)
    return Graph(data, aut_group=set())


if __name__ == '__main__':
    g = generate_random_graph(500, 0.7)
    h = generate_random_graph(500, 0.6)
    start = time.time()
    iso = g.is_isomorphic(h)
    print(time.time() - start)
    start = time.time()
    tr = g.triangle_sequence()
    print(time.time() - start)