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

#    edge = Edge(node1, node2, weight)
    graph[node1].append((node2, weight))
    graph[node2].append((node1, weight))


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


class State(object):

    infinite = 99999

    def __init__(self, cost=None, path=None):

        if not cost:
            self.cost = State.infinite
        else:
            self.cost = cost

        if not path:
            self.path = []
        else:
            self.path = path

    def __repr__(self):
        return "(cost: "   + str(self.cost) \
               + ", prev:" + str(self.path) + ")"

    def __cmp__(self, other):
        return self.cost < other.cost


def compute(states, graph, conf, last):

    if states[conf][last].cost == State.infinite:

        best = (State.infinite, [])

        for neigh, edge_cost in graph[last]:

            if conf & (1 << neigh):

                if neigh == 0 and conf != (1 << last) + 1:
                    pass

                choice = compute(states, graph, conf ^ (1 << last), neigh)
                choice = (choice.cost + edge_cost, choice.path + [last])

                if best[0] > choice[0]:
                    best = choice

        states[conf][last] = State(best[0], best[1])

    return states[conf][last]


def compute_tsp_pd(graph, max_weight):

    pp(graph)

    num_nodes = len(graph)
    State.infinite  = int(max_weight) * (num_nodes + 1)

    states    = [num_nodes * [State()] for _ in xrange(1 << num_nodes)]

    states[1][0].cost = 0
    states[1][0].path = [0]

    best = (State.infinite, [])

    for neigh, edge_cost in graph[0]:

        choice = compute(states, graph, (1 << num_nodes) - 1, neigh)
        choice = (choice.cost + edge_cost, choice.path)

        if best[0] > choice[0]:
            best = choice

    pp(best[1])
    best[1].append(0)
    pp(best)

    total_cost = 0
    prev = 0
    for node in best[1][1:]:
        for neigh, cost in graph[node]:
            if neigh == prev:
                total_cost += cost
        prev = node
    print total_cost



def main():

    graph = generate_graph(num_nodes=9, max_weight=10)
    compute_tsp_pd(graph, max_weight=10)

if __name__ == "__main__":
    main()



