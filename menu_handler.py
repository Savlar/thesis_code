from graph_generator import *
from graphs import find_symmetries
from cycle_notation import CycleNotation


structure = []


def print_menu():
    print('1 - generate petersen graph')
    print('2 - generate complete graph')
    print('3 - generate non-isomorphic trees')
    print('4 - generate bipartite graph')
    print('5 - enter graph manually')
    print('6 - find all symmetries')
    print('7 - check group and get group properties')
    print('8 - print symmetries in cycle notation')


def print_structure():
    if isinstance(structure, Graph):
        print(structure)
    else:
        print(*structure, sep='\n')


def print_cycle():
    if not len(structure):
        print('\nCurrently unavailable\n')
        return
    for item in structure:
        print(item)
        for sym in item.aut_group:
            print(sym)


def get_symmetries():
    global structure
    for graph in structure:
        all_symmetries = []
        find_symmetries([], set(range(len(graph))), [set()] * len(graph), all_symmetries, graph)
        if isinstance(graph, BipartiteGraph):
            all_symmetries = filter(lambda x: sum(x[:graph.m]) == sum(range(graph.m)), all_symmetries)
        for sym in all_symmetries:
            graph.aut_group.append(CycleNotation(sym))


def menu():
    global structure
    commands = {'1': generate_petersen, '2': generate_complete_graph, '3': generate_non_isomorphic_trees,
                '4': generate_bipartite, '5': user_entered_graph, '6': get_symmetries, '8': print_cycle}
    while True:
        print_menu()
        user_input = input('Enter number or q for exit: ')
        if user_input == 'q':
            return
        if user_input in map(str, range(1, 6)):
            structure = commands[user_input]()
            print_structure()
        if user_input in ['6', '8']:
            commands[user_input]()
        # if user_input == '8':
        #     res = []
        #     for i in range(len(notations)):
        #         for j in range(len(notations)):
        #             r = notations[i] * notations[j]
        #             print(notations[i], '*', notations[j], '=', r)
        #             if r.cycle_notation not in res:
        #                 res.append(r.cycle_notation)
        #     print(len(res), len(res) == len(notations))


if __name__ == '__main__':
    menu()
