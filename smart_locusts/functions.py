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


def schwefel(x):
    schwefel.__count__ += 1
    ans = 418.9829 * len(x) + np.sum(- x * np.sin(np.abs(x) ** 0.5))
    # print ans
    return ans

def ackley(x):
     ackley.__count__ += 1
     arg1 = -0.2 * np.sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))
     arg2 = 0.5 * (np.cos(2. * np.pi * x[0]) + np.cos(2. * np.pi * x[1]))
     return -20. * np.exp(arg1) - np.exp(arg2) + 20. + np.e


def xin_sheyang(x):
    xin_sheyang.__count__ += 1
    return np.sum(np.abs(x)) * np.exp(- np.sum(np.sin(x ** 2)))


def zakharov(x):
    zakharov.__count__ += 1
    term1 = 1 / 2 * np.sum(np.arange(len(x)) * x)
    return np.sum(x ** 2) + term1 ** 2 + term1 ** 4


def goldenstein_price(x):
    goldenstein_price.__count__ += 1
    x1 = x[0]
    x2 = x[1]
    return (1. + (x1 + x2 + 1.) ** 2 * (19. - 14. * x1 + 3. * x1 ** 2 - 14. * x2 + 6. * x1 * x2 + 3. * x2 ** 2)) * \
           (30. + (2.*x1 - 3. * x2) ** 2 * (18. - 32. * x1 + 12. * x1 ** 2 + 48. * x2 - 36. * x1 * x2 + 27. * x2**2))

sphere.__count__ = 0
rosenbrok.__count__ = 0
rastrigin.__count__ = 0
griewank.__count__ = 0
schwefel.__count__ = 0
ackley.__count__ = 0
xin_sheyang.__count__ = 0
zakharov.__count__ = 0
goldenstein_price.__count__ = 0
