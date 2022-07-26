import extinction, numpy as np
from extinction.noise import oneoverf
from extinction import figurateur
from extinction.bruteforce import ggx_smith_g1

from matplotlib import pyplot as plt
import os
import time

n = 1000
k_or_beta = 0.0

rngs = [np.random.default_rng(seed=mu) for mu in range(1000)]
timeline = np.linspace(1, n, n)

sigmas = np.array([oneoverf.sequence(n, k_or_beta, rng) for rng in rngs])


steps = 1000
angle = np.linspace(1/steps, np.pi/2, steps)
smith = ggx_smith_g1(angle, 0.5)

slope = 1/np.tan(angle)
tested = extinction.visibility(sigmas, slope)


figs = {}

t0 = time.time()
figs['visibility'], ax = plt.subplots(1,1, tight_layout = True)
t1 = time.time()
print(t1-t0)

ax.plot(angle, tested)
ax.plot(angle, smith)


figs['noises'] = plt.figure()
figurateur.cloud_and_hist(figs['noises'], sigmas[:100])


figurateur.save(figs)
figurateur.show(figs)
