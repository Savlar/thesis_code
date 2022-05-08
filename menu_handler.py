import time

from graph_generator import *
from graphs import find_symmetries, CycleNotation

graph = []
notations = []


def print_menu():
    print('1 - generate petersen graph')
    print('2 - generate complete graph')
    print('3 - generate non-isomorphic trees')
    print('4 - generate bipartite graph')
    print('5 - Enter graph manually')
    print('6 - test')
    print('7 - find all symmetries')
    print('8 - check mult')


def menu():
    global graph, notations
    commands = {'1': generate_petersen, '2': generate_complete_graph, '3': generate_non_isomorphic_trees,
                '4': generate_bipartite, '5': user_entered_graph, '6': generate_test}
    while True:
        print_menu()
        user_input = input('Enter number or q for exit: ')
        if user_input == 'q':
            return
        if user_input in [str(i) for i in range(1, 7)]:
            graph = commands[user_input]()
            print(graph)
        if user_input in [str(i) for i in range(7, 8)]:
            if len(graph):
                for entry in graph:
                    # print(entry)
                    start = time.time()
                    all_symmetries = []
                    find_symmetries([], set(range(len(entry))), [set()] * len(entry), all_symmetries, entry)
                    notations = []
                    for sym in all_symmetries:
                        notations.append(CycleNotation(sym))
                        # print(notations[-1])
                    print(time.time() - start)
        if user_input == '8':
            res = []
            for i in range(len(notations)):
                for j in range(len(notations)):
                    r = notations[i] * notations[j]
                    print(notations[i], '*', notations[j], '=', r)
                    if r.cycle_notation not in res:
                        res.append(r.cycle_notation)
            print(len(res), len(res) == len(notations))


if __name__ == '__main__':
    menu()
    # for g in get_data(n):
    #     a = []
    #     total_aut += len(a)
    #     total_trees += math.factorial(n) / len(a)
