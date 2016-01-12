
import numpy as np
from pso import run_experiment
from random import random as rnd
from math import pi, cos, sin
from sklearn.cluster import k_means
from pprint import pprint as pp
from operator import itemgetter

def check_convergence(curr, prev):
    return set(curr.flat) == set(prev.flat)


def closest_cluster(x, clusters):
    return min([(cluster[0], np.linalg.norm(x - cluster[1])) for cluster in enumerate(clusters)],
               key=lambda e: e[1])


def kmeans(X, num_centroids, max_iter=2):

    X = np.array(X)
    current_centroids  = np.array(X[:num_centroids])
    previous_centroids = np.zeros((num_centroids, 2))

    data = range(num_centroids)

    iter = 0

    while not check_convergence(current_centroids, previous_centroids) and iter < max_iter:

        for idx in xrange(num_centroids):
            data[idx] = []

        # Assign points
        for x in X:
            centroid = closest_cluster(x, current_centroids)
            data[centroid[0]].append(x)

        previous_centroids = np.array(current_centroids)

        # recompute centroids
        for idx in xrange(num_centroids):
            current_centroids[idx] = np.mean(data[idx], 0)

        iter += 1

    # print "Kmeans iter: ", iter
    return current_centroids, data


def mosquito_init(sample_space, dim_count, num_particles, num_swarms=5):

    if num_swarms > num_particles:
        num_swarms = num_particles

    low_bound, high_bound = sample_space

    mosquitos = np.random.uniform(low_bound, high_bound, size=(num_particles, dim_count))
    leaders, swarms = kmeans(mosquitos, num_centroids=num_swarms)
    # leaders, swarm_idx = k_means(mosquitos, num_swarms)

    starvation = [0.0 for _ in xrange(num_swarms)]
    return [(np.inf, None) for _ in xrange(num_swarms)], swarms, starvation, num_particles


def random_sample(px, py, r, uniform=True):

    a = rnd()
    b = rnd()

    if uniform and b < a:
        a, b = b, a

    x = b * r * cos(2 * pi * a / b)
    y = b * r * sin(2 * pi * a / b)

    return x + px, y + py


def random_test(num_points=100):

    samples = [random_sample(0, 0, 1) for _ in xrange(num_points)]

    x = [sample[0] for sample in samples]
    y = [sample[1] for sample in samples]

    import matplotlib.pyplot as plt

    plt.plot(x, y, 'ro')
    plt.axis([-10, 10, -10, 10])
    plt.show()


