from symmetries_app.symmetries_code.graph import Graph
from symmetries_app.symmetries_code.graph_generator import generate_random_graph
from symmetries_app.symmetries_code.partial_symmetries import PartialSymmetries


# https://www.sciencedirect.com/science/article/pii/S0095895617300539
asymmetric_graphs = {'X1,X8': Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 5}, 4: {2, 6}, 5: {3}, 6: {4}}),

                     'X2,X7': Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 5}, 4: {2, 5, 6}, 5: {3, 4}, 6: {4}}),

                     'X3,X6': Graph({1: {2, 3}, 2: {1, 4}, 3: {1, 4, 5}, 4: {2, 3, 5, 6}, 5: {3, 4}, 6: {4}}),

                     'X4,X5': Graph({1: {2, 3}, 2: {1, 3, 4}, 3: {1, 2, 4, 5}, 4: {2, 3, 6}, 5: {3}, 6: {4}}),

                     'X9,X14': Graph({1: {2, 3}, 2: {1}, 3: {1, 4, 5}, 4: {3}, 5: {3, 6}, 6: {5, 7}, 7: {6}}),

                     'X10,X13': Graph({1: {2}, 2: {1, 3, 4}, 3: {2, 5}, 4: {2, 5, 6}, 5: {3, 4}, 6: {4, 7}, 7: {6}}),

                     'X11,X12': Graph(
                         {1: {2, 3}, 2: {1, 4}, 3: {1, 4, 5}, 4: {2, 3, 6}, 5: {3, 6, 7}, 6: {4, 5}, 7: {5}}),

                     'X15,X18': Graph(
                         {1: {2, 5}, 2: {1, 3}, 3: {2, 4, 6}, 4: {3, 5}, 5: {1, 4, 6, 7}, 6: {3, 5, 8}, 7: {5},
                          8: {6}}),

                     'X16,X17': Graph(
                         {1: {2, 3, 6}, 2: {1, 4}, 3: {1, 5}, 4: {2, 5, 7}, 5: {3, 4, 6}, 6: {1, 5, 7, 8}, 7: {4, 6},
                          8: {6}}),
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
    g = Graph({1: {12, 11, 14, 10, 3, 6, 13, 8, 4}, 2: {9, 13, 8, 12, 3, 7, 6, 5, 14, 11, 10}, 3: {10, 8, 11, 14, 2, 6, 4, 1, 9, 7}, 4: {11, 9, 7, 10, 14, 3, 8, 5, 1}, 5: {8, 12, 14, 9, 11, 10, 2, 4}, 6: {14, 11, 8, 3, 1, 10, 2, 13, 12, 9, 7}, 7: {14, 13, 4, 10, 9, 2, 12, 3, 11, 6}, 8: {5, 2, 3, 11, 9, 6, 12, 4, 10, 14, 1}, 9: {12, 2, 11, 13, 4, 8, 5, 7, 3, 10, 6, 14}, 10: {3, 12, 13, 14, 4, 7, 1, 6, 8, 5, 11, 9, 2}, 11: {4, 1, 9, 12, 3, 8, 6, 14, 5, 10, 13, 2, 7}, 12: {9, 1, 10, 5, 11, 2, 13, 8, 14, 7, 6}, 13: {2, 9, 7, 10, 12, 14, 6, 1, 11}, 14: {7, 6, 1, 3, 10, 13, 5, 11, 4, 12, 8, 2, 9}})
    print(g.density())
    # for _ in PartialSymmetries(generate_random_graph(22, 0.1), timeout_after=5, use_timer=True).get_partial_symmetries():
    #     pass
