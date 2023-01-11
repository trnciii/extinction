from matplotlib import pyplot as plt
import numpy as np
import _path as path
import itertools
import os

here = path.here()
sources = path.sources()

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


files = os.listdir(os.path.join(here, 'images'))

types = ['white', 'exp', 'pow', 'triangle', 'cos']
memories = [1, 100]

for a, t, m in itertools.product([0.5], types, memories):
	fig, ax = plt.subplots(1,1,constrained_layout=True, figsize=(2, 1.5))

	acf = path.load_npy(a, t, m, 'ac_input.npy')
	x = np.linspace(0, 1, acf.shape[0], endpoint=False)

	if t == 'white':
		if m == 100: continue

		ax.plot(x, acf)
		ax.get_xaxis().set_visible(False)
		ax.get_yaxis().set_visible(False)

		fig.savefig(f'acf/delta.jpg')

	else:
		if m == 1:
			n = acf.shape[0]//100
			right = 0.01
			col = 'lightgreen'

			ax.plot(x[:n], acf[:n])
		else:
			right = 1
			col = 'lightpink'

			ax.plot(x, acf)

		ax.get_yaxis().set_visible(False)
		ax.get_xaxis().set_ticks([0, right])
		ax.get_xticklabels()[-1].set_backgroundcolor(col)


		fig.savefig(f'acf/{rename_table.get(t,t)}_{memory_label[m]}.jpg')
