def dfs(visited, graph, vertex, subgraphs):
    if 1 < len(visited) != len(graph.keys()) and visited not in subgraphs:
        subgraphs.append(set(visited))
    if vertex not in visited:
        for neighbour in graph[vertex]:
            visited.add(vertex)
            dfs(visited, graph, neighbour, subgraphs)
            visited.remove(vertex)


if __name__ == '__main__':
    subgraphs = []
    g = {0: {1, 2}, 1: {0, 3}, 2: {0, 4}, 3: {1, 5}, 4: {2}, 5: {3}}
    # g = {0: {1, 2}, 1: {0, 2, 3}, 2: {0, 1, 3}, 3: {1, 2}}
    g = {0: {1, 3, 4, 5, 6}, 1: {0, 2, 3, 4, 5}, 2: {1, 5, 7}, 3: {0, 1, 4, 6}, 4: {0, 1, 3, 5, 6, 7},
         5: {0, 1, 2, 4, 6, 7}, 6: {0, 3, 4, 5, 7}, 7: {2, 4, 5, 6}}
    for key in g.keys():
        dfs(set(), g, key, subgraphs)
        # break
    print(*subgraphs, sep='\n')
