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


figs = {}

cols = 5

for generator in [oneoverf, autoregressive]:
	figs[generator.name], axes = plt.subplots(2, cols, constrained_layout=True, figsize=(20, 5))
	for c, beta in enumerate(np.linspace(-0.99, 0.99, cols)):
		ax_h, ax_s = axes[:, c]
		ax_h.set_title(f'height {beta:.2f}')
		ax_s.set_title(f'slope  {beta:.2f}')

		rngs = [np.random.default_rng(seed=mu) for mu in range(1000)]

		_n = [10**e for e in range(2,5)]
		height_o = np.array([generator.sequence(max(_n), beta, rng, silent=True) for rng in rngs])

		for n in _n:
			height = height_o[:n]
			slope = np.diff(height)

			hist_h, bin_edges_h = np.histogram(height, bins='auto', density=True)
			hist_s, bin_edges_s = np.histogram(slope, bins='auto', density=True)

			# print(f'{hist.size=}')
			# print(hist)
			# print(f'{bin_edges.size=}')
			# print(bin_edges)

			# sample_slope = [-1, 0, 1]
			# print(f'prob={probability(sample_slope, slope)}')
			# print(end='',flush=True)

			ax_h.plot(bin_edges_h[:-1], hist_h, label=f'{n=}')
			ax_s.plot(bin_edges_s[:-1], hist_s, label=f'{n=}')

			ax_h.legend()
			ax_s.legend()

figurateur.save(figs, out_dir=path.out())
figurateur.show(figs)
