import numpy as np
from matplotlib import pyplot as plt
import os

def cloud(ax, x, signals,
	line_top = ('salmon', 1, 2),
	line_cloud = ('#77777777', 0, 1) ):

	m = signals.shape[0]

	for i in range(m):
		c, order, w = line_top if i == 0 else line_cloud
		ax.plot(x, signals[i], color=c, linewidth=w, zorder=order)


def power_spectra(signals):
	n = signals.shape[1]

	freq = np.fft.fftfreq(n)
	power = np.abs(np.fft.fft(signals))**2

	return freq[1:n//2], power[:, 1:n//2]


def save(figs, out_dir='./result/', prefix='', suffix=''):

	if (parent := os.path.dirname(out_dir)) != '':
		os.makedirs(parent, exist_ok=True)

	for k, v in figs.items():
		filename = out_dir + prefix + k + suffix + '.png'
		v.savefig(filename, dpi=150)


def show(figs, exclude={}):
	for f in [v for k, v in figs.items() if k in exclude]:
		plt.close(f)

	plt.show()


def inspect_noise(noises):
	n = noises.shape[1]

	figs = {}

	figs['noises'], ax = plt.subplots(1, 2)

	cloud(ax[0], np.linspace(1, n, n), noises)
	ax[0].set_position((0.1, 0.05, 0.7, 0.95))

	ax[1].hist(np.reshape(noises, (-1)), bins=20, orientation='horizontal')
	ax[1].set_position((0.8, 0.05, 0.2, 0.95))
	ax[1].get_xaxis().set_visible(False)
	ax[1].get_yaxis().set_visible(False)


	figs['powers'], ax = plt.subplots(1, 1)
	x, y = power_spectra(noises)
	cloud(ax, x, y)
	ax.set_yscale('log')
	ax.set_xscale('log')

	return figs