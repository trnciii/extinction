import numpy as np
from matplotlib import pyplot as plt, gridspec
import itertools
from scipy.stats import norm
from scipy.signal.windows import hann

def decompose(h):
	f = np.fft.fft2(h)
	a = np.abs(f)
	return a, f/a

def decompose_filtered(h):
	m0, m1 = hann(h.shape[0]), hann(h.shape[1])
	mask = np.array([[m0[i]*m1[j] for i in range(h.shape[0])] for j in range(h.shape[1])])

	f = np.fft.fft2(h*mask)
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


def create_acf(n=2048):
	l = np.linspace(-1, 1, n, endpoint=False)
	x, y = np.meshgrid(l, l)

	d = 1 - np.sqrt(x*x + y*y) / 2**0.5

	z = np.exp(-10*d)
	print(z)

	return x, y, z


x, y, z = create_acf()

fig, ax = plt.subplots(1,1, constrained_layout=True)
ax.imshow(z)
ax.axis('off')
fig.savefig('result/acf.png')
plt.close(fig)


psd = np.fft.fft2(z)
amp = np.sqrt(psd.real)
print(np.allclose(psd.imag, 0))


fig, ax = plt.subplots(1,1, constrained_layout=True)
ax.imshow(amp.real)
ax.axis('off')
fig.savefig('result/amp.png')
plt.close(fig)



types = ['beckmann', 'ggx']
height = [np.load(f'../../data/{t}-sigma-0-25-0-25_2048-it-150.npy') for t in types]
fourier = [decompose(h) for h in height]

for t, h in zip(types, height):
	r, p = decompose_filtered(h)

	fig, (ar, ap) = plt.subplots(1, 2, figsize=(44, 22))

	ar.axis('off')
	ap.axis('off')

	ar.set_title(f'{t} amp')
	ap.set_title(f'{t} phase')

	ar.imshow(r.real, cmap='turbo')
	ap.imshow(p.real, cmap='turbo')

	fig.savefig(f'result/{t}.png')




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
		h = np.fft.ifft2(amp*p)
		h /= np.std(h)*0.25

		print(tr, tp, np.allclose(h.imag, 0))

		plot_height(axh, h.real)
		plot_slope_dist(axs, np.diff(h.real))


fig.savefig('result/swap.png')
