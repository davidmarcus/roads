import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import numpy

X = Y = 10 # default dimensions for the road graph

class RoadGraph(nx.Graph):

    # construction
    @classmethod
    def from_graph(cls, graph):
        """Create a RoadGraph instance of any graph of type nx.Graph"""
        G = cls()
        G.add_edges_from(graph.edges())
        G.make_weighted()
        return G

    def make_weighted(self):
        """Weight every edge of the graph by calculating the length of each edge"""
        for edge in self.edges():
            self.remove_edge(*edge)
            self.add_edge(*edge)
            
    @classmethod
    def grid_graph(cls, x, y):
        """A graph representing a rectangular street grid with width x and height y"""
        G = nx.grid_2d_graph(x, y)
        return cls.from_graph(G)

    # visualization
    def show(self, highlight=set()):
        """Draw the graph"""
        nx.draw_networkx(self, pos={n: n for n in self.nodes_iter()}, node_color=['b' if node in highlight else 'r' for node in self.nodes_iter()], with_labels=False, node_size=20)
        plt.show()

    def show_isochrone(self, node, distance):
        self.show(highlight=self.isochrone_nodes(node, distance))

    # metrics
    @property
    def length(self):
        """The length of all roads in a graph"""
        return sum(data['weight'] for node0, node1, data in self.edges_iter(data=True))

    @property
    def mean_path_length(self):
        """The mean path length between nodes in the graph"""
        return numpy.mean([nx.dijkstra_path_length(self, node0, node1) for node0 in self.nodes() for node1 in self.nodes() if isinstance(node0[0], int) and isinstance(node1[0], int)])
        
    def isochrone_nodes(self, node, distance):
        return set(k for k, v in nx.shortest_path_length(self, node, weight='weight').items() if v <= distance)

    # optimization
    def get_removal_target(self):
        """Find an edge to drop"""
        results = []
        for node0, node1, data in self.edges(data=True):
            edge = node0, node1
            self.remove_edge(*edge)
            if nx.is_connected(self):
                results.append((self.mean_path_length, edge))
            self.add_edge(*edge)
        weight, edge = sorted(results)[0]
        print 'DROPPING %s, mean_path_length: %s' % (edge, weight)
        return edge

    def get_addition_target(self):
        """Find an edge to add"""
        results = []
        for i in xrange(1, X):
            for j in xrange(Y):
                node = (i, j)
                for edge in [(node, (i - 1, j - 1)), (node, (i - 1, j)), (node, (i - 1, j + 1))]:
                    if 0 <= edge[-1][-1] < Y and not self.has_edge(*edge):
                        G_copy = self.__class__.from_graph(self)
                        G_copy.add_edge(*edge)
                        results.append((G_copy.mean_path_length, edge))
        weight, edge = sorted(results)[0]
        print 'ADDING %s, mean_path_length=%s' % (edge, weight)
        return edge

    def add_edge(self, node0, node1):
        """Add an edge to the graph G"""
        (x0, y0), (x1, y1) = node0, node1
        if x0 == x1 or y0 == y1 or not self.has_edge((x0, y1), (x1, y0)):
            super(RoadGraph, self).add_edge(node0, node1, weight=math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2))
        else:
            self.remove_edge((x0, y1), (x1, y0))
            midpoint = (numpy.mean([x0, x1]), numpy.mean([y0, y1]))
            for x in [x0, x1]:
                for y in [y0, y1]:
                    super(RoadGraph, self).add_edge(midpoint, (x, y), weight=math.sqrt(2.0) / 2)

    def iterate(self, target=(X * (Y - 1) + Y * (X - 1))):
        """Add or remove an edge, based on whether the graph has capacity to add an edge and stay within the target length"""
        if self.length <= target - math.sqrt(2):
            edge = self.get_addition_target()
            self.add_edge(*edge)
        else:
            edge = self.get_removal_target()
            self.remove_edge(*edge)


