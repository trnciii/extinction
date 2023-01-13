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
types = ['white', 'triangle', 'exp', 'cos']
memories = [1, 100]

width = len(types) * len(memories) - 1
dimi = width+4, width+1
dimf = dimi[1]*1.5, (dimi[0]-1)*1.5

for alpha, frame in itertools.product(alphas, frames):
	print(f'{alpha=}, {frame=}', flush=True)

	fig, axes = plt.subplots(*dimi, figsize=dimf, constrained_layout=True,
		gridspec_kw={'height_ratios': [1]*(width+2) + [0.2]+[1]}
	)

	for a in itertools.chain(*axes):
		a.axis('off')


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


	for i, (t, m) in enumerate(type_memories):
		f = load_npy(alpha, t, m, 'height.npy')

		left = f.shape[0]//2 - 200
		right = left + 400
		low = np.min(f[left:right]) - 15*alpha
		high = np.max(f[left:right]) + 15*alpha

		for a in [axes[1][1+i], axes[2+i][0]]:
			a.plot(range(right-left), f[left:right], linewidth=1)
			a.text(
				0.05, 0.95,
				f'{rename_table.get(t,t)}' + (f'({memory_label[m]})' if t!='white' else ''),
				fontsize=12,
				transform = a.transAxes,
				horizontalalignment='left',
				verticalalignment='top'
			)

			a.yaxis.set_ticks([low, high])

	for a, i in zip(axes[0][1:], images):
		a.imshow(i, cmap='gray')


	a = axes[-1][0]
	a.scatter(range(20), np.random.random(20), s=5)
	a.text(0.05, 0.95, 'smith', fontsize=12, transform=a.transAxes, horizontalalignment='left', verticalalignment='top')
	a.yaxis.set_ticks([-1, 2])
	image_smith = np.array(Image.open(os.path.join(path.from_spec(alpha, 'smith', 1), f'frame_{frame}.png')).convert('F'))
	image_smith /= np.max(image_smith)

	for a in axes[-1]:
		s = a.spines['top']
		s.set_position('zero')
		s.set_color('red')
		s.set_linewidth(3)

	for a in axes[-2]:
		a.axhline(y=0.5, linewidth=4, color='grey')


	for _a, base in list(zip(axes[2:-2], images)) + [(axes[-1], image_smith)]:
		for a, i in zip(_a[1:], images):

			if base is i: continue

			diff = i - base
			a.imshow(diff, norm=Normalize(vmin=-0.05, vmax=0.05), cmap='twilight_shifted')

	fig.savefig(f'compared/{alpha:3.2f}_{frame}.jpg')
