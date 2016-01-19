import numpy as np
from random import random as rnd
from math import pi, cos, sin
from pprint import pprint as pp

def random_sample(px, py, r, uniform=False):

    a = rnd()
    b = rnd()

    if uniform and b < a:
        a, b = b, a

    x = b * r * cos(2 * pi * a / b)
    y = b * r * sin(2 * pi * a / b)

    return x + px, y + py


def abc_init(sample_space, dim_count, fitness, employed, num_particles):

    low_bound, high_bound = sample_space
    food_sources = np.random.uniform(low_bound, high_bound, size=(employed, dim_count))
    food_sources = [(food_source, fitness(food_source), 1) for food_source in food_sources]

    return num_particles, food_sources


def abc_update(config, fun):

    num_particles, fs = config[0]
    employed, onlookers, scouts = config[1]
    fitness, sample_space, dim_count = fun
    low_bound, high_bound = sample_space

    limit = onlookers * len(sample_space)  # as per original paper

    fs_neigh = [np.array(random_sample(pos[0], pos[1], r=0.5)) for pos, _, _ in fs]
    fs_neigh_fit = map(fitness, fs_neigh)

    fs = [fs[i] if fs[i][1] < fs_neigh_fit[i] else (fs_neigh[i], fs_neigh_fit[i], 1)
          for i in xrange(employed)]

    fs_values = [1 / (1 + value) for _, value, _ in fs]
    fs_prob_sum = sum(fs_values)
    fs_prob = [value / fs_prob_sum for value in fs_values]

    fs_onlookers = np.random.choice(xrange(employed), size=onlookers, p=fs_prob)
    fs = [(pos, value, iter + 1) for pos, value, iter in fs]

    for onlooker in fs_onlookers:

        pos, value, iter = fs[onlooker]
        npos = np.array(random_sample(pos[0], pos[1], r=0.5))
        nfit = fitness(npos)

        if nfit < value:
            fs[onlooker] = npos, nfit, 1

    best_ans = np.inf, None
    for idx in xrange(len(fs)):
        if best_ans[0] > fs[idx][1]:
            best_ans = fs[idx][1], fs[idx][0]

    fs_valid = filter(lambda k: k[2] < limit, fs)
    num_scouts = len(fs) - len(fs_valid) + scouts

    new_fs = np.random.uniform(low_bound, high_bound, size=(num_scouts, dim_count))
    new_fs = [(pos, fitness(pos), 1) for pos in new_fs]

    fs = fs_valid + new_fs
    fs = sorted(fs, key=lambda elem: elem[1])[:employed]

    config = (num_particles, fs), (employed, onlookers, scouts)

    return best_ans, config


def run_experiment(fun, init, update, max_iter=500, num_particles=20, bee_prop=(50, 50, 1)):

    fitness, _, dim_count = fun
    employed, onlookers, scouts = bee_prop

    employed  = employed * num_particles / 100
    onlookers = onlookers * num_particles / 100

    config = init(num_particles, employed), (employed, onlookers, scouts)
    best_ans = (np.inf, np.zeros(dim_count), -1)

    for step in xrange(max_iter):
        ans, config = update(config, fun)
        if ans[0] < best_ans[0]:
            best_ans = (ans[0], ans[1], step)

    return best_ans


def run_bees(fun, num_attempts=10, writer=None, dbg=True):

    fitness, sample_space, dim_count = fun

    rows = []

    init   = lambda num_particles, employed_bees: abc_init(sample_space, dim_count, fitness,
                                                           employed_bees, num_particles)

    for bee_proportions in [(50, 50, 1), (25, 75, 1), (75, 25, 1)]:

        employed, onlookers, scouts = bee_proportions

        exp_best = (np.inf, np.zeros(dim_count), -1, np.inf)
        for attempt in xrange(num_attempts):
            fitness.__count__ = 0
            update = lambda c, f: abc_update(c, f)
            best, pos, step = run_experiment(fun, init, update, bee_prop=bee_proportions)
            if best < exp_best[0] or (best == exp_best[0] and exp_best[3] > fitness.__count__):
                    exp_best = best, pos, step, fitness.__count__

        row = (fitness.__name__,
                   str(employed),
                   str(onlookers),
                   str(scouts),
                   str(exp_best[0]),
                   str(np.abs(exp_best[0])),
                   str(exp_best[1]),
                   str(exp_best[2]),
                   str(exp_best[3]))

        rows.append(row)

    if writer is not None:

        rows = sorted(rows, cmp=lambda x, y: -1 if float(x[4]) < float(y[4]) else 1)
        for row in rows:
            writer.writerow(row)
        writer.writerow(())

    return None




























