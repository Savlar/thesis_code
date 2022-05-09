from typing import Set


def to_cycle_notation(lst):
    out = []
    unchecked = set(range(len(lst)))
    while unchecked:
        current = unchecked.pop()
        bracket = [current]
        while True:
            if lst[current] == current or lst[current] in bracket:
                out.append(tuple(bracket))
                break
            bracket.append(lst[current])
            current = lst[current]
            unchecked.remove(current)
    return out


class CycleNotation:

    def __init__(self, data=None):
        self.cycle_notation = []
        if data:
            self.cycle_notation = to_cycle_notation(data)

    def __len__(self):
        return sum(len(x) for x in self.cycle_notation)

    def flatten(self) -> Set[int]:
        return set(item for set_ in self.cycle_notation for item in set_)

    def __str__(self):
        return ''.join((str(x) for x in self.cycle_notation))

    def __repr__(self):
        return self.__str__()

    def __mul__(self, other):
        result = []
        # remaining = self.flatten().union(other.flatten())
        remaining = set(range(len(self)))
        while remaining:
            current_item = list(remaining)[0]
            first_item = current_item
            result_set = [current_item]
            while True:
                next_item = other.get_next(current_item)
                next_item_other = self.get_next(next_item)
                current_item = next_item_other
                if current_item == first_item:
                    break
                result_set.append(next_item_other)
            result.append(tuple(result_set))
            remaining.difference_update(result_set)
        result = [set(x) for x in result]
        c = CycleNotation()
        c.cycle_notation = result
        return c

    def get_set_containing(self, what):
        for set_ in self.cycle_notation:
            if what in set_:
                return set_

    def get_next(self, what):
        for set_ in self.cycle_notation:
            if what in set_:
                for i, item in enumerate(list(set_)):
                    if what == item:
                        if i == len(set_) - 1:
                            return list(set_)[0]
                        else:
                            return list(set_)[i + 1]
