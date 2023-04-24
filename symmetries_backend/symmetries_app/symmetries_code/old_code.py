from typing import List, Set


def find_symmetries_dict(visited: List[int], not_visited: Set[int], graph, g, mapping):
    """
    unused function to find the symmetries of a graph, represented using a dictionary, replaced with much faster networkx function
    """
    if len(not_visited) == 0:
        if graph == g.data:
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


def find_symmetries(visited: List[int], not_visited: Set[int], graph: List[Set[int]], g, all_symmetries):
    """
    unused function to find symmetries of a graphs represented using a list, i-th index are the neighbours of vertex 'i'
    """
    if len(not_visited) == 0:
        if graph == g:
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
            find_symmetries(visited, not_visited, graph, g, all_symmetries)
        for v in neighbours:
            graph[visited[v]].remove(vertex)
        graph[vertex] = set()
        visited.pop()
        not_visited.add(vertex)


def dfs(visited, graph, vertex, subgraphs):
    if 1 < len(visited) != len(graph.keys()) and visited not in subgraphs:
        subgraphs.append(set(visited))
    if vertex not in visited:
        for neighbour in graph[vertex]:
            visited.add(vertex)
            dfs(visited, graph, neighbour, subgraphs)
            visited.remove(vertex)
