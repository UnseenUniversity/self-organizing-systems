from update_rules import *
from topologies import *


def pso_init(sample_space, dim_count, num_particles, topology):

    low_bound, high_bound = sample_space

    pos = np.random.uniform(low_bound, high_bound, size=(num_particles, dim_count))
    vel = np.zeros((num_particles, dim_count))
    fit = [np.inf for _ in xrange(num_particles)]

    neigh = {}
    for idx in xrange(num_particles):
        neigh[idx] = topology(idx, num_particles)

    neigh_best = [np.inf for _ in xrange(num_particles)]

    best_pos, best_fit = pos, fit

    return pos, vel, fit, neigh, best_pos, best_fit, neigh_best


def pso_update(config, fun, vel_update):

    fitness, sample_space, dim_count = fun
    pos, vel, fit, neighbourhood, best_pos, best_fit, neigh_best = config

    # evaluate particle fitness
    fit = [fitness(p) for p in pos]

    best_ans = (np.inf, None)

    # update personal best
    for idx in xrange(len(pos)):

        if fit[idx] < best_fit[idx]:
            best_fit[idx] = fit[idx]
            best_pos[idx] = pos[idx]

            if fit[idx] < best_ans[0]:
                best_ans = (fit[idx], pos[idx])

    # update global best
    for idx in xrange(len(pos)):
        social_best = np.inf

        for neigh in neighbourhood[idx]:
            if best_fit[neigh] < social_best:
                social_best     = best_fit[neigh]
                neigh_best[idx] = best_pos[neigh]

    vel = vel_update(vel, pos, best_pos, neigh_best)
    pos = np.clip(pos + vel, sample_space[0], sample_space[1])

    return best_ans, (pos, vel, fit, neighbourhood, best_pos, best_fit, neigh_best)


def run_experiment(fun, init, update, max_iter=500, num_particles=20):

    fitness, _, dim_count = fun
    config   = init(num_particles)
    best_ans = (np.inf, np.zeros(dim_count), -1)

    for step in xrange(max_iter):
        ans, config = update(config, fun)
        if ans[0] < best_ans[0]:
            best_ans = (ans[0], ans[1], step)

    return best_ans


def run_pso(fun, num_attempts=1, writer=None, dbg=False):

    fitness, sample_space, dim_count = fun
    topology   = [full_topology, ring_topology, neumann_topology]
    fi_choices = [(0.01, 0.01), (1, 2), (2.05, 2.05), (2, 1)]
    pso_type   = [pso_vanilla, inertia_weight, constriction_factor]

    rows = []

    for pso in pso_type:
        for top in topology:

            init = lambda num_particles: pso_init(sample_space, dim_count, num_particles, top)

            for fi in fi_choices:

                vel_update = lambda vel, pos, lbest, gbest : pso(fi[0], fi[1], vel, pos, lbest, gbest)
                update = lambda config, fun: pso_update(config, fun, vel_update)

                exp_best = (np.inf, np.zeros(dim_count), -1, np.inf)
                for attempt in xrange(num_attempts):
                    fitness.__count__ = 0
                    best, pos, step = run_experiment(fun, init, update)
                    if best < exp_best[0] or \
                       (best == exp_best[0] and exp_best[3] > fitness.__count__):
                        exp_best = best, pos, step, fitness.__count__

                row = (fitness.__name__,
                       top.__name__,
                       pso.__name__,
                       str(fi),
                       str(exp_best[0]),
                       str(np.abs(exp_best[0])),
                       str(exp_best[1]),
                       str(exp_best[2]),
                       str(exp_best[3]))

                if writer is not None:
                    rows.append(row)

                if dbg:
                    print "Experiment using " + top.__name__ + ", phi=" + str(fi) + " and update rule " + pso.__name__
                    print "Best result : score ", exp_best[0], "| pos ", exp_best[1], "| ", exp_best[2]
                    print

    if writer is not None:

        rows = sorted(rows, cmp=lambda x, y: float(x[4]) < float(y[4]))
        for row in rows:
            writer.writerow(row)
        writer.writerow(())
