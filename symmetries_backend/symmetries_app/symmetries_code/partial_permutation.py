from symmetries_app.symmetries_code.cycle_notation import to_cycle_path_notation


class PartialPermutation:
    """
    class for representing partial permutations
    """

    def __init__(self, dom, ran):
        self.dom = dom
        self.ran = ran
        self.cycle_path = to_cycle_path_notation(dom, ran)

    def __str__(self):
        if len(self.cycle_path) == 0:
            return 'id'
        return 'v'.join(str(x) for x in self.cycle_path)

    def __getitem__(self, item):
        return self.dom[self.ran.index(item)]

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.ran == other.ran and self.dom == other.dom

    def __lt__(self, other):
        return self.dom < other.dom

    def is_cycle(self):
        """
        returns True if this partial permutation only contains cycles, so domain = range
        """
        return self.dom == self.ran
