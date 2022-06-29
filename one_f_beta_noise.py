import numpy as np
from matplotlib import pyplot as plt

import figurateur


def one_f_beta(n, beta, rngs=[np.random.default_rng(seed=0)]):
	if type(rngs) is not list:
		rngs = [rngs]

	kmax = n//2
	seqs = len(rngs)


	f = np.tile( np.linspace(1, kmax, kmax), (seqs, 1) ) / (2*np.pi)
	C = 1/np.abs(f**beta)

	phase = np.array([2*np.pi*rng.random((kmax)) for rng in rngs])
	Cpos = C*np.exp(1j*phase)
	Cneg = np.flip(np.conj(Cpos), axis=1)

	C = np.concatenate((np.zeros((seqs, 1)), Cpos, Cneg), axis=1)
	noise = np.fft.ifft(C)

	return noise.real[:, :n]



if __name__ == '__main__':
	n = 1000
	beta = 1
	seqs = 100

	rngs = [np.random.default_rng(seed=i) for i in range(seqs)]
	noises = one_f_beta(n, beta, rngs)


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
	figurateur.show(figs, exclude={})
