__author__ = 'alexei'

import random
import numpy as np
from pprint import pprint as pp
import matplotlib.pyplot as plt

# class Edge(object):
#
#     def __init__(self, node1, node2, weight):
#
#         self.node1  = node1
#         self.node2  = node2
#         self.weight = weight
#
#     def __repr__(self):
#         return "(" + str(self.node1) + ","  + \
#                      str(self.node2) + ")[" + \
#                      str(self.weight) + "]"


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

                weight = random.randint(1, max_weight)
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

    infinite = 9999999

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


def check_path_cost(graph, path):
        total_cost = 0
        prev = path[0]
        for node in path[1:]:
            for neigh, cost in graph[node]:
                if neigh == prev:
                    total_cost += cost
            prev = node
        return total_cost


def compute_state(states, graph, conf, last):

    if states[conf][last].cost == State.infinite:

        best = (State.infinite, [])

        for neigh, edge_cost in graph[last]:

            if conf & (1 << neigh):

                if neigh == 0 and conf != (1 << last) + 1:
                    pass

                choice = compute_state(states, graph, conf ^ (1 << last), neigh)
                choice = (choice.cost + edge_cost, choice.path + [last])

                if best[0] > choice[0]:
                    best = choice

        states[conf][last] = State(best[0], best[1])

    return states[conf][last]


def compute_tsp_pd(graph, max_weight):

    # pp(graph)

    num_nodes = len(graph)
    # State.infinite  = int(max_weight) * (num_nodes + 1)

    states    = [num_nodes * [State()] for _ in xrange(1 << num_nodes)]

    states[1][0].cost = 0
    states[1][0].path = [0]

    best = (State.infinite, [])

    for neigh, edge_cost in graph[0]:

        choice = compute_state(states, graph, (1 << num_nodes) - 1, neigh)
        choice = (choice.cost + edge_cost, choice.path)

        if best[0] > choice[0]:
            best = choice

    best[1].append(0)

    # pp(best)
    # print check_path_cost(graph, best[1]) == best[0]

    return best


class ACOSettings():

    Q        = 5
    num_ants = 5
    NCmax    = 1000

    def __init__(self, alpha, beta, ro):

        self.alpha = alpha
        self.beta  = beta
        self.ro    = ro

    def __repr__(self):
        return "(" + str(self.alpha) + "," + str(self.beta) + "," + str(self.ro) + ")"

class Ant:

    def __init__(self, start, num_nodes):

        self.path   = [start]
        self.neighbourhood = [node for node in xrange(num_nodes) if node != start]

    def __repr__(self):
        return "(" + str(self.path) + "|" + str(self.neighbourhood) + ")"


class Edge:

    def __init__(self, dist, ph, h):

        self.ph   = ph
        self.h    = h
        self.dist = dist

    def __repr__(self):

        return "(dist: " + str(self.dist) + ", ph: " + \
               str(self.ph) + ", h: " + str(self.h) + ")"


def ants_tsp(graph, config, store_best_path=True):

    num_nodes = len(graph)

    # ants = [Ant(random.randint(0, num_nodes - 1), num_nodes)
    #         for _ in xrange(ACOSettings.num_ants)]
    ants = [Ant(i, num_nodes) for i in xrange(ACOSettings.num_ants)]

    state = {}
    all_edges = []

    for node in graph:
        for edge in graph[node]:

            state[(node, edge[0])] = Edge(edge[1],
                                          float(1) / num_nodes,
                                          float(ACOSettings.Q) / edge[1])
            state[(edge[0], node)] = state[(node, edge[0])]
            all_edges.append((node, edge[0]))

    if store_best_path:
        best_solution = (State.infinite, [])
    else:
        best_solution = State.infinite

    cycle = 0
    while cycle < ACOSettings.NCmax:

        steps = num_nodes # full graph

        while steps > 0:

            steps -= 1

            for ant in ants:
                if len(ant.neighbourhood) > 0:

                    # Analyze targets
                    node = ant.path[-1]

                    def compute_likelihood(i, j):
                        edge = state[(i, j)]
                        return (edge.ph ** config.alpha) * (edge.h ** config.beta)

                    likelihood = map(lambda neigh: compute_likelihood(node, neigh), ant.neighbourhood)
                    total      = sum(likelihood)
                    likelihood = map(lambda term: term / total, likelihood)
                    target = np.random.choice(ant.neighbourhood, 1, p=likelihood)

                    ant.path.append(target[0])
                    ant.neighbourhood.remove(target[0])
                else:
                    ant.path.append(ant.path[0])

        lengths = map(lambda ant: check_path_cost(graph, ant.path), ants)

        # print lengths

        # Store the best path as well
        if store_best_path:
            for idx in xrange(len(lengths)):
                if lengths[idx] < best_solution[0]:
                    best_solution = (lengths[idx], ants[idx].path)
        else:
            best_solution = min(best_solution, min(lengths))

        for i, j in all_edges:
            edge = state[(i, j)]
            edge.ph = max(float(1) / num_nodes, (1 - config.ro) * edge.ph)

        for ant_idx in xrange(len(ants)):

            ant = ants[ant_idx]
            Lk  = lengths[ant_idx]

            prev = ant.path[0]

            for node in ant.path[1:]:
                edge = state[(prev, node)]
                edge.ph += float(ACOSettings.Q) / Lk
                prev = node

            ants[ant_idx] = Ant(ant_idx, num_nodes)

        # for i, j in all_edges:
        #     print state[(i, j)].ph,
        # print
        # print

        cycle += 1

    return best_solution


def run_experiment(graph, config, num_attempts=10):

    result = [ants_tsp(graph, config) for _ in xrange(num_attempts)]
    return result


def run_tests(graph):

    tests = [ACOSettings(1.5, 1.2, 0.8)]
    results = map(lambda test: run_experiment(graph, test), tests)
    return zip(results, tests)


def test_9():

    graph   = generate_graph(num_nodes=9, density=1.0, max_weight=100)
    # optimum = compute_tsp_pd(graph, max_weight=10)
    # print optimum
    aoc_experiments = run_tests(graph)


    pp(aoc_experiments)


    # print "Optimum solution: ", optimum
    # pp(aoc_experiments)


def main():

    test_9()


if __name__ == "__main__":
    main()



