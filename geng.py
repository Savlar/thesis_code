import os


def get_data(x):
    n = x
    os.system('sudo nauty-geng ' + str(n) + ' ' + str(n - 1) + ':' + str(n - 1) + ' -c > temp.txt')
    os.system('sudo nauty-showg temp.txt > out.txt')

    with open('out.txt', 'r') as file:
        data = list(filter(lambda x: len(x) and 'Graph' not in x, file.read().split('\n')))

    data = [data[i:i+n] for i in range(0, len(data), n)]
    graphs = []

    for graph in data:
        graph_data = []
        for edge in graph:
            graph_data.append(set(map(int, edge[:-1].split(':')[1].strip().split(' '))))
        graphs.append(graph_data)

    return graphs
