from mfgeo import noise, figurateur
from mfgeo.distributions import ggx
import numpy as np
from matplotlib import pyplot as plt
import os, path

# outdir = path.out()


def sample_ggx_ndf(u, alpha):
	assert u.ndim == 2
	assert u.shape[1] == 2

	phi = 2*np.pi * u[:,1]
	a2 = alpha*alpha
	r2 = a2 * u[:,0] / (1 + u[:,0]*(a2-1))
	r = np.sqrt(r2)

	ret = np.empty((u.shape[0], 3))
	ret[:,0] = r*np.cos(phi)
	ret[:,1] = r*np.sin(phi)
	ret[:,2] = np.sqrt(1-r2)
	return ret


rng = np.random.default_rng(seed=10)

alpha = 0.4

size = 10000
u2 = rng.uniform(size=(size, 2))
u1 = rng.uniform(size=(size))
sampled = np.arctan(alpha * np.sqrt(u1) / np.sqrt(1 - u1))
hist, bins = np.histogram(sampled, bins='auto', density=True)
x = bins[1:]
plt.plot(x, hist/np.cos(x))
plt.plot(x, np.cumsum(hist) * np.diff(bins))

theta = np.linspace(0, np.pi/2, 100)
D = ggx.ndf(theta, alpha)
plt.plot(theta, D)

plt.show()