import random

from typing import Dict

import copy

import itertools
from ast import literal_eval

import networkx as nx

from symmetries_app.symmetries_code.graph import Graph
from symmetries_app.symmetries_code.graph_generator import generate_random_graph
from symmetries_app.symmetries_code.utils import read_gap_file


def induced_asymmetric(g, size):
    """
    generates all induced subgraphs with 'size' vertices
    Parameters
    ----------
    g - instance of 'Graph'
    size - number of vertices of a subgraph

    Returns
    -------
    are_asymmetric; subgraphs - True if all induced subgraphs with 'size' vertices are asymmetric; a dictionary of all
    induced subgraphs with 'size' vertices, filtered by their degree sequences, this only matters when 'are_asymmetric' is True
    """
    subgraphs = dict()
    for vertices in itertools.combinations(g.vertices(), size):
        subgraph = g.create_subgraph(vertices, False)
        if not subgraph.is_asymmetric():
            return False, dict()
        subgraphs.setdefault(subgraph.degree_sequence(), []).append(subgraph)
    return True, subgraphs


def asymmetric_non_isomorphic(graphs):
    """
    returns True if all asymmetric graphs in the list 'graphs' are pairwise non-isomorphic
    """
    for key in graphs:
        for a, b in itertools.combinations(graphs[key], 2):
            if nx.vf2pp_is_isomorphic(a.nx_rep, b.nx_rep):
                return False
    return True


def has_asymmetricity_level(g, depth):
    """
    returns True is graph 'g' has asymmetricity level 'depth'
    """
    for i in reversed(range(depth + 1)):
        asym, subgraphs = induced_asymmetric(g, len(g) - i)
        if not asym or not asymmetric_non_isomorphic(subgraphs):
            return False
    return True


def find_asym_d(g):
    """
    returns the asymmetric depth for graph 'g'
    """
    depth = -1
    while True:
        asym, subgraphs = induced_asymmetric(g, len(g) - (depth + 1))
        if not asym or not asymmetric_non_isomorphic(subgraphs):
            return depth
        depth += 1


def asym_depth_for_n_vertices(n):
    """
    returns the asymmetric depth any graph with 'n' vertices can have
    Parameters
    ----------
    n - number of vertices of a graph

    Returns
    -------
    cur_max; graphs_with_max_depth - asymmetric depth; a list of graphs with asymmetric depth 'cur_max'
    """
    cur_max = 0
    graphs_with_max_depth = []
    for g in read_gap_file(n):
        max_depth = find_asym_d(g)
        if max_depth == cur_max:
            graphs_with_max_depth.append(g)
        elif max_depth > cur_max:
            graphs_with_max_depth = [g]
            cur_max = max_depth
    return cur_max, graphs_with_max_depth


def add_vertex_to_asymmetric(add_to_vertices, from_depth, to_depth):
    with open('all_graphs/asymmetric/asym_d_' + str(from_depth) + '_' + str(add_to_vertices) + 'v.txt') as file:
        file = file.read().split('\n')[:-1]
        for g in file:
            data = literal_eval(g)
            new_vertex = len(data) + 1
            for no_neighbours in range(len(data) + 1):
                for combs in itertools.combinations(data.keys(), no_neighbours):
                    data_copy: Dict = copy.deepcopy(data)
                    if len(combs) == 0:
                        data_copy[new_vertex] = set()
                    for vertex in combs:
                        data_copy.setdefault(new_vertex, set()).add(vertex)
                        data_copy[vertex].add(new_vertex)
                    if has_asymmetricity_level(Graph(data_copy, aut_group=set()), to_depth):
                        with open('all_graphs/asymmetric/asym_d_' + str(to_depth) + '_' + str(add_to_vertices + 1) + 'v.txt', 'a') as output:
                            output.write(str(data_copy) + '\n')


def find_asym_d_random(only_save_depth_gte=4):
    """
    finds the maximal asymmetric depth for randomly generated graphs,
    only saves graphs with maximal asymmetric depth >= 'only_save_depth_gte'
    """
    while True:
        vertices = random.randrange(25, 31)
        g = generate_random_graph(vertices)
        asym_d_max = find_asym_d(g)
        if asym_d_max >= only_save_depth_gte:
            with open('all_graphs/asymmetric/random_maximal_asym_d.txt', 'a') as file:
                file.write(str(asym_d_max) + ' -> ' + str(g.data) + '\n')


if __name__ == '__main__':
    # depth, graphs = max_depth_for_n_vertices(9)
    # print(depth, len(graphs))
    # add_vertex_to_asymmetric(11, 1, 2)
    find_asym_d_random(5)
