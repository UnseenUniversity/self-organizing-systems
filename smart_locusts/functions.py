import numpy as np


# [-100, 100]
def sphere(x):
    sphere.__count__ += 1
    return sum(x ** 2)


# [-10, 10]
def rosenbrok(x):
    rosenbrok.__count__ += 1
    ans = 0
    for k in xrange(len(x) - 1):
        ans += 100 * (x[k + 1] - x[k] ** 2) ** 2 + (x[k] - 1) ** 2
    return ans


# -5.12, 5.12
def rastrigin(x, a=10):
    rastrigin.__count__ += 1
    return a * len(x) + sum(x ** 2 - a * np.cos(2 * np.pi * x))


# -600, 600
def griewank(x):
    griewank.__count__ += 1
    return 1 / 4000 * sum(x ** 2) - np.prod(np.cos(x / np.sqrt(np.arange(len(x))[1:]))) + 1

sphere.__count__ = 0
rosenbrok.__count__ = 0
rastrigin.__count__ = 0
griewank.__count__ = 0