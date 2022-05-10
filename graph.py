class Graph:

    def __init__(self, data):
        self.data = data
        self.aut_group = []

    def __str__(self):
        out = '\nGenerated graph:\n'
        for i in range(len(self.data)):
            out += str(i) + ' -> ' + ' '.join(map(str, self.data[i])) + '\n'
        return out

    def __eq__(self, other):
        return self.data == other.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


class BipartiteGraph(Graph):

    def __init__(self, data, m, n):
        super().__init__(data)
        self.m = m
        self.n = n
