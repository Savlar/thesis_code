import itertools
import time

from graph import Graph
from psym import PartialPerm


def is_group(partial_perms):
    for item in partial_perms:
        if not item.is_cycle():
            return False
    return True


def get_box(partial_permutations):
    if len(partial_permutations) == 1 and str(partial_permutations[0]) == 'id':
        return [set()]
    cycles = []
    for item in partial_permutations:
        if item.is_cycle():
            cycles.append(item)
        else:
            break
    row = dict()
    col = dict()
    index = 0
    cycles = sorted(cycles)
    for cycle in cycles:
        domain = tuple(sorted(cycle.dom))
        ran = tuple(sorted(cycle.ran))
        if domain not in col.keys() and ran not in row.keys():
            row[ran] = index
            col[domain] = index
            index += 1
    size = len(row.keys())
    result = [[[] for _ in range(size)] for _ in range(size)]
    for item in partial_permutations:
        i = row[tuple(sorted(item.ran))]
        j = col[tuple(sorted(item.dom))]
        result[i][j].append(item)
    return result


def create_subgraph(new_vertex_set, old_graph):
    new_data = dict()
    for key in old_graph.data.keys():
        if key in new_vertex_set:
            new_data[key] = set()
            for neighbour in old_graph.data[key]:
                if neighbour in new_vertex_set:
                    new_data[key].add(neighbour)
    return Graph(new_data)


def create_new_graph_permuted(dom, ran, old):
    new = dict()
    for i in range(len(ran)):
        new[ran[i]] = [item for item in old.data[dom[i]]]
    for key in new.keys():
        for i in range(len(new[key])):
            index_of = dom.index(new[key][i])
            new[key][i] = ran[index_of]
        new[key] = set(new[key])
    new = {key: new[key] for key in sorted(new.keys())}
    return Graph(new)


def partial_perm_graph(perm, g):
    ng = [[key, list(g.data[key].intersection(perm.ran))] for key in g.data.keys() if key in perm.ran]
    for x in perm.cycle_path:
        change = {x.value[i]: x.value[i+1] for i in range(len(x.value) - 1)}
        for item in ng:
            if item[0] in change.keys():
                item[0] = change[item[0]]
            for i, neighbour in enumerate(item[1]):
                if neighbour in change.keys():
                    item[1][i] = change[neighbour]
    ng = {item[0]: set(item[1]) for item in ng}
    ng = {key: ng[key] for key in sorted(ng.keys())}
    return Graph(ng)


if __name__ == '__main__':
    g = Graph({1: {2}, 2: {1, 3}, 3: {2}, 4: set()})
    g = Graph({1: {2, 3}, 2: {1, 4}, 3: {1}, 4: {2}})
    # g = Graph({1: {2, 3, 4, 5}, 2: {1}, 3: {1}, 4: {1}, 5: {1}})
    # g = Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2}, 4: {2, 5, 6}, 5: {4}, 6: {5}})
    # g = Graph({1: {2}, 2: {1, 3}, 3: {2, 4}, 4: {3, 5}, 5: {4, 6}, 6: {5, 7}, 7: {6}})
    # g = Graph({1: {2}, 2: {1, 3}, 3: {2, 4}, 4: {3, 5}, 5: {4, 6}, 6: {5, 7}, 7: {6}, 8: set()})
    # g = Graph({1: {2}, 2: {1, 3}, 3: {2, 4}, 4: {3, 5}, 5: {4, 6}, 6: {5}, 7: set(), 8: set()})
    # g = Graph({1: {2, 3, 4, 5}, 2: {1}, 3: {1}, 4: {1}, 5: {1}})
    # g = Graph({1: {2, 3}, 2: {1, 4, 5}, 3: {1}, 4: {2}, 5: {2}})
    # g = Graph({1: {2, 3, 4}, 2: {1, 5}, 3: {1}, 4: {1}, 5: {2}})
    # g = Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4, 5}, 4: {2, 3, 5}, 5: {3, 4, 6}, 6: {5}})

    orig = {*range(1, len(g.data.keys()) + 1)}
    total = 0
    start = time.time()
    induced_subgraphs = dict()
    for i in range(len(orig) + 1):
        x = [PartialPerm(*x) for x in itertools.product(itertools.combinations(orig, i), itertools.permutations(orig, i))]
        for perm in x:
            subgraph = create_subgraph(set(perm.dom), g)
            info = (subgraph.vertex_count(), subgraph.edge_count())
            new_graph = partial_perm_graph(perm, g)
            if new_graph == subgraph:
                # print(perm)
                if perm.is_cycle():
                    induced_subgraphs.setdefault(info, []).insert(0, perm)
                else:
                    induced_subgraphs.setdefault(info, []).append(perm)
                total += 1
    for key in induced_subgraphs:
        print('Vertex, Edge:', *key)
        if not is_group(induced_subgraphs[key]):
            for row in get_box(induced_subgraphs[key]):
                for col in row:
                    print(*col, end='; ')
                print()
        else:
            print(*induced_subgraphs[key], sep='; ')
    print(total)
    print(time.time() - start)
