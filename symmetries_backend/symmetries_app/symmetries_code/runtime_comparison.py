from symmetries_app.symmetries_code.graph import Graph

types = {1: 'deg_filter', 2: 'deg_tri_filter', 3: 'no_filter', 4: 'heuristic_filter'}


class GraphData:

    def __init__(self,  t, p, i, at):
        self.time = t
        self.partial = p
        self.induced = i
        self.all_times = at
        self.average_time = sum(self.all_times) / len(self.all_times)

    def __str__(self):
        return '\n'.join([str(self.time), str(self.partial), str(self.induced)])


class Runtimes:

    def __init__(self, graph):
        self.graph = graph
        self.runtime_data = dict()

    def add_runtime(self, key, value):
        self.runtime_data[key] = value


def read_data(filename):
    with open(filename, 'r') as file:
        data = list(filter(lambda x: len(x), file.read().split('\n')))
        return data


def read_input_file():
    with open('tests/inputs.txt', 'r') as file:
        data = file.read().split('\n')
        graphs = set()
        g = ''
        for row in data:
            if len(row) != 0:
                g += row + '\n'
            else:
                graphs.add(g)
                g = ''
        return graphs


def get_runtime_data():
    graphs = dict()
    new_graph, data = dict(), []
    for t in types.values():
        for row in read_data('tests/output_' + t + '.txt'):
            if 'Generated' in row:
                if len(new_graph) > 0:
                    times = list(map(float, data[:-2]))
                    avg_time = sum(times) / len(times)
                    data = GraphData(avg_time, int(float(data[-2])), int(data[-1]), times)
                    graph = Graph(new_graph, aut_group=set())
                    graphs.setdefault(str(graph), Runtimes(Graph(new_graph)))
                    if t in graphs[str(graph)].runtime_data.keys():
                        print('duplicate', str(graph))
                    graphs[str(graph)].add_runtime(t, data)
                new_graph, data = dict(), []
            elif '->' in row:
                key, values = row.split('->')
                values = set(map(int, filter(lambda x: len(x), values.split(' '))))
                new_graph[int(key)] = values
            elif row != '':
                data.append(row)
    return graphs


def compare_runtime(data, t1, t2, from_vertices=1, to_vertices=20):
    """

    Parameters
    ----------
    data -
    t1 - graph filtering type that is expected to be faster
    t2 - graph filtering type that is expected to be slower

    Returns
    -------

    """
    saved_time_seconds = []
    saved_time = []
    t1_faster = 0
    t1_slower = 0
    for key, value in data.items():
        value = value.runtime_data
        if str(from_vertices) in key and str(to_vertices) not in key:
            try:
                saved_time_seconds.append(value[t1].time - value[t2].time)
                saved_time.append((value[t1].time / value[t2].time) * 100)
                if saved_time_seconds[-1] > .1:
                    print(key, value[t1].time, saved_time_seconds[-1], saved_time[-1])
                if value[t2].time < value[t1].time:
                    t1_slower += 1
                else:
                    t1_faster += 1
            except KeyError:
                pass
    #             print(key)
    print(t1_faster, t1_slower)
    print(round(sum(saved_time) / len(saved_time), 2))


if __name__ == '__main__':
    all_graphs = read_input_file()
    runtimes = get_runtime_data()
    compare_runtime(runtimes, types[1], types[3], from_vertices=11, to_vertices=19)
