from typing import Set, List

# https://math.stackexchange.com/a/2678754
# petersen = [{1, 2, 3, 4, 5}, {0}, {0}, {0}, {0}, {0}]
# petersen = [{1, 2, 3, 4}, {0}, {0}, {0}, {0, 5}, {4}]
# petersen = [{1, 2, 3}, {0}, {0}, {0, 4}, {3, 5}, {4}]
# petersen = [{1, 2, 3}, {0}, {0}, {0, 4, 5}, {3}, {3}]
from graph import Graph


def find_symmetries(visited: List[int], not_visited: Set[int], graph: List[Set[int]], all_symmetries, g):
    if len(not_visited) == 0:
        if Graph(graph) == g:
            all_symmetries.append(list(visited))
    curr_vertex = len(g) - len(not_visited)
    for vertex in list(not_visited):
        not_visited.remove(vertex)
        visited.append(vertex)
        neighbours = g[curr_vertex].intersection(set(range(curr_vertex)))
        graph[vertex] = {visited[v] for v in neighbours}
        for v in neighbours:
            graph[visited[v]].add(vertex)
        if graph[curr_vertex] - g[curr_vertex] == set():
            find_symmetries(visited, not_visited, graph, all_symmetries, g)
        for v in neighbours:
            graph[visited[v]].remove(vertex)
        graph[vertex] = set()
        visited.pop()
        not_visited.add(vertex)

# g = [{1, 2, 3}, {0, 2, 3}, {0, 1, 3}, {0, 1, 2}]
# g = [{1, 3}, {0, 2, 3}, {1, 3}, {0, 1, 2}]
# a = []
# x = CycleNotation([2, 6, 0, 4, 5, 3, 1, 7])
# y = CycleNotation([1, 2, 6, 7, 4, 3, 0, 5])
# print(x * y)
