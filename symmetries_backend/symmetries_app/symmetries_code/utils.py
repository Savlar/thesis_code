import copy

import functools

import time

import random

import subprocess

from ast import literal_eval
import math

from symmetries_app.symmetries_code.graph import Graph
from symmetries_app.symmetries_code.graph_generator import generate_random_graph
from symmetries_app.symmetries_code.main import asymmetric_graphs
from symmetries_app.symmetries_code.partial_symmetries import PartialSymmetries

# https://oeis.org/A002720
# number of permutations of , i-th index is the number of partial permutations of i-element set
totals = [1, 2, 7, 34, 209, 1546, 13327, 130922, 1441729, 17572114, 234662231, 3405357682, 53334454417, 896324308634,
              16083557845279, 306827170866106, 6199668952527617, 132240988644215842, 2968971263911288999,
              69974827707903049154, 1727194482044146637521, 44552237162692939114282]


def read_graph_from_file():
    graphs = []
    with open('tests/inputs.txt', 'r') as file:
        file = file.read().split('\n')[:-1]
        d = dict()
        for row in file:
            if row == '':
                graphs.append(Graph(d, aut_group=set()))
                d = dict()
                continue
            key, values = row.split('->')
            values = set(map(int, filter(lambda x: len(x), values.split(' '))))
            d[int(key)] = values
    return graphs


def partial_symmetries_info(vertices, include_complete=True):
    with open('all_graphs/data/all_graphs_' + str(vertices) + 'v.txt') as file:
        file = file.read().split('\n')
        file = file[4:-5] if not include_complete else file[:-1]
        info = dict()
        for i in range(0, len(file), 4):
            data = literal_eval(file[i].strip())
            g = Graph(data, aut_group=set())
            p = PartialSymmetries(g, use_timer=False)
            edges = int(file[i + 1].split(':')[1].strip())
            p.total_partial_symmetries = int(file[i + 2].split(':')[1].strip())
            p.total_induced_subgraphs = int(file[i + 3].split(':')[1].strip())
            info.setdefault(edges, []).append(p)
    return info


def partial_symmetries_average(n):
    total = 0
    graph_count = 0
    for val in partial_symmetries_info(n).values():
        graph_count += len(val)
        for graph in val:
            total += graph.total_partial_symmetries
    print(n, round(total / graph_count, 2), round((total / graph_count) / totals[n], 5))


def run_tests(runs=3, clear_output_file=False):
    """
    function that runs tests for all graphs entered in 'tests/inputs.txt' file,
    output is appended to 'tests/output.txt' file
    Parameters
    ----------
    runs - how many times should partial symmetries be calculated for each graph
    clear_output_file - if contents of output file should first be deleted
    """
    if clear_output_file:
        with open('tests/output.txt', 'w') as file:
            file.write('')
    for graph in read_graph_from_file():
        runtime = []
        p = PartialSymmetries(graph, use_timer=False, only_full_symmetries=False)
        for i in range(runs):
            for _ in p.get_partial_symmetries():
                pass
            runtime.append(p.runtime)
            if i != runs - 1:
                p.clear()
        with open('tests/output.txt', 'a') as file:
            file.write(str(graph) + '\n')
            for t in runtime:
                file.write(str(t) + '\n')
            file.write(str(p.total_partial_symmetries) + '\n')
            file.write(str(p.total_induced_subgraphs) + '\n')


def run_asymmetric():
    for i in range(9):
        print(list(asymmetric_graphs.keys())[i])
        graph = asymmetric_graphs[list(asymmetric_graphs.keys())[i]]
        for j in range(2):
            graph.checks = 0
            p = PartialSymmetries(graph)
            for _ in p.get_partial_symmetries():
                pass
            print(p.runtime)
            print(p.total_partial_symmetries)
            print(p.total_induced_subgraphs)
            print(p.graph.checks)
            print()


def all_partial_symmetries(n):
    found = False
    for g in read_gap_file(n):
        if not found:
            if g.data == {1: {6, 8, 9}, 2: {7, 9, 10}, 3: {7}, 4: {8, 9, 10}, 5: set(), 6: {1, 10}, 7: {2, 3, 8, 10}, 8: {1, 4, 7, 9, 10}, 9: {1, 2, 4, 8}, 10: {2, 4, 6, 7, 8}}:
                found = True
            continue
        if g.edge_count() < 24:
            p = PartialSymmetries(g, use_timer=False)
            with open('all_graphs/data/all_graphs_' + str(n) + 'v.txt', 'a') as file:
                file.write(str(g.data) + '\n')
                file.write('Edges: ' + str(g.edge_count()) + '\n')
                file.write('Partial symmetries: ' + str(int(p.get_number_of_partial_symmetries())) + '\n')
                file.write('Non-isomorphic induced subgraphs: ' + str(p.total_induced_subgraphs) + '\n')


