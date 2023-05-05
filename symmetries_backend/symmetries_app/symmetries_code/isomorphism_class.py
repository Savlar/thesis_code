import math

from networkx import vf2pp_is_isomorphic, vf2pp_all_isomorphisms

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
        if g.is_isomorphic(graph):
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
        return self.rep.is_isomorphic(other)

    def add_isomorphic(self, item):
        self.graphs.append(item)

    def create_d_class(self):
        """
        creates the eggbox diagram for this isomorphism class
        """
        vertices = [g.vertices() for g in self.graphs]
        size = len(self.graphs)
        for i in range(size):
            self.d_class.append([])
            for j in range(size):
                h_class = []
                if i != j:
                    for mapping in vf2pp_all_isomorphisms(self.graphs[j].nx_rep, self.graphs[i].nx_rep):
                        h_class.append(str(PartialPermutation(list(mapping.keys()), list(mapping.values()))))
                else:
                    dom = vertices[j]
                    for ran in self.graphs[i].aut_group:
                        h_class.append(str(PartialPermutation(dom, ran)))
                self.d_class[-1].append({'data': h_class, 'is_group': i == j and len(h_class) > 1})
