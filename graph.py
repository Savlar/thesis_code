class Graph:

    def __init__(self, data):
        self.data = data
        self.aut_group = set()
        self.group_type = None

    def __len__(self):
        return len(self.data.keys())

    def __str__(self):
        out = '\nGenerated graph:\n'
        for key in self.data.keys():
            out += str(key) + ' -> ' + ' '.join(map(str, self.data[key])) + '\n'
        return out

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(str(self))

    def is_group(self):
        for item in self.aut_group:
            if not item.is_cycle():
                return False
        return True

    def vertex_count(self):
        return len(self)

    def edge_count(self):
        return sum(len(neighbours) for neighbours in self.data.values()) // 2

    def group_desc(self):
        if self.group_type is None:
            return ''
        types = [self.group_type]
        if 'x' in self.group_type:
            types = [x.strip() for x in self.group_type.split('x')]
        group_types = {'C': 'cyclic group', 'S': 'symmetric group', 'D': 'dihedral group', '1': 'error'}
        group_sizes = {'C': ' of size ', 'S': ' of degree ', 'D': ' of size ', '1': 'error'}
        d = []
        for t in types:
            desc = ''
            if t:
                desc += group_types[t[0]]
                desc += group_sizes[t[0]] + t[1:]
            d.append(desc)
        return ' x '.join(d)

    def __getitem__(self, index):
        return self.data[index]

    def get_gap_repr(self):
        cycles = ['()']
        for cycle in self.aut_group:
            repr_ = cycle.gap_repr()
            if len(repr_):
                cycles.append(repr_)
        return 'g := Group(' + ','.join(cycles) + '); desc:=StructureDescription(g); AppendTo("output_test.txt",Concatenation(desc, "\\n"));\n'


class BipartiteGraph(Graph):

    def __init__(self, data, m, n):
        super().__init__(data)
        self.m = m
        self.n = n


class Subgraph(Graph):

    def __init__(self, data, partial_perms):
        super().__init__(data)
        self.partial_perms = partial_perms
