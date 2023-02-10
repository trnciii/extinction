from matplotlib import pyplot as plt
import os, json, itertools
from PIL import Image
import _path as path
import numpy as np

rename_table = {
	'white': 'delta',
	'cos': 'wave',
	'pow': 'frac',
	'triangle': 'line',
}

memory_label = {
	1: 'short',
	100: 'long'
}

alphas = [0.1, 0.5, 0.9]
frames = list(range(4))
types = ['white', 'exp', 'pow', 'triangle', 'cos']
memories = [1, 100]


def plot_height(ax, a, t, m):
	h = path.load_npy(a, t, m, 'height.npy')

	left = h.shape[0]//2 - 250
	right = left + 500

	f = h[left:right]

	low = np.min(f) - 15*a
	high = np.max(f) + 15*a

	ax.plot(range(right-left), f, linewidth=1)
	ax.set_title(f'{rename_table.get(t,t)} height')

def plot_acf(ax, a, t, m):
	acf_in = path.load_npy(a, t, m, 'ac_input.npy')
	acf_ge = path.load_npy(a, t, m, 'ac_generated.npy')

	n = 1000
	ax.plot(range(n), acf_ge[:n])
	ax.plot(range(n), acf_in[:n])
	ax.set_title(f'{rename_table.get(t,t)} autocorrelation')


for a, t, m in itertools.product(alphas, types, [1]):
	if t == 'white' and m == 100:
		continue

	fig, axes = plt.subplots(2, 5, figsize=(18, 2*18/5), constrained_layout=True)
	(ax_height, *ax_images), (ax_acf, *_) = axes

	for ax in itertools.chain(*axes):
		ax.axis('off')


	for ax, f in zip(ax_images, range(4)):
		image = Image.open(os.path.join(path.from_spec(a, t, m), f'frame_{f}.png'))
		ax.imshow(image)

	plot_height(ax_height, a, t, m)
	plot_acf(ax_acf, a, t, m)


	fig.savefig(f'aligned/{a}_{t}_{m}.png')
	plt.close(fig)
