# Python program to print DFS
# traversal for complete graph
from collections import defaultdict
import networkx as nx
import networkx as nx1

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1


# This class represents a
# directed graph using adjacency
# list representation
# from main import resultValues


class Graph:

    # Constructor
    def __init__(self):

        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.count = 0;
        self.countList = []
        self.flag = False
        self.graph1 = defaultdict(list)
        self.key = ""
        self.map = dict()
        self.rfact = 0.0
        self.kfact = 0.0

    def setTrue(self):
        print("Ccc")
        self.flag = True

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # A function used by DFS
    def DFSUtil(self, v, visited):

        # Mark the current node as visited
        # and print it
        visited.add(v)
        print(v, end=' ')
        # Graph.addEdge1(self,)
        # Recur for all the vertices
        # adjacent to this vertex
        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited)

    def DFS(self, v):

        # Create a set to store visited vertices
        visited = set()
        # Call the recursive helper function
        # to print DFS traversal
        self.DFSUtil(v, visited)

    # Fetch values of R and K Factor
    def resultvalues(self):

        print("*** ")

    # return self.rfact, self.kfact

    def findRandKfactor(self, name):

        map = dict()

        for key, values in self.graph.items():
            # print('Key :: ', key)
            if (isinstance(values, list)):
                for value in values:
                    count = 0
                    # print("Val ",value)
                    if key not in self.map:
                        self.map[key] = 1
                    else:
                        self.map[key] = 1 + self.map[key]
            else:
                print("else Val ", value)

        rfac = 0;
        for x in self.map:
            rfac += self.map[x]
        rfac = 0;

        min = 0
        key = 0
        for x in self.map:
            rfac += self.map[x]

        # K factor
        for y in self.map:
            if min < self.map[y]:
                self.key = y
                min = self.map[y]

        print("Super Spreader " + name, self.key)
        print("Super Spreader " + name, self.key)

        print("K Factor for " + name, round(self.map[self.key] / len(self.map), 4))
        print("R Factor for " + name, round(rfac / len(self.map), 4))

    def vis(self):
        print("VIS")
        g = nx.DiGraph()
        g.add_nodes_from(self.graph.keys())

        for k, v in self.graph.items():
            g.add_edges_from(([(k, t) for t in v]))
        plt.clf()
        nx.draw_planar(g, with_labels=True, arrows=True)
        plt.savefig("RFactor.png")
        plt.clf()

        g1 = nx1.DiGraph()
        print("Self ", self.key)
        g1.add_node(self.key)
        for k, values in self.graph.items():
            for value in values:
                if k == self.key:
                    print(f'{k} - {value}')
                    g1.add_edge(k, value)

        plt1.clf()
        nx1.draw(g1, with_labels=True)
        plt1.savefig("KFactor.png")

        exit(0)
