import numpy as np

def sequence(n, k, rng):
	mean = lim_mean(k)

	ret = np.empty(n)
	ret[0] = rng.uniform() * 2*mean
	for i in range(n-1):
		ret[i+1] = k*ret[i] + rng.random()*np.sqrt(1-k*k)
	return ret

def lim_mean(k):
	return np.sqrt(1-k*k) / (2*(1-k))

def lim_std(k):
	return np.sqrt((1-k*k)/12)/(1-k)

def mean(x0, n, k):
	term1 = (x0 * (1-k**n)) / (n*(1-k))
	term2 = lim_mean(k)
	term3 = (np.sqrt(1-k*k) * (1-k**n)) / (2*n*(1-k)*(1-k))

	return term1 + term2 + term3, term2


if __name__ == '__main__':

	from matplotlib import pyplot as plt
	import figurateur

	n = 1000
	k = 0.99
	seqs = 100

	rngs = [np.random.default_rng(seed=i) for i in range(seqs)]
	noises = np.array([sequence(n, k, rng) for rng in rngs])

	print('shape', noises.shape)

	figs = {}

	figs['noises'], ax = plt.subplots(1, 2)

	figurateur.cloud(ax[0], np.linspace(1, n, n), noises)
	ax[0].set_position((0.1, 0.05, 0.7, 0.95))

	ax[1].hist(np.reshape(noises, (-1)), bins=20, orientation='horizontal')
	ax[1].set_position((0.8, 0.05, 0.2, 0.95))
	ax[1].get_xaxis().set_visible(False)
	ax[1].get_yaxis().set_visible(False)


	figs['powers'], ax = plt.subplots(1, 1)
	x, y = figurateur.power_spectra(noises)
	figurateur.cloud(ax, x, y)
	ax.set_yscale('log')
	ax.set_xscale('log')


	figurateur.save(figs)
	figurateur.show(figs, exclude={'noises'})
