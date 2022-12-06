import itertools
from itertools import chain, combinations

from cycle_notation import to_cycle_path_notation, Path, Cycle


class PartialPerm:

    def __init__(self, dom, ran):
        self.dom = dom
        self.ran = ran
        self.cycle_path = to_cycle_path_notation(dom, ran)

    def __str__(self):
        # return str(self.dom) + ' -> ' + str(self.ran)
        if len(self.cycle_path) == 0:
            return 'id'
        return 'v'.join(str(x) for x in self.cycle_path)

    def is_cycle(self):
        for item in self.cycle_path:
            if isinstance(item, Path):
                return False
        return True

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        # return sum(self.dom) == sum(other.dom) and sum(self.ran) == sum(other.ran)
        return self.ran == other.ran and self.dom == other.dom

    def __lt__(self, other):
        # return sum(self.ran) < sum(other.ran) or sum(self.dom) < sum(other.dom)
        return self.dom < other.dom

    # def __le__(self, other):
    #     return sum(self.ran) <= sum(other.ran) or sum(self.dom) <= sum(other.dom)


def powerset(s):
    res = []
    for r in range(len(s) + 1):
        for comb in itertools.combinations(s, r):
            lst = list(comb) + [None for _ in range((len(s) - len(comb)))]
            res.extend(itertools.permutations(lst))
    return set(res)


if __name__ == '__main__':
    orig = {*range(1, 5)}
    total = 0
    # print(*itertools.product({1, 2, 3}, {1, 2, 3}, repeat=1))
    # print(len(list(itertools.product(itertools.combinations({1, 2, 3}, 2), itertools.permutations({1, 2, 3}, 2)))))
    for i in range(len(orig) + 1):
        x = [PartialPerm(*x) for x in itertools.product(itertools.combinations(orig, i), itertools.permutations(orig, i))]
        print(*x, sep='\n')
        total += len(x)
    print(total)
    # print(*itertools.product({1, 2, 3}, {1, 2, 3}, repeat=2))

    # p = powerset(orig)
    # partial_perms = []
    # for item in p:
    #     partial_perms.append(PartialPerm(tuple(range(1, len(orig) + 1)), item))
    # print(*partial_perms)
    # print(len(partial_perms))
