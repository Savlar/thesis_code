import copy
import itertools
from typing import Dict, Set, Tuple, List

from networkx import vf2pp_all_isomorphisms, vf2pp_is_isomorphic
import networkx as nx

from symmetries_app.symmetries_code.isomorphism_class import IsomorphismClass, check_if_isomorphic


class Graph:

    def __init__(self, data=None, aut_group=None, group_type=None):
        self.data: Dict[int: Set[int]] = data
        self.nx_rep = self.get_nx_graph() if data is not None else None
        self.aut_group = aut_group
        self.checks = 0
        if aut_group is None:
            self.get_symmetries()
        self.group_type = group_type

    def __len__(self) -> int:
        return len(self.data.keys())

    def __getitem__(self, index: int) -> Set[int]:
        return self.data[index]

    def __str__(self) -> str:
        out = '\nGenerated graph:\n'
        for key in sorted(self.data.keys()):
            out += str(key) + ' -> ' + ' '.join(map(str, sorted(self.data[key]))) + '\n'
        return out

    def __eq__(self, other) -> bool:
        return self.data == other.data

    def __hash__(self) -> int:
        return hash(str(self))

    def vertices(self) -> List[int]:
        return list(self.data.keys())

    def edges(self) -> List[Tuple[int, int]]:
        result = []
        for v in self.vertices():
            for neighbour in self.get_neighbours(v):
                if neighbour > v:
                    result.append((v, neighbour))
        return result

    def degree(self, vertex) -> int:
        if vertex not in self.vertices():
            return -1
        return len(self.data[vertex])

    def min_degree(self):
        return min(self.degree_sequence())

    def max_degree(self):
        return max(self.degree_sequence())

    def degree_sequence(self) -> Tuple[int]:
        return tuple(sorted(self.degree(key) for key in self.vertices()))

    def triangle_sequence(self) -> Tuple:
        size = len(self)
        vertices = list(self.data.keys())
        triangles = dict().fromkeys(vertices, 0)
        done = set()
        for i in range(size):
            vertex = vertices[i]
            done.add(vertex)
            neighbours = self.get_neighbours(vertex).difference(done)
            for _from, to in itertools.combinations(neighbours, 2):
                if _from in self.data[to]:
                    triangles[_from] += 1
                    triangles[to] += 1
                    triangles[vertex] += 1
        return tuple(sorted(triangles.values()))

    def graph_sequence(self):
        return self.degree_sequence() + self.triangle_sequence()

    def total_possible_edges(self):
        v = self.vertex_count()
        return (v * (v - 1)) // 2

    def density(self):
        if self.edge_count() == 0:
            return 0
        return self.edge_count() / self.total_possible_edges()

    def triangles(self, vertex):
        neighbours = self.get_neighbours(vertex)
        triangles = 0
        for _from, to in itertools.combinations(neighbours, 2):
            if _from in self.data[to]:
                triangles += 1
        return triangles

    def get_neighbours(self, vertex) -> Set[int]:
        if vertex not in self.vertices():
            return set()
        return self.data[vertex]

    def vertex_count(self) -> int:
        return len(self)

    def edge_count(self) -> int:
        return sum(len(neighbours) for neighbours in self.data.values()) // 2

    def add_vertex(self, to_add):
        if to_add not in self.vertices():
            self.data[to_add] = set()

    def add_edge(self, _from, to):
        """
        adds a new edge to the graph, if the vertices do not exist, they are created
        """
        self.add_vertex(_from)
        self.add_vertex(to)
        self.data[_from].add(to)
        self.data[to].add(_from)
        self.changed_graph()

    def remove_vertex(self, to_remove):
        """
        function that removes a vertex 'to_remove' from the graph and also removes it as a neighbour from other vertices
        """
        if to_remove in self.vertices():
            del self.data[to_remove]
            for vertex in self.data.keys():
                self.remove_vertex_from_neighbours(vertex, to_remove)
        self.changed_graph()

    def remove_vertex_from_neighbours(self, key, to_remove):
        self.data[key] = self.data[key].difference({to_remove})
        self.changed_graph()

    def remove_edge(self, _from, to):
        self.remove_vertex_from_neighbours(_from, to)
        self.remove_vertex_from_neighbours(to, _from)

    def get_nx_graph(self):
        g = nx.Graph()
        g.add_nodes_from(self.data.keys())
        for key in self.data.keys():
            for neighbour in self[key]:
                g.add_edge(key, neighbour)
        self.nx_rep = g
        return self.nx_rep

    def is_isomorphic(self, other):
        return vf2pp_is_isomorphic(self.nx_rep, other.nx_rep)

    def changed_graph(self):
        self.nx_rep = self.get_nx_graph()
        self.get_symmetries()

    def get_symmetries(self):
        """
        function that finds all symmetries of the graph and sorts it and return a tuple 't',
        so that the i-th index in 't' means the vertex i-th vertex in the vertex set gets mapped to vertex t[i]
        """
        self.aut_group = list()
        for sym in vf2pp_all_isomorphisms(self.nx_rep, self.nx_rep):
            self.aut_group.append(tuple(sym[key] for key in sorted(sym)))

    def is_asymmetric(self):
        total = 0
        for _ in vf2pp_all_isomorphisms(self.nx_rep, self.nx_rep):
            total += 1
            if total > 1:
                return False
        return True

    def create_subgraph(self, new_vertex_set, find_aut=False):
        new_data = dict()
        for key in new_vertex_set:
            new_data[key] = self.data[key].intersection(new_vertex_set)
        return Graph(new_data, aut_group=set() if not find_aut else None)

    def create_subgraph_without_edges(self, to_remove_edges):
        data = copy.deepcopy(self.data)
        for _from, to in to_remove_edges:
            data[_from].remove(to)
            data[to].remove(_from)
        return Graph(data=data)

    def find_isomorphism_classes_list(self, size):
        vertices = self.vertices()
        induced_subgraphs = []
        for comb in itertools.combinations(vertices, size):
            subgraph = self.create_subgraph(set(comb), True)
            isomorphic, graph, checks = check_if_isomorphic(subgraph, induced_subgraphs)
            self.checks += checks
            if isomorphic:
                graph.add_isomorphic(subgraph)
            else:
                induced_subgraphs.append(IsomorphismClass(subgraph))
        yield from list(sorted(induced_subgraphs, key=lambda x: x.rep.edge_count()))

    def find_isomorphism_classes(self, size, type_id=1):
        vertices = self.vertices()
        induced_subgraphs = dict()
        for comb in itertools.combinations(vertices, size):
            subgraph = self.create_subgraph(set(comb), True)
            seq = subgraph.degree_sequence() if type_id == 1 else subgraph.graph_sequence()
            if seq not in induced_subgraphs.keys():
                induced_subgraphs[seq] = {IsomorphismClass(subgraph)}
            elif subgraph.vertex_count() < 5:
                # no 2 graphs with < 5 vertices can have the same degree sequence and not be isomorphic
                (graph,) = induced_subgraphs[seq]
                graph.add_isomorphic(subgraph)
            else:
                isomorphic, graph, checks = check_if_isomorphic(subgraph, induced_subgraphs[seq])
                self.checks += checks
                if isomorphic:
                    graph.add_isomorphic(subgraph)
                else:
                    induced_subgraphs[seq].add(IsomorphismClass(subgraph))
        yield from list(sorted(set().union(*(induced_subgraphs.values())), key=lambda x: x.rep.edge_count()))

    def group_desc(self):
        if self.group_type is None:
            return ''
        types = [self.group_type]
        if 'x' in self.group_type:
            types = [x.strip() for x in self.group_type.split('x')]
        group_types = {'C': 'cyclic group', 'S': 'symmetric group', 'D': 'dihedral group', '1': 'error'}
        group_sizes = {'C': ' of order ', 'S': ' of degree ', 'D': ' of order ', '1': 'error'}
        d = []
        for t in types:
            desc = ''
            if t:
                desc += group_types[t[0]]
                desc += group_sizes[t[0]] + t[1:]
            d.append(desc)
        return ' x '.join(d)

    def get_gap_repr(self, filename: str):
        cycles = ['()']
        for cycle in self.aut_group:
            repr_ = cycle.gap_repr()
            if len(repr_):
                cycles.append(repr_)
        return 'g := Group(' + ','.join(cycles) + '); desc:=StructureDescription(g); AppendTo("' + filename + '",Concatenation(desc, "\\n"));\n'
