import numpy as np


def acf(x, window=None):
	if window == None: window = len(x)//2
	npcorr = np.correlate(x, x[:window], mode='valid')
	return npcorr/npcorr[0]


def main():
	from matplotlib import pyplot as plt
	import sys

	from noise import autoregressive
	from noise import oneoverf

	import figurateur


	figs = {}

	for generator in [autoregressive, oneoverf]:

		n = 1000
		num_k = 7

		figs[generator.name], ax = plt.subplots(num_k, 2, tight_layout=True, figsize=(19.2, 10.8))

		rng = np.random.default_rng(seed=1234)

		for k, (ax_nosie, ax_ac) in zip(np.linspace(-1, 1, num_k), ax):
			noise = generator.sequence(n, k, rng)
			ac = acf(noise)

			ax_nosie.plot(range(n), noise, linewidth=0.6)
			ax_nosie.set_title('k = {:.3}'.format(k), loc='left')
			ax_ac.plot(range(ac.shape[0]), ac, linewidth=0.6)


	figurateur.save(figs, prefix='autocorr_')

	if not '-b' in sys.argv:
		figurateur.show(figs)


if __name__ == '__main__':
	main()