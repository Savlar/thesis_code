import itertools
import time
from typing import Set, List
from collections import OrderedDict
# https://math.stackexchange.com/a/2678754
# petersen = [{1, 2, 3, 4, 5}, {0}, {0}, {0}, {0}, {0}]
# petersen = [{1, 2, 3, 4}, {0}, {0}, {0}, {0, 5}, {4}]
# petersen = [{1, 2, 3}, {0}, {0}, {0, 4}, {3, 5}, {4}]
# petersen = [{1, 2, 3}, {0}, {0}, {0, 4, 5}, {3}, {3}]
from graph import Graph
from partial_sym_test import partial_perm_graph
from psym import PartialPerm


# from psym import PartialPerm


def find_symmetries(visited: List[int], not_visited: Set[int], graph: List[Set[int]], g):
    if len(not_visited) == 0:
        if Graph(graph) == g:
            yield list(visited)
    curr_vertex = len(g) - len(not_visited)
    for vertex in list(not_visited):
        not_visited.remove(vertex)
        visited.append(vertex)
        neighbours = g[curr_vertex].intersection(set(range(curr_vertex)))
        graph[vertex] = {visited[v] for v in neighbours}
        for v in neighbours:
            graph[visited[v]].add(vertex)
        if graph[curr_vertex] - g[curr_vertex] == set():
            yield from find_symmetries(visited, not_visited, graph, g)
        for v in neighbours:
            graph[visited[v]].remove(vertex)
        graph[vertex] = set()
        visited.pop()
        not_visited.add(vertex)


def find_symmetries_dict(visited: List[int], not_visited: Set[int], graph, g, mapping):
    if len(not_visited) == 0:
        if Graph(graph) == g:
            yield list(visited)
    index = len(g) - len(not_visited)
    for vertex in list(not_visited):
        not_visited.remove(vertex)
        visited.append(vertex)
        curr_vertex = sorted(g.data.keys())[index]
        neighbours = g[curr_vertex].intersection(set(key for key in g.data.keys() if key < curr_vertex))
        graph[vertex] = {visited[mapping[v]] for v in neighbours}
        for v in neighbours:
            graph[visited[mapping[v]]].add(vertex)
        if graph[curr_vertex] - g[curr_vertex] == set():
            yield from find_symmetries_dict(visited, not_visited, graph, g, mapping)
        for v in neighbours:
            graph[visited[mapping[v]]].remove(vertex)
        graph[vertex] = set()
        visited.pop()
        not_visited.add(vertex)
# g = [{1, 2, 3}, {0, 2, 3}, {0, 1, 3}, {0, 1, 2}]
# g = [{1, 3}, {0, 2, 3}, {1, 3}, {0, 1, 2}]
# a = []
# print(x * y)

# g = Graph(data=[{1, 2}, {0, 2, 3}, {0, 1, 3}, {1, 2}])
# g = Graph(data={1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4}, 4: {2, 3}})
# g = Graph(data={1: {2}, 2: {1, 3}, 3: {2}, 4: set()})
g = Graph({1: {2, 3}, 2: {1, 4, 5}, 3: {1}, 4: {2}, 5: {2}})
# g = Graph({1: {2, 3, 4, 5}, 2: {1}, 3: {1}, 4: {1}, 5: {1}})
# start = time.time()
# g_size = len(g.data.keys())
# orig = {*range(1, len(g.data.keys()) + 1)}
# for perm in [PartialPerm(*x) for x in itertools.product(itertools.combinations(orig, g_size), itertools.permutations(orig, g_size))]:
#     new_graph = partial_perm_graph(perm, g)
#     if new_graph == g:
#         print(perm)
# for sym in find_symmetries_dict([], set(g.data.keys()), {i: set() for i in g.data.keys()}, g,
#                                             {key: count for count, key in enumerate(g.data.keys())}):
#     print(sym)
# g = Graph(data={'a': {'c'}, 'c': {'a', 'd'}, 'd': {'c'}})
# g = Graph(data={10: {3}, 3: {10, 4}, 4: {3}})
# for sym in find_symmetries([], set(range(len(g))), [set() for _ in range(len(g))], g):
# for sym in find_symmetries_dict([], set(g.data.keys()), {i: set() for i in g.data.keys()}, g, {1: 0, 2: 1, 3: 2, 4: 3}):
# for sym in find_symmetries_dict([], set(g.data.keys()), {i: set() for i in g.data.keys()}, g, {1: 0, 2: 1, 3: 2, 4: 3}):
# for sym in find_symmetries_dict([], set(g.data.keys()), {i: set() for i in g.data.keys()}, g, {'a': 0, 'c': 1, 'd': 2}):
# for sym in find_symmetries_dict([], set(g.data.keys()), {i: set() for i in g.data.keys()}, g, {key: count for count, key in enumerate(g.data.keys())}):
#     print(sym)
# print(time.time() - start)
