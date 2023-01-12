from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from PIL import Image
import numpy as np
import os
import itertools
import _path as path
import json


def load_npy(a, t, m, filename):
	with open(os.path.join(path.from_spec(a, t, m), 'meta.json')) as f:
		meta = json.load(f)
	return np.load(os.path.join(path.sources(), meta['id'], filename))


src_path = os.path.join(path.here(), 'images')

to_filepath = lambda a,f,t,m:os.path.join(src_path, f'{a:3.2f}_{t}_{m}/frame_{f}.png')


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


files = os.listdir(src_path)

alphas = [0.1, 0.5, 0.9]
frames = list(range(4))
types = ['white', 'exp', 'pow', 'triangle', 'cos']
memories = [1, 100]

width = len(types) * len(memories) - 1

for alpha, frame in itertools.product(alphas, frames):
	print(f'{alpha=}, {frame=}', flush=True)

	fig, axes = plt.subplots(
		width+1, width+1,
		figsize=(15, 15),
		constrained_layout=True
	)
	# plt.subplots_adjust(wspace=0.05, hspace=0.05)


	type_memories = [
		(t, m) for m, t in itertools.product(memories, types)
		if not (t == 'white' and m == 100)
	]

	images = [
		np.array(Image.open(
			os.path.join(path.from_spec(alpha, t, m), f'frame_{frame}.png')
		).convert('F'))
		for t, m in type_memories
	]

	for i in images:
		i /= np.max(i)


	axes[0][0].imshow(images[0], cmap='gray')
	axes[0][0].axis('off')

	for i, (t, m) in enumerate(type_memories):
		f = load_npy(alpha, t, m, 'height.npy')

		left = f.shape[0]//2 - 200
		right = left + 400
		low = np.min(f[left:right]) - 15*alpha
		high = np.max(f[left:right]) + 15*alpha

		for a in [axes[0][1+i], axes[1+i][0]]:
			a.plot(range(right-left), f[left:right], linewidth=1)
			a.text(
				0.05, 0.95,
				f'{rename_table.get(t,t)} ({memory_label[m]})' if t!='white' else 'delta',
				fontsize=12,
				transform = a.transAxes,
				horizontalalignment='left',
				verticalalignment='top'
			)

			a.yaxis.set_ticks([low, high])
			a.axis('off')


	for _a, base in zip(axes[1:], images):
		for a, i in zip(_a[1:], images):
			a.axis('off')

			if base is i: continue

			diff = i - base
			a.imshow(diff, norm=Normalize(vmin=-0.05, vmax=0.05), cmap='seismic')

	fig.savefig(f'compared/{alpha:3.2f}_{frame}.jpg')
