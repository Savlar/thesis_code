import time

from networkx import vf2pp_all_isomorphisms

from symmetries_app.symmetries_code.graph import Graph
from symmetries_app.symmetries_code.graph_generator import generate_random_graph
from symmetries_app.symmetries_code.partial_symmetries import PartialSymmetries


# https://www.sciencedirect.com/science/article/pii/S0095895617300539
asymmetric_graphs = {'X1': Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 5}, 4: {2, 6}, 5: {3}, 6: {4}}),
                     'X8': Graph({1: {2, 3}, 2: {1, 3, 4, 5}, 3: {1, 2, 4, 6}, 4: {2, 3, 6}, 5: {2, 6}, 6: {3, 4, 5}}),
                     'X2': Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 5}, 4: {2, 5, 6}, 5: {3, 4}, 6: {4}}),
                     'X7': Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4, 5}, 4: {2, 3, 6}, 5: {3, 6}, 6: {4, 5}}),
                     'X3': Graph({1: {2, 3}, 2: {1, 4}, 3: {1, 4, 5}, 4: {2, 3, 5, 6}, 5: {3, 4}, 6: {4}}),
                     'X6': Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4, 5}, 4: {2, 3, 5}, 5: {3, 4, 6}, 6: {5}}),
                     'X4': Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4, 5}, 4: {2, 3, 6}, 5: {3}, 6: {4}}),
                     'X5': Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4, 5}, 4: {2, 3, 5, 6}, 5: {3, 4}, 6: {4}}),
                     'X9': Graph({1: {2, 3}, 2: {1}, 3: {1, 4, 5}, 4: {3}, 5: {3, 6}, 6: {5, 7}, 7: {6}}),
                     'X14': Graph({1: {2, 3, 4, 5, 6}, 2: {1, 3, 5, 7}, 3: {1, 2, 4}, 4: {1, 3, 5, 6, 7}, 5: {1, 2, 4, 6, 7}, 6: {1, 4, 5, 7}, 7: {2, 4, 5, 6}}),
                     'X10': Graph({1: {2}, 2: {1, 3, 4}, 3: {2, 5}, 4: {2, 5, 6}, 5: {3, 4}, 6: {4, 7}, 7: {6}}),
                     'X13': Graph({1: {2, 3, 6}, 2: {1, 3, 4, 7}, 3: {1, 2, 4, 6}, 4: {2, 3, 5, 6, 7}, 5: {4, 6, 7}, 6: {1, 3, 4, 5, 7}, 7: {2, 4, 5, 6}}),
                     'X11': Graph({1: {2, 3}, 2: {1, 4}, 3: {1, 4, 5}, 4: {2, 3, 6}, 5: {3, 6, 7}, 6: {4, 5}, 7: {5}}),
                     'X12': Graph({1: {2, 3, 6}, 2: {1, 3, 4, 7}, 3: {1, 2, 4}, 4: {2, 3, 5, 6, 7}, 5: {4, 6, 7}, 6: {1, 4, 5, 7}, 7: {2, 4, 5, 6}}),
                     'X15': Graph({1: {2, 5}, 2: {1, 3}, 3: {2, 4, 6}, 4: {3, 5}, 5: {1, 4, 6, 7}, 6: {3, 5, 8}, 7: {5}, 8: {6}}),
                     'X18': Graph({1: {2, 4, 5, 6, 7}, 2: {1, 3, 4, 5, 6}, 3: {2, 6, 8}, 4: {1, 2, 5, 7}, 5: {1, 2, 4, 6, 7, 8}, 6: {1, 2, 3, 5, 7, 8}, 7: {1, 4, 5, 6, 8}, 8: {3, 5, 6, 7}}),
                     'X16': Graph({1: {2, 3, 6}, 2: {1, 4}, 3: {1, 5}, 4: {2, 5, 7}, 5: {3, 4, 6}, 6: {1, 5, 7, 8}, 7: {4, 6}, 8: {6}}),
                     'X17': Graph({1: {2, 4, 5, 6, 7}, 2: {1, 3, 6}, 3: {2, 5, 6, 8}, 4: {1, 5, 7, 8}, 5: {1, 3, 4, 6, 7, 8}, 6: {1, 2, 3, 5, 7}, 7: {1, 4, 5, 6, 8}, 8: {3, 4, 5, 7}}),
                     None: Graph({})}


def run(graph, only_full_symmetries=False, use_timer=False):
    """
    yields either full symmetries or all partial symmetries of 'graph'
    Parameters
    ----------
    graph
    only_full_symmetries - True if we only want full automorphisms
    use_timer - True if the execution should time out after 60 seconds
    """
    global asymmetric_graphs
    p = PartialSymmetries(graph, only_full_symmetries, use_timer)
    yield from p.get_partial_symmetries()


if __name__ == '__main__':
    # g = Graph({1: {2, 3, 4}, 2: {1, 4}, 3: {1, 4}, 4: {1, 2, 3}})
    # p = PartialSymmetries(g, only_full_symmetries=True)
    # for sym in p.get_partial_symmetries():
    #     print(sym)
    for _ in range(30):
        p = PartialSymmetries(generate_random_graph(11))
        print(p.graph.density())
        for _ in p.get_partial_symmetries():
            pass
        print(p.runtime)
    # for key in asymmetric_graphs.keys():
    #     p = PartialSymmetries(asymmetric_graphs[key])
    #     for _ in p.get_partial_symmetries():
    #         pass
    #     print(p.runtime)
