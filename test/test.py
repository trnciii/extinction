import extinction, numpy as np
from extinction.noise import oneoverf
from extinction import figurateur

from matplotlib import pyplot as plt
import os
import time

n = 1000
k_or_beta = 0

rngs = [np.random.default_rng(seed=mu) for mu in range(1000)]
timeline = np.linspace(1, n, n)

sigmas = np.array([oneoverf.sequence(n, k_or_beta, rng) for rng in rngs])



slope_linspace = np.linspace(0, 1, 1000)

visibility = extinction.visibility(sigmas, slope_linspace)


figs = {}

t0 = time.time()
figs['visibility'], ax = plt.subplots(1,1, tight_layout = True)
t1 = time.time()
print(t1-t0)

ax.plot(slope_linspace, visibility)


figs['noises'] = figurateur.cloud_and_hist(sigmas)


figurateur.save(figs)
figurateur.show(figs)
