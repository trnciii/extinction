import numpy as np
from mfgeo.noise import oneoverf, autoregressive
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


for n in [100, 1000, 10000]:
	rngs = [np.random.default_rng(seed=mu) for mu in range(1000)]

	# for beta in np.linspace(-0.99, 0.99, 3):
	beta = 0.99

	height = np.array([oneoverf.sequence(n, beta, rng) for rng in rngs])
	slope = np.diff(height)

	hist, bin_edges = np.histogram(slope, bins='auto', density=True)

	# print(f'{hist.size=}')
	# print(hist)
	# print(f'{bin_edges.size=}')
	# print(bin_edges)

	sample_slope = [-1, 0, 1]
	print(f'prob={probability(sample_slope, slope)}')

	print()

	plt.plot(bin_edges[:-1], hist, label=f'{beta=:2} {n=}')

	print(flush=True)

plt.legend()
plt.savefig(path.out(f'autoregressive_{beta:2}.png'))
plt.show()
