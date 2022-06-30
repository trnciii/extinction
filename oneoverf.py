import numpy as np
from matplotlib import pyplot as plt

import figurateur


def sequence(n, beta, rng):
	kmax = n//2

	f = np.linspace(1, kmax, kmax)/(2*np.pi)
	C = 1/np.abs(f**beta)

	phase = np.array(2*np.pi*rng.random(kmax))
	Cpos = C*np.exp(1j*phase)
	Cneg = np.flip(np.conj(Cpos))

	C = np.concatenate(([0], Cpos, Cneg))
	noise = np.fft.ifft(C)

	return noise.real[:n]



if __name__ == '__main__':
	n = 1000
	beta = 1
	seqs = 100

	rngs = [np.random.default_rng(seed=i) for i in range(seqs)]
	noises = np.array([sequence(n, beta, rng) for rng in rngs])


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
