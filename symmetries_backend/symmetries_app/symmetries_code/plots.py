import numpy as np
import matplotlib.pyplot as plt

from symmetries_app.symmetries_code.runtime_comparison import get_runtime_data
from symmetries_app.symmetries_code.utils import partial_symmetries_info

PARTIAL_SYMMETRIES_IMG_DIR = 'all_graphs/partial_symmetries_images/'


def time_comparison():
    xrange = np.arange(30, 45, 1)
    plt.ylim(0, 50)
    plt.xlabel('n-th Fibonacci number')
    plt.ylabel('time in seconds')
    with open('tests/interpreter_test_data.txt', 'r') as file:
        file = file.read().split('\n')
        for i in range(4):
            data = list(map(float, file[15 * i:15 * (i + 1)]))
            plt.plot(xrange, data)
        plt.legend(['CPython', 'PyPy', 'Java', 'C'])
        plt.savefig('tests/lang_comparison.jpg', dpi=1000)


def kotlin_python_partial_sym_comparison_minimal_asym():
    graphs = {'X1': [0.050, 0.028], 'X2': [0.042, 0.018], 'X3': [0.039, 0.012], 'X4': [0.031, 0.013], 'X9': [0.132, 0.040],
              'X10': [0.176, 0.034], 'X11': [0.169, 0.030], 'X15': [1.175, 0.071], 'X16': [1.235, 0.084]}
    create_scatter_graph(graphs.keys(), [list(x[0] for x in graphs.values()), list(x[1] for x in graphs.values())],
                ['Results in [Slá21]', 'Our results'], filename='tests/comparison_asymmetric_slavik.jpg')


def kotlin_python_partial_sym_comparison_random():
    graphs = {'7,0': [0.215, 0.335], '8,27': [2.424, 1.511], '8,12': [4.291, 0.058], '9,11': [72.948, 0.192],
          '10,17': [186.448, 0.443], '10,11': [291.316, 0.699]}
    x_labels = [r'$G_{' + x + '}$' for x in graphs.keys()]
    create_scatter_graph(x_labels, [list(x[0] for x in graphs.values()), list(x[1] for x in graphs.values())],
                         legend=['Results in [Slá21]', 'Our results'], filename='tests/comparison_random_slavik.jpg')

def create_scatter_graph(x, y, legend=None, dpi=1000, filename='test.jpg'):
    plt.figure(figsize=(5, 5))
    plt.xlabel('graph')
    plt.ylabel('time (s)')
    for values in y:
        plt.scatter(x, values)
    plt.legend(legend)
    plt.savefig(filename, dpi=dpi)


def create_partial_symmetries_max_values_graph(n):
    info = partial_symmetries_info(n, include_complete=True)
    size = len(info) if len(info) % 2 == 0 else len(info) + 2
    plt.xticks(range(0, (size // 2), 1))
    plt.legend(['number of vertices', 'number of partial symmetries'])
    spacing = None
    for key in sorted(info.keys())[:size // 2]:
        psym_max = max(info[key], key=lambda x: x.total_partial_symmetries)
        if spacing is None:
            spacing = psym_max.total_partial_symmetries * 0.03
        print(key, psym_max.total_partial_symmetries)
        plt.scatter(key, psym_max.total_partial_symmetries)
        y_location = psym_max.total_partial_symmetries + spacing * 0.8 if key % 2 == 1 else psym_max.total_partial_symmetries - spacing * 1.5
        plt.annotate(str(psym_max.total_partial_symmetries), (key - 0.45, y_location), fontsize=6)
    plt.savefig(PARTIAL_SYMMETRIES_IMG_DIR + str(n) + '_vertices_max_values.jpg')


def create_partial_symmetries_graph(n, include_complete=False):
    start = 0 if include_complete else 1
    step = 1 if n < 7 else 2
    plt.xlabel('number of edges')
    plt.ylabel('number of partial symmetries')
    max_edges = (n * (n - 1) // 2)
    plt.xticks(range(start, max_edges + 1, step))
    data = partial_symmetries_info(n, include_complete=include_complete)
    for key in sorted(list(data.keys()))[:max_edges // 2 + 1]:
        partial_symmetries = list(set(x.total_partial_symmetries for x in data[key]))
        plt.scatter([key] * len(partial_symmetries), partial_symmetries)
        plt.scatter([max_edges - key] * len(partial_symmetries), partial_symmetries)
    img_type = 'all' if include_complete else 'minus_complete'
    plt.savefig(PARTIAL_SYMMETRIES_IMG_DIR + str(n) + '_vertices_' + img_type + '.jpg', dpi=1000)


def create_runtime_comparison_graph():
    runtimes = get_runtime_data()
    no_filter = []
    deg_filter = []
    deg_tri_filter = []
    labels = []
    for runtime in runtimes.values():
        if runtime.graph.vertex_count() > 11:
            vertices = runtime.graph.vertex_count()
            label = '$G_{' + str(vertices) + ',' + str(runtime.graph.edge_count()) + '}$'
            labels.append(label)
            no_filter.append(runtime.runtime_data['no_filter'].average_time)
            deg_filter.append(runtime.runtime_data['deg_filter'].average_time)
            deg_tri_filter.append(runtime.runtime_data['deg_tri_filter'].average_time)
    labels = sorted(labels)
    fig, ax = plt.subplots()
    ax.plot(no_filter, color='limegreen')
    ax.plot(deg_filter, color='orange')
    ax.plot(deg_tri_filter, color='cornflowerblue')
    plt.ylim(0, 175)
    xticks = range(0, len(labels), 8)
    ax.tick_params(axis='x', labelsize=8)
    ax.set_xticks(xticks)
    ax.set_xticklabels(labels[::8])
    plt.legend(['no filter', 'degree filter', 'degree triangle filter'])
    plt.xlabel('graph')
    plt.ylabel('runtime (s)')

    coefficients_deg_tri = np.polyfit(range(len(labels)), deg_tri_filter, 1)
    coefficients_deg = np.polyfit(range(len(labels)), deg_filter, 1)
    coefficients_no = np.polyfit(range(len(labels)), no_filter, 1)
    deg_tri = np.poly1d(coefficients_deg_tri)
    deg = np.poly1d(coefficients_deg)
    no = np.poly1d(coefficients_no)
    ax.plot(range(len(labels)), [no(i) for i in range(len(labels))], '--', color='limegreen')
    ax.plot(range(len(labels)), [deg(i) for i in range(len(labels))], '--', color='orange')
    ax.plot(range(len(labels)), [deg_tri(i) for i in range(len(labels))], '--', color='cornflowerblue')

    plt.savefig('tests/graph_filtering_runtime_comparison.jpg', dpi=1000)


if __name__ == '__main__':
    # kotlin_python_partial_sym_comparison_minimal_asym()
    # kotlin_python_partial_sym_comparison_random()
    # create_partial_symmetries_graph(10)
    # create_runtime_comparison_graph()
    create_partial_symmetries_max_values_graph(8)
