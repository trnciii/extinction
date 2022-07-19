if __name__ == '__main__':
	import numpy as np
	from matplotlib import pyplot as plt
	import os

	from noise import autoregressive, oneoverf
	import figurateur

	noise = autoregressive
	noise = oneoverf


	n = 500
	k_or_beta = 0

	rngs = [np.random.default_rng(seed=mu) for mu in range(50)]
	timeline = np.linspace(1, n, n)

	sigmas = np.array([noise.sequence(n, k_or_beta, rng) for rng in rngs])
	sigmas_averaged = np.cumsum(sigmas, axis=1)/timeline


	figs = {}

	figs.update(figurateur.inspect_noise(sigmas))

	figs['sigma_averaged'], ax = plt.subplots(1,1)
	figurateur.cloud(ax, timeline, sigmas_averaged)
	ax.set_xscale('log')


	pre = 'ar_' if noise is autoregressive else '1_f_'
	figurateur.save(figs, prefix=pre)
	figurateur.show(figs, exclude={'powers'})
