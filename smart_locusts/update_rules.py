import numpy as np
from random import random as rnd


def pso_vanilla(fi1, fi2, vel, pos, best_pos, neigh_best):

    new_vel = []
    for idx in xrange(len(vel)):
        new_vel.append(vel[idx] + fi1 * rnd() * (best_pos[idx] - pos[idx]) +
                                  fi2 * rnd() * (neigh_best[idx] - pos[idx]))

    return np.array(new_vel)


# values for weight 0.4 .. 0.9
def inertia_weight(fi1, fi2, vel, pos, best_pos, neigh_best, weight=0.9):

    new_vel = []
    for idx in xrange(len(vel)):
        new_vel.append(weight * vel[idx] + fi1 * rnd() * (best_pos[idx] - pos[idx]) +
                                           fi2 * rnd() * (neigh_best[idx] - pos[idx]))

    return np.array(new_vel)


# fi1, fi2 = 2.05
# constriction factor 0.729
def constriction_factor(fi1, fi2, vel, pos, best_pos, neigh_best, K=0.729):

    phi = fi1 + fi2
    K   = 2 / np.abs(2 - phi - np.sqrt(phi ** 2 - 4 * phi))

    new_vel = []
    for idx in xrange(len(vel)):
        new_vel.append(K * (vel[idx] + fi1 * rnd() * (best_pos[idx] - pos[idx]) +
                                       fi2 * rnd() * (neigh_best[idx] - pos[idx])))

    return np.array(new_vel)
