import numpy as np
from matplotlib import pyplot as plt
import os

import noise
import figurateur


n = 500
k = 0.9 # 0: whitenoise

rngs = [np.random.default_rng(seed=mu) for mu in range(50)]
timeline = np.linspace(1/n, 1, n)

sigmas = np.array([noise.noise(n, k, rng) for rng in rngs])
# sigmas = np.array([rng.random(n) for rng in rngs])
sigmas_averaged = np.cumsum(sigmas, axis=1)/timeline


figs = {}

figs['sigma'], ax = plt.subplots(1, 1)
figurateur.cloud(ax, sigmas)

figs['sigma_averaged'], ax = plt.subplots(1,1)
figurateur.cloud(ax, sigmas_averaged)


figurateur.save(figs)
figurateur.show(figs)
