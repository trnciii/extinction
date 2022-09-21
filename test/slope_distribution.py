import numpy as np
from mfgeo.noise import oneoverf
from mfgeo import figurateur
from matplotlib import pyplot as plt
import path


def probability(x, sample):
	hist, bin_edges = np.histogram(sample, bins='auto', density=True)
	index = np.digitize(x, bin_edges)
	return np.where((0<index) * (index<hist.size),
		np.take(hist, index-1, mode='clip'),
		0
	)


n = 1000

rngs = [np.random.default_rng(seed=mu) for mu in range(1000)]

for beta in range(-1, 2):

	height = np.array([oneoverf.sequence(n, beta, rng) for rng in rngs])
	slope = np.diff(height)

	hist, bin_edges = np.histogram(slope, bins='auto', density=True)


	print(f'{hist.size=}')
	print(hist)
	print(f'{bin_edges.size=}')
	print(bin_edges)

	sample_slope = [-1, 0, 1]
	print(f'prob={probability(sample_slope, slope)}')

	print()

	plt.plot(bin_edges[:-1], hist, label=f'{beta=:2}')

print(flush=True)

plt.legend()
plt.savefig(path.out('sampled_slope_distribution.png'))
plt.show()
