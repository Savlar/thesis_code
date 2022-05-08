from geng import get_data


def generate_petersen():
    return [[{2, 3, 5}, {3, 4, 6}, {0, 4, 7}, {0, 1, 8}, {1, 2, 9},
            {0, 6, 9}, {1, 5, 7}, {2, 6, 8}, {3, 7, 9}, {4, 5, 8}]]


def generate_complete_graph():
    while True:
        try:
            no_nodes = int(input('Enter number of nodes: '))
            return [[set(range(no_nodes)).difference({i}) for i in range(no_nodes)]]
        except ValueError:
            print('Please enter a number')


def generate_non_isomorphic_trees():
    while True:
        try:
            no_nodes = int(input('Enter number of nodes: '))
            return get_data(no_nodes)
        except ValueError:
            print('Please enter a number')


def generate_test():
    return [[{1, 3}, {0, 2, 3}, {1, 3}, {0, 1, 2}]]


def generate_bipartite():
    m = 3
    n = 2
    # return [[{*range(m, m + n)} for _ in range(m)] + [{*range(m)} for _ in range(n)]]
    return [[{3}, {4}, {3}, {0, 2}, {1}]]


def user_entered_graph():
    user_input = input('Enter graph').replace(' ', '')
    entries = filter(lambda x: len(x), user_input.split(';'))
    for item in entries:
        vertex, adjacent = item.split('-')
        print(vertex, adjacent)
