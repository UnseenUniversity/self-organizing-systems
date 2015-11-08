__author__ = 'alexei'

import random
from pprint import pprint as pp


class Edge(object):

    def __init__(self, node1, node2, weight):

        self.node1  = node1
        self.node2  = node2
        self.weight = weight

    def __repr__(self):
        return "(" + str(self.node1) + ","  + \
                     str(self.node2) + ")[" + \
                     str(self.weight) + "]"


def find_root(dset, node):

    if dset[node] == node:
        return node

    dset[node] = find_root(dset, dset[node])
    return dset[node]


def union(dset, set1, set2):

    root1 = find_root(dset, set1)
    root2 = find_root(dset, set2)

    if root1 != root2:
        dset[root1] = root2
        return True

    return False


def insert_edge(graph, node1, node2, weight):

    edge = Edge(node1, node2, weight)
    graph[node1].append(edge)
    graph[node2].append(edge)


def generate_graph(num_nodes=9, density=0.4, max_weight=10):

    graph = {}

    for idx in xrange(num_nodes):
        graph[idx] = []

    dset = [i for i in xrange(num_nodes)]

    num_sets = num_nodes

    for node_a in xrange(num_nodes):
        for node_b in xrange(node_a + 1, num_nodes):
            if random.random() < density:
                if union(dset, node_a, node_b):
                    num_sets -= 1

                weight = random.randint(0, max_weight)
                insert_edge(graph, node_a, node_b, weight)

    ndset = [find_root(dset, node) for node in xrange(len(dset))]

    while num_sets > 1:

        a, b = (random.randint(0, num_nodes - 1), random.randint(0, num_nodes - 1))

        if find_root(ndset, ndset[a]) != find_root(ndset, ndset[b]):
            weight = random.randint(0, max_weight)
            insert_edge(graph, a, b, weight)
            union(dset, a, b)
            num_sets -= 1

    dset = ndset
    return graph



def main():
    generate_graph()


if __name__ == "__main__":
    main()



