
import numpy as np
from random import random as rnd

# [-100, 100]
def sphere(x):
    return sum(x ** 2)

# [-10, 10]
def rosenbrok(x):

    ans = 0
    for k in xrange(len(x) - 1):
        ans += 100 * (x[k + 1] - x[k] ** 2) ** 2 + (x[k] - 1) ** 2
    return ans

# -5.12, 5.12
def rastrigin(x, a=10):
    return a * len(x) + sum(x ** 2 - a * np.cos(2 * np.pi * x))

# -600, 600
def griewank(x):
    return 1 / 4000 * sum(x ** 2) - np.prod(np.cos(x / np.sqrt(np.arange(len(x))[1:]))) + 1


# fi1, fi2 = 2.05
# constriction factor 0.729

#
# class Particle(object):
#
#     def __init__(self, position, velocity):
#
#         self.neighbours = []
#         self.position = position
#         self.velocity = velocity
#         self.fitness  = None


def main(num_particles, part_vel, fi1, fi2, part_pos, part_best_pos, part_gbest):

#    print "Old velocities ", part_vel

    new_vel = []
    for idx in xrange(num_particles):

        # print part_pos[idx], part_vel[idx]
        # print part_best_pos[idx], part_best_pos[idx] - part_pos[idx]
        # print part_gbest[idx], part_gbest[idx] - part_pos[idx]
        # print

        new_vel.append(part_vel[idx] + fi1 * rnd() * (part_best_pos[idx] - part_pos[idx]) +
                                       fi2 * rnd() * (part_gbest[idx] - part_pos[idx]))


    # print "New velocities ", new_vel

    return np.array(new_vel)


# values for weight 0.4 .. 0.9
def inertia_weight(num_particles, part_vel, fi1, fi2, part_pos, part_best_pos, part_gbest, weight=0.9):

    new_vel = []
    for idx in xrange(num_particles):
        new_vel.append(weight * part_vel[idx] + fi1 * rnd() * (part_best_pos[idx] - part_pos[idx]) +
                                                fi2 * rnd() * (part_gbest[idx] - part_pos[idx]))

    return np.array(new_vel)


def constriction_factor(num_particles, part_vel, fi1, fi2, part_pos, part_best_pos, part_gbest, K=0.729):

    phi = fi1 + fi2
    K   = 2 / np.abs(2 - phi - np.sqrt(phi ** 2) - 4 * phi)

    new_vel = []
    for idx in xrange(num_particles):
        new_vel.append(K * (part_vel[idx] + fi1 * rnd() * (part_best_pos[idx] - part_pos[idx]) +
                                            fi2 * rnd() * (part_gbest[idx] - part_pos[idx])))

    return np.array(new_vel)


def full_topology(idx, num_particles):
    return range(0, idx) + range(idx + 1, num_particles)


def ring_topology(idx, num_particles):

    if idx == 0:
        return [-1, 1]
    elif idx == num_particles - 1:
        return [idx - 1, 0]
    else:
        return [idx - 1, idx + 1]


def neumann_topology(idx, num_particles):

    num_rows = int(np.sqrt(num_particles))
    num_cols = num_particles / num_rows

    # print num_rows, num_cols, num_particles
    topology = np.arange(num_particles).reshape(num_rows, num_cols)

    # print topology

    for i in xrange(num_rows):
        for j in xrange(num_cols):
            if topology[i][j] == idx:

                ans = [topology[i-1][j], topology[i][j-1]]

                # print i, j, idx

                if i + 1 >= num_rows:
                    ans.append(topology[-1][j])
                else:
                    ans.append(topology[i+1][j])

                if j + 1 >= num_cols:
                    ans.append(topology[i][-1])
                else:
                    ans.append(topology[i][j+1])

                return ans


def run_experiment(fun, topology, fi1, fi2, pso_update, max_iter=500, num_particles=20, ):

    sample_space = fun[1]
    fitness_fun  = fun[0]

    part_pos = np.random.uniform(sample_space[0], sample_space[1], [num_particles, 2])
    part_vel = np.zeros([num_particles, 2])
    part_fit = [np.inf for _ in xrange(num_particles)]

    part_best_pos = part_pos
    part_best_fit = part_fit

    part_gbest = [np.inf for _ in xrange(num_particles)]

    part_neigh = {}
    for idx in xrange(num_particles):
        part_neigh[idx] = topology(idx, num_particles)

    best_ans = (np.inf, np.zeros(2), -1)

    for iter in xrange(max_iter):

        # print
        # print
        # print "Iter ", iter
        # print "part_pos", part_pos

        # evaluate particle fitness
        part_fit  = [fitness_fun(pos) for pos in part_pos]

        # print "fit: ", part_fit

        # update personal best
        for idx in xrange(num_particles):
            if part_best_fit[idx] > part_fit[idx]:
                part_best_pos[idx] = part_pos[idx]
                part_best_fit[idx] = part_fit[idx]

            if part_fit[idx] < best_ans[0]:
                best_ans = (part_fit[idx], part_pos[idx], iter)

        # update global best
        for idx in xrange(num_particles):
            social_best = np.inf
            for neigh in part_neigh[idx]:
                if part_best_fit[neigh] < social_best:
                    social_best     = part_best_fit[neigh]
                    part_gbest[idx] = part_best_pos[neigh]

        # update particle velocity
        part_vel = pso_update(num_particles, part_vel, fi1, fi2, part_pos, part_best_pos, part_gbest)
        # print "velocity: ", part_vel

        # if iter >= 2:
        #     exit(0)
        # part_pos += part_vel

        # part_vel = np.clip(part_vel, sample_space[0], sample_space[1])
        part_pos = np.clip(part_pos + part_vel, sample_space[0], sample_space[1])

        # print best_ans

    return best_ans


def run_simulation(f, writer, num_attempts=10):

    print "Run simulation for function ", f[0].__name__

    topology   = [full_topology, ring_topology, neumann_topology]
    fi_choices = [(0.01, 0.01), (1, 2), (2.05, 2.05), (2, 1)]
    pso_type   = [main, inertia_weight, constriction_factor]

    for pso in pso_type:
        for top in topology:
            for fi in fi_choices:

                exp_best = (np.inf, np.zeros(2), -1)
                for attempt in xrange(num_attempts):
                    best, pos, iter = run_experiment(f, top, fi[0], fi[1], pso)
                    if best < exp_best[0]:
                        exp_best = best, pos, iter

                writer.writerow((f[0].__name__, top.__name__, pso.__name__, str(fi), str(exp_best[0]), str(np.abs(exp_best[0])), str(exp_best[1]), str(exp_best[2])))

                print "Experiment using " + top.__name__ + ", phi=" + str(fi) + " and update rule " + pso.__name__
                print "Best result : score ", exp_best[0], "| pos ", exp_best[1], "| ", exp_best[2]
                print
    print
    print

def solve_assignment():

    import csv

    with open("results.csv", "w") as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_ALL)

        writer.writerow(("Function", "Topology", "PSO", "Phi", "Score", "Error", "Position", "Iter"))

        functions = [(griewank, (-600, 600)),
                     (sphere, (-100, 100)),
                     (rosenbrok, (-10, 10)),
                     (rastrigin, (-5.12, 5.12)),
                     ]

        for fun in functions:
            run_simulation(fun, writer)

solve_assignment()
