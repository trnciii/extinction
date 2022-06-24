import numpy as np
from matplotlib import pyplot as plt
import os

def cloud(ax, signals,
	line_top = ('salmon', 1, 2),
	line_cloud = ('#77777777', 0, 1) ):

	m, n = signals.shape

	timeline = np.linspace(1/n, 1, n)
	for i in range(m):
		c, order, w = line_top if i == 0 else line_cloud
		ax.plot(timeline, signals[i], color=c, linewidth=w, zorder=order)


def power_spectrum(ax, signals,
	line_top = ('salmon', 1, 2),
	line_cloud = ('#77777777', 0, 1)):

	m, n = signals.shape

	freq = np.fft.fftfreq(n, 1/n)
	power = np.abs(np.fft.fft(signals))**2

	freq = np.log(freq[:n//2])
	power = np.log(power[:, :n//2])

	for i in range(m):
		ax.plot(freq, power[i])


def save(figs, out_dir='./result/'):

	if (parent := os.path.dirname(out_dir)) != '':
		os.makedirs(parent, exist_ok=True)

	for k, v in figs.items():
		v.savefig(out_dir+'{}.png'.format(k), dpi=150)


def show(figs, exclude={}):
	for f in [v for k, v in figs.items() if k in exclude]:
		plt.close(f)

	plt.show()