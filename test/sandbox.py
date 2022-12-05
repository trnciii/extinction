from mfgeo import noise, figurateur
from mfgeo.distributions import ggx
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
import os, path

# outdir = path.out()

f, ax = plt.subplots(2,1,figsize=(40,15))

rng = np.random.default_rng(seed=10)

alpha = 0.4

size = 100000000
u1 = rng.uniform(size=(size))

sampled = 0.37*(2*u1 - 1)/(2*np.sqrt(-u1*u1 + u1))
theta = np.arctan(sampled)

ax[1].plot(range(sampled.shape[0]), np.cumsum(sampled))

hist, bins = np.histogram(theta, bins='auto', density=True)
ax[0].plot(bins[:-1], hist, label='sampled')


theta = np.linspace(-np.pi/2, np.pi/2, 200)
D = ggx.ndf(theta, alpha)
ax[0].plot(theta, D/1.45, label='analytical')


print(flush=True)
ax[0].legend()
plt.show()