def mosquito_update(config, fun, starvation_kt=1.0):

    fitness, sample_space, dim_count = fun
    leaders, swarms, starvation, num_particles = config

    global_best_value, global_best_pos = (np.inf, np.zeros(dim_count))

    # check collisions
    new_leaders, new_swarms, new_starvation = [], [], []

    for i in xrange(len(leaders)):
        leader_i = leaders[i]
        if leader_i[1] is not None:
            for j in xrange(len(leaders)):
                leader_j = leaders[j]
                if j <= i or leader_j[1] is None:
                    continue

                dist = np.linalg.norm(leader_i[1] - leader_j[1])

                if dist * 100 / (sample_space[1] - sample_space[0]) <= 1.0:
                    # collision
                    # print "Collision ", dist, leader_i, leader_j
                    if leaders[i][0] > leaders[j][0]:
                        leaders[i] = tuple(leaders[j])
                    leaders[j] = (np.inf, None)
                    swarms[i] += swarms[j]
                    starvation[i] = max(starvation[i], starvation[j])

        new_leaders.append(leader_i)
        new_swarms.append(swarms[i])
        new_starvation.append(starvation[i])

    leaders, swarms, starvation = new_leaders, new_swarms, new_starvation
    improve    = [None for _ in xrange(len(leaders))]

    new_swarms = []

    # Compute fitness
    for idx in xrange(len(swarms)):

        best_score, best_pos = leaders[idx]
        new_best_score, new_best_pos = best_score, best_pos

        new_swarm = []

        for particle in swarms[idx]:

            if np.array_equal(particle, new_best_pos):
                new_swarm.append((new_best_score, particle))
                # print "Particle on top of best swarm position"
                continue

            value = fitness(particle)
            if value < new_best_score:
                new_best_score = value
                new_best_pos = particle

            new_swarm.append((value, particle))

        if new_best_score < global_best_value:
            global_best_value, global_best_pos = new_best_score, new_best_pos

        new_swarms.append(new_swarm)

        if new_best_pos is None or np.array_equal(best_pos, new_best_pos):
            improvement = 0.0
        else:
            improvement = 100 - 100 * new_best_score / best_score

        improve[idx] = improvement
        leaders[idx] = new_best_score, new_best_pos

        # compute starvation
        perc_particles = float(len(swarms[idx])) / num_particles

        if improve[idx] > 10:
            starvation[idx] = 0.0
        else:
            # print improve[idx], starvation[idx], perc_particles, num_particles, len(swarms[idx])
            # print (1 / (improve[idx] + 0.0001)) * perc_particles
            starvation[idx] += starvation_kt * (1 / (improve[idx] + 0.0001)) * perc_particles
            if starvation[idx] > 1.0:
                starvation[idx] = 1.0
            # print starvation[idx]
            # exit(0)


    new_herd = 0
    res_leaders, res_swarms, res_starvation = [], [], []

    # print
    # pp(new_swarms)
    # print

    # migration
    for idx in xrange(len(new_swarms)):

        if starvation[idx] > 0.1:

            sample = rnd()
            if sample <= starvation[idx]:

                count = int(sample * 100 / len(new_swarms[idx]))

                if count < 1:
                    continue

                # print "Underperfoming particles ", count
                # extract least performing particles
                # def comp(x, y):
                #     print x, y
                #     print type(x[0]), type(x[1])
                #     if x[0] < y[0]:
                #         return 1
                #     return -1

                # print new_swarms[idx]
                # print type(new_swarms[idx][0]), new_swarms[idx][0][0], new_swarms[idx][0][1]
                # exit(0)
                particles = sorted(new_swarms[idx], cmp=lambda x, y: 1 if x[0] < y[0] else -1)
                # print particles
                # exit(0)
                # have them migrate to cleaner fields
                new_herd += count
                # new_herd.append(particles[:sample])
                new_swarms[idx] = particles[count:]

        if len(new_swarms[idx]) == 0:
            continue

        result_swarm = []

        # Move particles closer to target
        for score, pos in new_swarms[idx]:

            target_score, target_pos = leaders[idx]

            if np.array_equal(pos, target_pos):
                # seek a more nutritious target
                target_score, target_pos = np.inf, None
                for jdx in xrange(len(swarms)):
                    if idx == jdx:
                        continue
                    if leaders[jdx][0] < target_score:
                        target_score, target_pos = leaders[jdx]

                if target_pos is None:  # unique swarm
                    result_swarm.append(pos)
                    continue

            new_pos = pos + np.random.uniform(0.8, 1.2) * starvation[idx] * np.array(target_pos - pos)
            result_swarm.append(new_pos)

        res_swarms.append(result_swarm)
        res_leaders.append(leaders[idx])
        res_starvation.append(starvation[idx])

    # make a new herd
    if new_herd > 0:
        # print "New herd!"
        low_bound, high_bound = sample_space
        mosquitos = np.random.uniform(low_bound, high_bound, size=(new_herd, dim_count))
        res_swarms.append(mosquitos)
        res_leaders.append((np.inf, None))
        res_starvation.append(0.0)

    # print "Leaders: "
    # pp(res_leaders)
    #
    # print "\nSwarms"
    # pp(res_swarms)
    #
    # print "\nStarvation"
    # pp(res_starvation)
    #
    # print "\nParticle count"
    # pp(num_particles)

    # print
    # print

    ans = global_best_value, global_best_pos
    config = res_leaders, res_swarms, res_starvation, num_particles

    return ans, config


def run_mosquitos(fun, num_attempts=10, writer=None, dbg=True):

    fitness, sample_space, dim_count = fun

    rows = []

    for num_clusters in {1, 5, 10, 20}:

        init   = lambda num_particles: mosquito_init(sample_space, dim_count, num_particles, num_swarms=num_clusters)

        for kt in {0.2, 0.5, 1.0, 2.0, 3.0}:

            exp_best = (np.inf, np.zeros(dim_count), -1, np.inf)

            for attempt in xrange(num_attempts):
                fitness.__count__ = 0
                update = lambda c, f: mosquito_update(c, f, starvation_kt=kt)
                best, pos, step = run_experiment(fun, init, update)
                if best < exp_best[0] or \
                  (best == exp_best[0] and exp_best[3] > fitness.__count__):
                    exp_best = best, pos, step, fitness.__count__

            row = (fitness.__name__,
                   "",
                   str(num_clusters),
                   str(kt),
                   str(exp_best[0]),
                   str(np.abs(exp_best[0])),
                   str(exp_best[1]),
                   str(exp_best[2]),
                   str(exp_best[3]))

            rows.append(row)

    if writer is not None:
        rows = sorted(rows, cmp=lambda x, y: float(x[4]) < float(y[4]))
        for row in rows:
            writer.writerow(row)
        writer.writerow(())


    return exp_best
