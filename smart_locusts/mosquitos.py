
import numpy as np
from pso import run_experiment
from random import random as rnd
from math import pi, cos, sin


def mosquito_init(sample_space, dim_count, num_particles, num_swarms=0.5):

    low_bound, high_bound = sample_space
    num_swarms = int(num_swarms * num_particles)

    pos        = np.random.uniform(low_bound, high_bound, size=(num_swarms, dim_count))
    fit        = [np.inf for _ in xrange(num_swarms)]
    count      = [num_particles / num_swarms for _ in xrange(num_swarms)]
    starvation = [1.0 for _ in xrange(num_swarms)]

    return pos, fit, count, starvation, num_particles


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


# random_test()
# exit(0)
def mosquito_update(config, fun, radius_kt=1.0, starvation_kt=1.0):

    fitness, sample_space, dim_count = fun

    pos, fit, count, starvation, num_particles = config

    sample_size = sample_space[1] - sample_space[0]
    radius = [radius_kt * (count[idx] * 100 / num_particles) * starvation[idx] * sample_size for idx in xrange(len(pos))]
    radius = np.clip(radius, 0.0001 * sample_size, 0.1 * sample_size)

    # compute fitness for each swarm
    # based on starvation

    best_fit = []
    best_target = []

    for idx in xrange(len(pos)):

        px, py = pos[idx]
        r      = radius[idx]
        perc_mosquitos = count[idx] * 100 / num_particles

        starved = False
        if starvation[idx] > 0.5:
            starved = True

        swarm_fitness = fit[idx]
        target        = pos[idx]

        for _ in xrange(count[idx]):

            sample = random_sample(px, py, r, starved)
            value  = fitness(np.array(sample))

            if value < swarm_fitness:
                swarm_fitness = value
                target        = sample

        if fit[idx] == np.inf:
            starvation[idx] = 0.0
        else:
            improvement = (fit[idx] - swarm_fitness)

            if improvement > 0:
                improvement *= 100 / fit[idx]

                if improvement >= 0.1 * fit[idx]:
                    starvation[idx] = 0.0
                else:
                    starvation[idx] = min(starvation[idx] + starvation_kt * perc_mosquitos * (1 / improvement), 1.0)
            else:
                starvation[idx] = min(starvation[idx] + 0.5 * perc_mosquitos)

        best_fit.append(swarm_fitness)
        best_target.append(target)

    for idx in xrange(len(pos)):


        
        print best_fit[idx], best_target[idx], starvation[idx], pos[idx]

    exit(0)


def run_mosquitos(fun, num_attempts=1, writer=None, dbg=True):

    fitness, sample_space, dim_count = fun

    init   = lambda num_particles: mosquito_init(sample_space, dim_count, num_particles)
    update = mosquito_update

    exp_best = (np.inf, np.zeros(dim_count), -1)

    for attempt in xrange(num_attempts):
        best, pos, step = run_experiment(fun, init, update)
        if best < exp_best[0]:
            exp_best = best, pos, step

    return exp_best
