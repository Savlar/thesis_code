import itertools
from typing import Dict, Set

from cycle_notation import CycleNotation
from gap import get_group_info
from graph import Graph
from graphs import find_symmetries_dict
from dfs import dfs


def get_subgraph_containing_vertices(vertices, graph):
    new_graph: Dict[int, Set[int]] = {key: graph[key] for key in graph.keys()}
    remove_key = []
    for key in graph.keys():
        if key not in vertices:
            remove_key.append(key)
        else:
            new_graph[key] = new_graph[key].intersection(vertices)
            if len(new_graph[key]) == 0:
                remove_key.append(key)
    for remove in remove_key:
        del new_graph[remove]
    return new_graph


def create_graph_without_vertices(old_data, vertices):
    data = old_data[:]
    for to_remove in vertices:
        data[to_remove] = set()
        for x in data:
            if to_remove in x:
                x.remove(to_remove)
    return Graph(data)


if __name__ == '__main__':
    asym_graphs = [
        {1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 5}, 4: {2, 6}, 5: {3}, 6: {4}},
        # {1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 5}, 4: {2, 5, 6}, 5: {3, 4}, 6: {4}},
        # {1: {2, 3}, 2: {1, 4}, 3: {1, 4, 5}, 4: {2, 3, 5, 6}, 5: {3, 4}, 6: {4}},
        # {1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4, 5}, 4: {2, 3, 6}, 5: {3}, 6: {4}},
        # {1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4, 5}, 4: {2, 3, 5, 6}, 5: {3, 4}, 6: {4}},
        {1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4, 5}, 4: {2, 3, 5}, 5: {3, 4, 6}, 6: {5}},
        # [{1, 2}, {0, 2, 3}, {0, 1, 3, 4}, {1, 2, 5}, {2, 5}, {3, 4}],
        # [{1, 2}, {0, 2, 3, 4}, {0, 1, 3, 5}, {1, 2, 5}, {1, 5}, {2, 3, 4}],
        # [{1, 2}, {0}, {0, 3, 4}, {2}, {2, 5}, {4, 6}, {5}],
        # [{1}, {0, 2, 3}, {1, 4}, {1, 4, 5}, {2, 3}, {3, 6}, {5}],
        # [{1, 2}, {0, 3}, {0, 3, 4}, {1, 2, 5}, {2, 5, 6}, {3, 4}, {4}],
        # [{1, 2, 5}, {0, 2, 3, 6}, {0, 1, 3}, {1, 2, 4, 5, 6}, {3, 5, 6}, {0, 3, 4, 6}, {1, 3, 4, 5}],
        # [{1, 2, 5}, {0, 2, 3, 6}, {0, 1, 3, 5}, {1, 2, 4, 5, 6}, {3, 5, 6}, {0, 2, 3, 4, 6}, {1, 3, 4, 5}],
        # [{1, 2, 3, 4, 5}, {0, 2, 4, 6}, {0, 1, 3}, {0, 2, 4, 5, 6}, {0, 1, 3, 5, 6}, {0, 3, 4, 6}, {1, 3, 4, 5}],
        # [{1, 4}, {0, 2}, {1, 3, 5}, {2, 4}, {0, 3, 5, 6}, {2, 4, 7}, {4}, {5}],
        # [{1, 2, 5}, {0, 3}, {0, 4}, {1, 4, 6}, {2, 3, 5}, {0, 4, 6, 7}, {3, 5}, {5}],
        # [{1, 3, 4, 5, 6}, {0, 2, 5}, {1, 4, 5, 7}, {0, 4, 6, 7}, {0, 2, 3, 5, 6, 7}, {0, 1, 2, 4, 6}, {0, 3, 4, 5, 7}, {2, 3, 4, 6}],
        {1: {2, 4, 5, 6, 7}, 2: {1, 3, 4, 5, 6}, 3: {2, 6, 8}, 4: {1, 2, 5, 7}, 5: {1, 2, 4, 6, 7, 8},
        6: {1, 2, 3, 5, 7, 8}, 7: {1, 4, 5, 6, 8}, 8: {3, 5, 6, 7}}
    ]
    for asym_graph in asym_graphs:
        subgraphs_vertices = []
        for key in asym_graph.keys():
            dfs(set(), asym_graph, key, subgraphs_vertices)
        subgraphs = []
        for vertices in subgraphs_vertices:
            subgraphs.append(Graph(get_subgraph_containing_vertices(vertices, asym_graph)))
        for graph in subgraphs:
            for sym in find_symmetries_dict([], set(graph.data.keys()), {i: set() for i in graph.data.keys()}, graph,
                                            {key: count for count, key in enumerate(graph.data.keys())}):
                cyc = CycleNotation(sym)
                graph.aut_group.add(cyc)
        with open('input.g', 'w') as file:
            file.write('PrintTo("output_test.txt", "");')
        input_ = ''
        # t = set.union(*(g.aut_group for g in subgraphs))
        # test_g = Graph(None)
        # test_g.aut_group = t
        # get_group_info(test_g.get_gap_repr())
        # break
        for n in subgraphs:
            input_ += n.get_gap_repr()
        get_group_info(input_)
        with open('output_test.txt', 'r') as file:
            groups_descriptions = file.read().split('\n')[:-1]
            for i, n in enumerate(subgraphs):
                n.group_type = groups_descriptions[i]
                print(n, n.aut_group, n.group_desc())
        break

# Graph( G, [1..3], OnPoints, function(x,y) return A[x][y]=1; end,  true );
# A := [[0,1,1,0,0,0], [1,0,1,1,0,0], [1,1,0,1,1,0], [0,1,1,0,1,0], [0,0,1,1,0,1], [0,0,0,0,1,0]];
