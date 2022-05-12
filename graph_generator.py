from geng import get_non_isomorphic_trees
from graph import Graph, BipartiteGraph


def generate_petersen():
    return [Graph([{2, 3, 5}, {3, 4, 6}, {0, 4, 7}, {0, 1, 8}, {1, 2, 9},
                  {0, 6, 9}, {1, 5, 7}, {2, 6, 8}, {3, 7, 9}, {4, 5, 8}])]


def generate_complete_graph():
    while True:
        try:
            no_nodes = int(input('Enter number of nodes: '))
            return [Graph([set(range(no_nodes)).difference({i}) for i in range(no_nodes)])]
        except ValueError:
            print('Please enter a number')


def generate_non_isomorphic_trees():
    while True:
        try:
            no_nodes = int(input('Enter number of nodes: '))
            trees = get_non_isomorphic_trees(no_nodes)
            print(f'Generated {str(len(trees))} non-isomorphic trees on {str(no_nodes)} vertices')
            return [Graph(item) for item in trees]
        except ValueError:
            print('Please enter a number')


def generate_test():
    return [{1, 3}, {0, 2, 3}, {1, 3}, {0, 1, 2}]


def generate_bipartite():
    m = n = None
    while True:
        try:
            if not m:
                m = int(input('Enter number of vertices in set U: '))
            if not n:
                n = int(input('Enter number of vertices in set V: '))
            return [BipartiteGraph([{*range(m, m + n)} for _ in range(m)] + [{*range(m)} for _ in range(n)], m, n)]
        except ValueError:
            print('Please enter a number')
    # return Graph([{3}, {4}, {3}, {0, 2}, {1}])


def user_entered_graph():
    try:
        no_nodes = int(input('Enter number of vertices: '))
        curr_vertex = 0
        neighbours = []
        while curr_vertex < no_nodes:
            try:
                user_input = input(f'Enter neighbours (separated by space) of vertex {curr_vertex}: ')
                adj_vertices = set(filter(lambda x: 0 <= x < no_nodes and x != curr_vertex, map(int, user_input.split(' '))))
                neighbours.append(adj_vertices)
                curr_vertex += 1
            except:
                print('Error')
        return [Graph(neighbours)]
    except ValueError:
        print('Please enter a number')
        user_entered_graph()
