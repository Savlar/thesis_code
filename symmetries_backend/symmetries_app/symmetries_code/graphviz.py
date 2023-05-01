from pyvis.network import Network
import html


def create_graph_pyvis(data, labels=False):
    """
    create pyvis visualization for given graph
    Parameters
    ----------
    data - dictionary representing a graph, keys are vertices, associated values are neighbours
    labels - if vertices should be labeled or not
    Returns
    -------
    html file with graph visualization
    """
    nt = Network(height='300px')
    nodes = list(map(int, data.keys()))
    if labels:
        nt.add_nodes(nodes, size=[10 for _ in range(len(nodes))], color=['black' for _ in range(len(nodes))], label=list(map(str, nodes)))
    else:
        nt.add_nodes(nodes, size=[10 for _ in range(len(nodes))], color=['black' for _ in range(len(nodes))])
    for key in nodes:
        for neighbour in data[key]:
            nt.add_edge(key, neighbour, color='black', physics=False)

    # sets how vertices interact with each other when dragged and how edges are visualized
    nt.repulsion(0)
    nt.set_edge_smooth('continuous')

    encoded = html.escape(nt.generate_html())
    return encoded
