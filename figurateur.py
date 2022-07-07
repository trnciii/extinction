import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
import os
import warnings

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
	power = np.abs(np.fft.fft(signals))

	return freq[1:n//2], power[:, 1:n//2]


def psd_line(freq, power):
	x = np.log(freq)
	y = np.log(power)

	A = np.vstack([x, np.ones(len(x))]).T

	return np.linalg.lstsq(A, y, rcond=None)[0]


def save(figs, out_dir='./result/', prefix='', suffix=''):

	if (parent := os.path.dirname(out_dir)) != '':
		os.makedirs(parent, exist_ok=True)

	for k, v in figs.items():
		k = k.replace('/','')
		filename = out_dir + prefix + k + suffix + '.png'
		v.savefig(filename, dpi=150)


def show(figs, exclude={}):
	exclude = set(exclude)
	diff = exclude.difference(figs.keys())
	if len(diff):
		message = 'fig key(s) {} not found in {}.'.format(diff, set(figs.keys()))
		warnings.warn(message, stacklevel=2)

	for k, v  in figs.items():
		if k in exclude:
			plt.close(v)
		else:
			v.canvas.set_window_title(k)

	print("", end='', flush=True)
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


	figs['powers'] , ax = plt.subplots(1, 1, tight_layout=True)

	# ax.set_title('psd (numpy)')
	# x, y = power_spectra(noises)

	ax.set_title('psd (scipy)')
	x, y = signal.welch(noises)
	x, y = x[1:], np.sqrt(y[:, 1:])

	cloud(ax, x, y)
	ax.set_yscale('log')
	ax.set_xscale('log')


	m, c = psd_line(x, np.mean(y, axis=0))
	print(m, c)

	slopelabel = 'slope = {:.4}'.format(m)
	ax.plot(x, np.exp(m*np.log(x) + c), label=slopelabel, color='lightblue')
	ax.legend()

	return figs