import math
import time
from typing import Set, List
from geng import get_data

# https://math.stackexchange.com/a/2678754
# petersen = [{1, 2, 3, 4, 5}, {0}, {0}, {0}, {0}, {0}]
# petersen = [{1, 2, 3, 4}, {0}, {0}, {0}, {0, 5}, {4}]
# petersen = [{1, 2, 3}, {0}, {0}, {0, 4}, {3, 5}, {4}]
# petersen = [{1, 2, 3}, {0}, {0}, {0, 4, 5}, {3}, {3}]


def find_symmetries(visited: List[int], not_visited: Set[int], graph: List[Set[int]], all_symmetries, g):
    if len(not_visited) == 0:
        if graph == g:
            all_symmetries.append(list(visited))
    curr_vertex = len(g) - len(not_visited)
    for vertex in list(not_visited):
        not_visited.remove(vertex)
        visited.append(vertex)
        neighbours = g[curr_vertex].intersection(set(range(curr_vertex)))
        graph[vertex] = {visited[v] for v in neighbours}
        for v in neighbours:
            graph[visited[v]].add(vertex)
        if graph[curr_vertex] - g[curr_vertex] == set():
            find_symmetries(visited, not_visited, graph, all_symmetries, g)
        for v in neighbours:
            graph[visited[v]].remove(vertex)
        graph[vertex] = set()
        visited.pop()
        not_visited.add(vertex)


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

# g = [{1, 2, 3}, {0, 2, 3}, {0, 1, 3}, {0, 1, 2}]
# g = [{1, 3}, {0, 2, 3}, {1, 3}, {0, 1, 2}]
# a = []
# x = CycleNotation([2, 6, 0, 4, 5, 3, 1, 7])
# y = CycleNotation([1, 2, 6, 7, 4, 3, 0, 5])
# print(x * y)
