from mfgeo import noise, figurateur
from mfgeo.distributions import ggx
import numpy as np
from matplotlib import pyplot as plt
import os, path

# outdir = path.out()

rng = np.random.default_rng(seed=10)

alpha = 0.4

size = 1000000
u1 = rng.uniform(size=(size))

# sampled = np.arctan(alpha * np.sqrt(u1) / np.sqrt(1 - u1))
sampled = alpha*(2*u1 - 1)/(2*np.sqrt(-u1*u1 + u1))

hist, bins = np.histogram(sampled, bins='auto', density=True)
x = np.arctan(bins)
# hist = hist / np.sum(np.diff(x)*hist)
plt.plot(x[:-1], hist, label='sampled')

theta = np.linspace(-np.pi/2, np.pi/2, bins.shape[0]-1)
D = ggx.ndf(theta, alpha)
plt.plot(theta, D, label='analytical')

print(np.sum(D*(theta[1]-theta[0])))

ratio = hist/D
print(ratio)
plt.plot(theta, ratio, label='ratio')

print(flush=True)
plt.legend()
plt.show()