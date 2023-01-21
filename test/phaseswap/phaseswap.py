import numpy as np
from matplotlib import pyplot as plt, gridspec
import itertools
from scipy.stats import norm


def decompose(h):
	f = np.fft.fft2(h)
	a = np.abs(f)
	return a, f/a

def text(ax, s):
	ax.text(0.5, 0.5, s,
		fontsize=25,
		transform = ax.transAxes,
		horizontalalignment='center',
		verticalalignment='center'
	)
	ax.axis('off')

def plot_height(ax, h):
	x, y = np.meshgrid(range(h.shape[0]), range(h.shape[1]))

	ax.view_init(elev=45, azim=15)
	ax.plot_surface(x, y, h, cmap='turbo')
	ax.axis('off')


def plot_slope_dist(ax, s):
	hist, bins = np.histogram(s, bins='auto', density=True)
	ax.plot(bins[:-1], hist)
	ax.plot(bins, norm.pdf(bins, scale=np.std(s)),
		label='norm',
		color='grey',
		linestyle='dashed',
		linewidth=4
	)
	ax.set_xlim([-1.5, 1.5])
	ax.set_ylim([0, 3.5])


types = ['beckmann', 'ggx']
height = [np.load(f'../../data/{t}-sigma-0-25-0-25_2048-it-150.npy') for t in types]
fourier = [decompose(h) for h in height]

fig = plt.figure(figsize=(20,10), constrained_layout=True)
grid = gridspec.GridSpec(len(types)+1, 2*len(types)+1, figure=fig,
	width_ratios = [1] + [3]*2*len(types),
	height_ratios = [1] + [5]*len(types),
	hspace = 0.2
)

text(fig.add_subplot(grid[1, 0]), 'Beckmann amp')
text(fig.add_subplot(grid[2, 0]), 'Trowbridge-Reitz amp')
text(fig.add_subplot(grid[0, 1:3]), 'Beckmann phase')
text(fig.add_subplot(grid[0, 3:5]), 'Trowbridge-Reitz phase')

axes = [[
	(
		fig.add_subplot(grid[1+i, 1+2*j], projection='3d'),
		fig.add_subplot(grid[1+i, 2+2*j])
	)
	for j in range(len(types))] for i in range(len(types))
]

for _a, tr, (r, _) in zip(axes, types, fourier):
	for (axh, axs), tp, (_, p) in zip(_a, types, fourier):
		h = np.fft.ifft2(r*p)

		print(tr, tp, np.allclose(h.imag, 0))

		plot_height(axh, h.real)
		plot_slope_dist(axs, np.diff(h.real))


fig.savefig('swap.png')
