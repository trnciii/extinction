import _path as path
import os, json

from matplotlib import pyplot as plt, gridspec
from matplotlib.patches import ConnectionPatch
from matplotlib.lines import Line2D

import itertools
import numpy as np
from mfgeo.distributions import beckmann


source = path.sources()

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

colors = {
	'measured': 'C0',
	'input': 'C1',
}

alphas = [0.1, 0.5, 0.9]
types = ['white', 'exp', 'pow', 'triangle', 'cos']
memories = [1, 100]

type_memories = [
	(t, m) for m, t in itertools.product(memories, types)
	if not (t == 'white' and m == 100)
]

for a, (t, m) in itertools.product(alphas[:1], type_memories):
	with open(os.path.join(path.from_spec(a, t, m), 'meta.json')) as f:
		meta = json.load(f)

	fig = plt.figure(figsize=(15,4), constrained_layout=True)

	grid = gridspec.GridSpec(
		4, 4, figure=fig,
		width_ratios=[0.05, 2.5, 1, 0.75],
		left=0.01, right=0.99,
		top=0.8,
		hspace=1
	)

	# height
	ax_h_full = fig.add_subplot(grid[:2, 1])
	ax_h_head = fig.add_subplot(grid[2:, 1])

	ax_h_full.set_title('height', fontsize=14)

	height = path.load_npy(a, t, m, 'height.npy')

	len_head = 1000
	ax_h_full.plot(range(height.shape[0]), height, linewidth=0.5, color=colors['measured'])
	ax_h_head.plot(range(len_head), height[:len_head], linewidth=1, color=colors['measured'])

	ax_h_head.get_xaxis().set_ticks([0, len_head])
	# ax_h_head.get_xticklabels()[-1].set_backgroundcolor('lightgreen')


	# acf
	ax_acf_full = fig.add_subplot(grid[:2, 2]) if m == 1 else fig.add_subplot(grid[:, 2])

	ax_acf_full.set_title('autocorrelation', fontsize=14)

	acf_ge = path.load_npy(a, t, m, 'ac_generated.npy')
	acf_in = path.load_npy(a, t, m, 'ac_input.npy')

	ax_acf_full.plot(np.linspace(0, 1, acf_ge.shape[0]), acf_ge, linewidth=1 , color=colors['measured'])
	ax_acf_full.plot(np.linspace(0, 0.5, acf_in.shape[0]), acf_in, color=colors['input'])

	if m == 1:
		ax_acf_head = fig.add_subplot(grid[2:, 2])

		len_head = acf_ge.shape[0]//200
		ax_acf_head.plot(np.linspace(0, 1, acf_ge.shape[0])[:len_head], acf_ge[:len_head], color=colors['measured'])
		ax_acf_head.plot(np.linspace(0, 0.5, acf_in.shape[0])[:len_head], acf_in[:len_head], linewidth=1, color=colors['input'])

		ax_acf_head.get_xaxis().set_ticks([0, 1/200])
		# ax_acf_head.get_xticklabels()[-1].set_backgroundcolor('lightgreen')


	# ndf
	ax_ndf = fig.add_subplot(grid[:2, 3])
	ax_ndf.set_title('slope distribution', fontsize=14)
	ax_ndf.get_yaxis().set_visible(False)

	hist, bins = np.histogram(np.diff(height), bins='auto', density=True)
	x = bins[:-1]

	ax_ndf.plot(x, hist, color=colors['measured'])

	angle = np.arctan(x)
	theo = beckmann.ndf(angle, a) * np.power(np.cos(angle), 4)
	theo /= np.sum(theo) * (bins[1] - bins[0])

	ax_ndf.plot(x, theo, label=f'{beckmann.name()} a={a}', linewidth=1, color=colors['input'])
	ax_ndf.text(
		0.95, 0.95, f'p={meta["shapiro"][1]:.2f}',
		fontsize=14,
		transform=ax_ndf.transAxes,
		verticalalignment='top',
		horizontalalignment='right'
	)


	# legend
	ax_legend = fig.add_subplot(grid[2:, 3])
	ax_legend.axis('off')
	ax_legend.legend(
		handles=[Line2D([0], [0], color=v, lw=4, label=k) for k,v in colors.items()],
		loc='center'
	)

	# name
	ax_name = fig.add_subplot(grid[1:3, 0])
	ax_name.axis('off')
	ax_name.text(
		0.5, 0.5, rename_table.get(t,t) + (f' ({memory_label[m]})' if t!='white' else ''),
		fontsize=20,
		transform=ax_name.transAxes,
		verticalalignment='center',
		horizontalalignment='center',
		rotation='vertical'
		)


	name = f'heights/{a:.2f}_{rename_table.get(t,t)}_{memory_label[m]}.png'
	fig.savefig(name)
	plt.close(fig)

	print(f'\\includegraphics[width=\\textwidth]{{thesis/{name}}}\\\\')
