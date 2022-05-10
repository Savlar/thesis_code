import itertools

from typing import List, Set

g = [{3, 4}, {4}, {3}, {0, 2}, {0, 1}]
# g = [{3}, {3, 4}, {4}, {0, 1}, {1, 2}]
# g = [{3}, {4}, {3}, {0, 2}, {1}]
m = 3
n = 2

g = [{*range(m, m + n)} for _ in range(m)] + [{*range(m)} for _ in range(n)]


def find_symmetries(visited: List[int], not_visited: Set[int], graph: List[Set[int]], all_symmetries, g):
    if len(not_visited) == 0:
        if graph == g and sum(visited[:m]) == sum(range(m)):
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
            try:
                graph[visited[v]].remove(vertex)
            except KeyError:
                pass
        graph[vertex] = set()
        visited.pop()
        not_visited.add(vertex)


a = []
find_symmetries([], set(range(len(g))), [set()] * len(g), a, g)
print(len(a))
print('\n'.join(str(x) for x in a))
