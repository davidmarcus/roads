import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import numpy

X = Y = 4
def graph_length(G):
    """The length of all roads in a graph"""
    return sum(data['weight'] for node0, node1, data in G.edges_iter(data=True))

def make_weighted(G):
    """The length of all roads in a graph"""
    for edge in G.edges():
        G.remove_edge(*edge)
        G.add_edge(*edge, weight=math.sqrt((edge[0][0] - edge[1][0])**2 + (edge[0][1] - edge[1][1])**2))

def grid_graph(x, y):
    """A graph representing a rectangular street grid with width x and height y"""
    G = nx.grid_2d_graph(x, y)
    make_weighted(G)
    return G

def mean_path_length(G):
    """The mean path length between nodes in the graph"""
    return numpy.mean([nx.dijkstra_path_length(G, node0, node1) for node0 in G.nodes() for node1 in G.nodes() if isinstance(node0[0], int) and isinstance(node1[0], int)])

def show(G):
    """Draw the graph"""
    nx.draw_networkx(G, pos={n: n for n in G.nodes_iter()}, with_labels=False, node_size=20)
    plt.show()

def get_removal_target(G):
    """Find an edge to drop"""
    results = []
    for node0, node1, data in G.edges(data=True):
        edge = node0, node1
        G.remove_edge(*edge)
        if nx.is_connected(G):
            results.append((mean_path_length(G), edge))
        G.add_edge(*edge, weight=data['weight'])
    weight, edge = sorted(results)[0]
    print 'DROPPING %s, mean_path_length: %s' % (edge, weight)
    return edge

def get_addition_target(G):
    """Find an edge to add"""
    results = []
    for i in xrange(1, X):
        for j in xrange(Y):
            node = (i, j)
            for edge in [(node, (i - 1, j - 1)), (node, (i - 1, j)), (node, (i - 1, j + 1))]:
                if 0 <= edge[-1][-1] < Y and not G.has_edge(*edge):
                    G_copy = G.copy()
                    add_edge(G_copy, edge)
                    results.append((mean_path_length(G_copy), edge))
    weight, edge = sorted(results)[0]
    print 'ADDING %s, mean_path_length=%s' % (edge, weight)
    return edge
    
def add_edge(G, edge):
    """Add an edge to the graph G"""
    ((x0, y0), (x1, y1)) = edge
    if x0 == x1 or y0 == y1 or not G.has_edge((x0, y1), (x1, y0)):
        G.add_edge(*edge, weight=math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2))
    else:
        G.remove_edge((x0, y1), (x1, y0))
        midpoint = (numpy.mean([x0, x1]), numpy.mean([y0, y1]))
        for x in [x0, x1]:
            for y in [y0, y1]:
                G.add_edge(midpoint, (x, y), weight=math.sqrt(2.0) / 2)

def iterate(G, target=graph_length(grid_graph(X, Y))):
    """Add or remove an edge, based on whether the graph has capacity to add an edge and stay within the target length"""
    if graph_length(G) <= target - math.sqrt(2):
        edge = get_addition_target(G)
        add_edge(G, edge)
    else:
        edge = get_removal_target(G)
        G.remove_edge(*edge)
