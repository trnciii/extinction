from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import os
import itertools
import _path as path
import json


def load_acf(a, t, m):
	with open(os.path.join(path.from_spec(a, t, m), 'meta.json')) as f:
		meta = json.load(f)
	return np.load(os.path.join(path.sources(), meta['id'], 'ac_generated.npy'))


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
types = ['white', 'cos', 'exp', 'pow', 'triangle']
memories = [1, 100]

width = len(types) * len(memories) - 1

for alpha, frame in itertools.product(alphas, frames):
	print(f'{alpha=}, {frame=}', flush=True)

	fig, axes = plt.subplots(
		width+1, width+1,
		figsize=(20,20),
		constrained_layout=True
	)
	# plt.subplots_adjust(wspace=0.05, hspace=0.05)


	type_memories = [
		(t, m) for m, t in itertools.product(memories, types)
		if not (t == 'white' and m == 100)
	]

	images = [
		np.asarray(Image.open(
			os.path.join(path.from_spec(alpha, t, m), f'frame_{frame}.png')
		).convert('L'))
		for t, m in type_memories
	]

	axes[0][0].imshow(images[0], cmap='gray')
	axes[0][0].axis('off')

	for i, (t, m) in enumerate(type_memories):
		acf = load_acf(alpha, t, m)
		n = m*150

		for a in [axes[0][1+i], axes[1+i][0]]:
			a.plot([0, n], [0, 0], color='black', linewidth=1)
			a.plot(range(n), acf[:n])
			a.text(
				0.95, 0.95,
				f'{rename_table.get(t,t)} ({memory_label[m]})',
				fontsize=16,
				transform = a.transAxes,
				horizontalalignment='right',
				verticalalignment='top'
			)

			# a.get_xaxis().set_visible(False)
			# a.get_yaxis().set_visible(False)
			a.axis('off')


	for _a, base in zip(axes[1:], images):
		for a, i in zip(_a[1:], images):
			a.imshow((i - base))
			a.axis('off')

	fig.savefig(f'compared/{alpha:3.2f}_{frame}.jpg')
