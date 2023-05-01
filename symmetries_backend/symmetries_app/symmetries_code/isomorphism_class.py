import math

from networkx import vf2pp_is_isomorphic

from symmetries_app.symmetries_code.partial_permutation import PartialPermutation


def check_if_isomorphic(graph, other):
    """
    checks if 'graph' is isomorphic to any graph in the list 'other'
    Returns
    -------
    triple (is_isomorphic; graph; checks) - (
        True if 'graph' is isomorphic to any graph in 'other';
        if it is isomorphic, then the graph to which it is isomorphic (representative of that isomorphism class);
        how many times we called the 'is_isomorphic' function
    )
    """
    checks = 0
    if graph is None:
        return False, None, checks
    for g in other:
        checks += 1
        if g.is_isomorphic(graph.nx_rep):
            return True, g, checks
    return False, None, checks


class IsomorphismClass:

    def __init__(self, rep):
        self.graphs = [rep]
        self.rep = rep
        self.d_class = []

    def size(self):
        """
        calculates the size of the d-class eggbox diagram
        """
        return math.pow(len(self.graphs), 2) * len(self.rep.aut_group)

    def is_isomorphic(self, other):
        """
        uses vf2++ algorithm to check if the representative of this isomorphic class is isomorphic to 'other' graph
        """
        return vf2pp_is_isomorphic(self.rep.nx_rep, other)

    def add_isomorphic(self, item):
        self.graphs.append(item)

    def create_d_class(self):
        """
        creates the eggbox diagram for this isomorphism class
        """
        vertex_combinations = list(x.vertices() for x in self.graphs)
        for i, graph in enumerate(self.graphs):
            self.d_class.append([])
            for j, dom in enumerate(vertex_combinations):
                h_class = []
                for ran in graph.aut_group:
                    h_class.append(str(PartialPermutation(dom, ran)))
                self.d_class[-1].append({'data': h_class, 'is_group': i == j and len(dom) > 1})
