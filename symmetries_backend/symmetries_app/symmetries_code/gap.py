import time

import os
import subprocess

from symmetries_app.symmetries_code.graph import Graph


def generate_trees(n):
    """
    function to generate all possible trees with 'n' vertices using nauty-geng package, it creates temporary files in folder
    'gap_files', this folder must be created
    Returns
    -------
    data - list of strings, output from nauty-showg, in the format 'vertex : neighbours'
    """
    filename = str(hash('trees' + str(n) + str(time.time_ns()))) + '.txt'
    with open(os.devnull, 'w') as fnull:
        subprocess.run('sudo nauty-geng ' + str(n) + ' ' + str(n - 1) + ':' + str(n - 1) + ' -c > gap_files/' + filename,
                       shell=True, stdout=fnull, stderr=fnull)
    os.system('sudo nauty-showg gap_files/' + filename + ' > gap_files/out_' + filename)

    with open('gap_files/out_' + filename, 'r') as file:
        data = list(filter(lambda x: len(x) and 'Graph' not in x, file.read().split('\n')))
    os.remove('gap_files/' + filename)
    os.remove('gap_files/out_' + filename)
    return data


def get_non_isomorphic_trees(n):
    """
    returns all pairwise non-isomorphic trees with 'n'-vertices, represented using the 'Graph' class,
    calls the 'generate_trees' function and parses the output, GAP names vertices of n-vertex graph 0..n-1, our app uses
    1..n,
    does not calculate symmetries
    """
    data = generate_trees(n)
    data = [data[i:i+n] for i in range(0, len(data), n)]

    graphs = []
    for graph in data:
        graph_data = dict()
        for index, edge in enumerate(graph):
            graph_data[index + 1] = set()
            for neighbour in edge[:-1].split(':')[1].strip().split(' '):
                graph_data[index + 1].add(int(neighbour) + 1)
        graphs.append(Graph(graph_data, aut_group=set()))
    return graphs


def get_group_info(input_, filename):
    """
    return information about given group, output is sent to file
    Parameters
    ----------
    input_ - group entered in GAP format
    filename - file to which 'input_' will be writte
    """
    with open(filename, 'w') as file:
        file.write(input_)
    with open(os.devnull, 'w') as fnull:
        subprocess.run('sudo gap --quitonbreak -b ' + filename + ' -c "QUIT;"', shell=True, stdout=fnull, stderr=fnull)
