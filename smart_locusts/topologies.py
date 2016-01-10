import numpy as np


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
    topology = np.arange(num_particles).reshape(num_rows, num_cols)

    for i in xrange(num_rows):
        for j in xrange(num_cols):
            if topology[i][j] == idx:

                ans = [topology[i - 1][j], topology[i][j - 1]]

                if i + 1 >= num_rows:
                    ans.append(topology[-1][j])
                else:
                    ans.append(topology[i + 1][j])

                if j + 1 >= num_cols:
                    ans.append(topology[i][-1])
                else:
                    ans.append(topology[i][j + 1])

                return ans
