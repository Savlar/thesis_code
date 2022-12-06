from typing import Set


class Cycle:

    def __init__(self, cycle):
        self.value = cycle

    def __str__(self):
        return str(tuple(self.value[:-1]))


class Path:

    def __init__(self, path):
        self.value = path

    def __str__(self):
        return '[' + ''.join(map(str, self.value)) + ')'


def to_cycle_notation(lst):
    mapping = {key: lst[i] for i, key in enumerate(sorted(lst))}
    out = []
    unchecked = set(lst)
    while unchecked:
        current = unchecked.pop()
        bracket = [current]
        while True:
            if mapping[current] in bracket or mapping[current] == current:
                out.append(tuple(bracket))
                break
            bracket.append(mapping[current])
            current = mapping[current]
            unchecked.remove(current)
    return out


def find_start(dom, ran, unchecked):
    for i, item in enumerate(dom):
        if item not in ran and ran[i] in unchecked:
            return ran[i]
    return None


def to_cycle_path_notation(dom, ran):
    out = []
    unchecked = set(ran)
    while unchecked:
        min_unchecked = find_start(dom, ran, unchecked) or min(unchecked)
        curr_index = ran.index(min_unchecked)
        first = dom[curr_index]
        bracket = []
        while True:
            if curr_index == -1:
                out.append(Path(bracket))
                break
            current = ran[curr_index]
            if current in bracket:
                out.append(Cycle([first] + bracket))
                break
            bracket.append(current)
            unchecked.remove(current)
            try:
                curr_index = dom.index(current)
            except ValueError:
                bracket = [first] + bracket
                bracket = bracket[::-1]
                curr_index = -1
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

    def gap_repr(self):
        repr_str = ''
        for cycle in self.cycle_notation:
            if len(cycle) > 1:
                repr_str += str(cycle)
        return repr_str


class CyclePathNotation:

    def __init__(self, dom, ran):
        self.cycle_path = to_cycle_path_notation(dom, ran)


if __name__ == '__main__':
    # x = CycleNotation([2, 6, 0, 4, 5, 3, 1, 7])
    # y = CycleNotation([1, 2, 6, 7, 4, 3, 0, 5])
    # print(x)
    # x = CyclePathNotation([1, 3, 4], [3, 2, 1])
    # x = CyclePathNotation([1, 2, 3, 4], [1, 3, 2, 4])
    # x = CyclePathNotation([1, 2], [1, 3])
    x = CyclePathNotation([1, 3], [3, 2])
    for item in x.cycle_path:
        print(item.value)
