from numpy import log, sqrt, array, linspace, exp
from scipy.optimize import leastsq
import math
from functools import partial

import csv


# data = [(1.6, -50),
#         (4.4, -55),
#         (8.5, -62),
#         (11.5, -66),
#         (15.2, -69),
#         ]

data = []
with open('../locdata/all_zviad.csv') as fin:
    reader = csv.reader(fin)
    for row in reader:
        data.append(tuple(float(x) for x in row))


WAVELENGTH = 0.125
C = 20.0*math.log(4.0*math.pi / WAVELENGTH, 10)

def get_implied_N(true_dist, level):
    level = -level
    return (level - C) / (10.0*math.log(true_dist, 10))

# def get_distance_from_level(level, n=2.1):
#     # from wikipedia
#     level = -level

#     r_in_meters = 10 ** ((level - C) / (10.0 * n))
#     r_in_meters = max(2.5, r_in_meters)
#     dist_in_meters = sqrt(r_in_meters ** 2 - 2.5 ** 2)
#     return dist_in_meters


# for sig in [-50, -55, -60, -65, -70]:
#     for N in [2.1, 2.33, 4, 5]:
#         dist = get_distance_from_level(sig, N)
#         print sig, N, dist, get_implied_N(dist, sig)


import matplotlib.pyplot as plt


Ns = [get_implied_N(*x) for x in data]
_, sigs = zip(*data)
plt.plot(sigs, Ns, 'bx')




def quad_eval(coeffs, x):
    a, b, c = coeffs
    return a * x ** 2 + b * x + c

def quad_residuals(coeffs, y_measured, x):
    err = y_measured - quad_eval(coeffs, x)
    return err


def exp_eval(coeffs, x):
    a, b, c = coeffs
    return exp(-a*x+b+50)+c

def exp_residuals(coeffs, y_measured, x):
    err = y_measured - exp_eval(coeffs, x)
    return err


def plot_function(fn, endpoints, fmt='ro'):
    Xs = linspace(*endpoints)
    reg_values = [fn(x) for x in Xs]
    plt.plot(Xs, reg_values, fmt)

# plsq = leastsq(quad_residuals, array([1,2,3]), args=(array(Ns), array(sigs)))
# plot_function(partial(quad_eval, plsq[0]), (min(sigs), max(sigs)))

# exp_lsq = leastsq(exp_residuals, array([1,2,3]), args=(array(Ns), array(sigs)))
# plot_function(partial(exp_eval, exp_lsq[0]), (min(sigs), max(sigs)), 'go')

# print plsq, exp_lsq

plt.savefig('test.png')
