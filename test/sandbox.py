from mfgeo import noise, figurateur
import numpy as np
from matplotlib import pyplot as plt

rngs = [np.random.default_rng(seed=mu) for mu in range(10)]

for noisetype in [noise.oneoverf]:
	n_range = [10**e for e in range(3, 8)]
	fig, axes = plt.subplots(len(n_range), 1, figsize=(20, 10), constrained_layout=True)

	for n, ax in zip(n_range, axes):
		height = np.array([noisetype.sequence(n, 1, rng) for rng in rngs])

		size = 500
		sliced = height[:, :size]*n/1000
		figurateur.cloud(ax, np.linspace(1, size, size), sliced)

plt.savefig('result/sadbox.png')
plt.show()