def single_edge_partial_symmetries(n):
    """
    calculates the number of partial symmetries for a graphs with 'n' vertices and 1 edge, all other vertices are
    isolated, this is the second highest number of partial symmetries for any 'n' vertex graph after K_n
    Parameters
    ----------
    n - number of vertices of the graph
    Returns
    -------
    total - number of partial symmetries for graph with 'n' vertices and 1 edge
    """
    total = 0
    for i in range(n + 1):
        if i == 0:
            total += 1
        elif i == 1:
            total += n ** 2
        elif i == n:
            total += math.factorial(n - 2) * 2
        else:
            subgraphs = math.comb(n - 2, i - 2)
            total += pow(subgraphs, 2) * (math.factorial(i - 2) * 2)
            subgraphs = 2 * math.comb(n - 2, i - 1) + math.comb(n - 2, i)
            total += pow(subgraphs, 2) * math.factorial(i)
    return total


def partial_perm_n_set(n):
    """
    counts the number of partial permutations of an 'n' element set, https://oeis.org/A002720
    Parameters
    ----------
    n - number of elements in a set
    Returns
    -------
    total - number of partial permutations of an 'n'-set
    """
    total = 0
    for i in range(n + 1):
        total += math.factorial(i) * math.comb(n, i) ** 2
    return total


def read_gap_file(n):
    """
    yields all graphs with 'n' vertices, without calculating their symmetries, only parses data from GAP files
    """
    data = dict()
    filename = 'all_graphs/gap/graph' + str(n) + '.g6'
    popen = subprocess.Popen(['nauty-showg', filename], stdout=subprocess.PIPE, universal_newlines=True)
    for std_out in iter(popen.stdout.readline, ''):
        std_out = std_out.strip()
        if 'Graph' in std_out:
            if len(data):
                yield Graph(data, aut_group=set())
                data = dict()
        elif std_out != '':
            key, value = std_out[:-1].split(':')
            key = int(key.strip()) + 1
            value = value.strip().split(' ')
            if value[0] != '':
                value = set(map(lambda x: x + 1, map(int, value)))
            else:
                value = set()
            data[key] = value
    yield Graph(data, aut_group=set())


def create_large_graphs():
    for _ in range(10):
        v = random.randrange(15, 21)
        g = generate_random_graph(v)
        with open('tests/large_inputs.txt', 'a') as file:
            file.write(str(g))

functools.lru_cache(maxsize=0)
def get_all_induced_subgraphs_test(g):
    ps = PartialSymmetries(Graph(copy.deepcopy(g.data), aut_group=set()), use_timer=False)
    induced_subgraphs = []
    start = time.time()
    for i in range(1, ps.graph.vertex_count() + 1):
        induced_subgraphs.extend(ps.graph.find_isomorphism_classes_list(i))
    print('no filter')
    print('Time: ', round(time.time() - start, 3))
    print('Total induced: ', len(induced_subgraphs))
    print('Checks: ', ps.graph.checks, '\n')

    ps = PartialSymmetries(Graph(copy.deepcopy(g.data), aut_group=set()), use_timer=False)
    induced_subgraphs = []
    start = time.time()
    for i in range(1, ps.graph.vertex_count() + 1):
        induced_subgraphs.extend(ps.graph.find_isomorphism_classes(i, 1))
    print('degree filter')
    print('Time: ', round(time.time() - start, 3))
    print('Total induced: ', len(induced_subgraphs))
    print('Checks: ', ps.graph.checks, '\n')

    ps = PartialSymmetries(Graph(copy.deepcopy(g.data), aut_group=set()), use_timer=False)
    induced_subgraphs = []
    start = time.time()
    for i in range(1, ps.graph.vertex_count() + 1):
        induced_subgraphs.extend(ps.graph.find_isomorphism_classes(i, 2))
    print('degree triangle filter')
    print('Time: ', round(time.time() - start, 3))
    print('Total induced: ', len(induced_subgraphs))
    print('Checks: ', ps.graph.checks, '\n')

    ps = PartialSymmetries(Graph(copy.deepcopy(g.data), aut_group=set()), use_timer=False)
    induced_subgraphs = []
    start = time.time()
    for i in range(1, ps.graph.vertex_count() + 1):
        type_id = 1 if (ps.graph.vertex_count() < 11 or 0.2 > ps.density or 0.8 < ps.density) else 2
        induced_subgraphs.extend(ps.graph.find_isomorphism_classes(i, type_id))
    print('heuristic filter')
    print('Time: ', round(time.time() - start, 3))
    print('Total induced: ', len(induced_subgraphs))
    print('Checks: ', ps.graph.checks, '\n')

def subgraphs_runtime_test():
    for _ in range(10):
        vertices = random.randrange(6, 7)
        g = generate_random_graph(vertices, 0)
        print(g.data)
        get_all_induced_subgraphs_test(g)


if __name__ == '__main__':
    run_tests(clear_output_file=True)
    # subgraphs_runtime_test()
