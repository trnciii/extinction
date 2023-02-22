from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import os, itertools, _path as path, json


a = {
	'alpha': 0.50,
	'type': 'white',
	'memory': '1'
}

b = {
	'alpha': 0.50,
	'type': 'cos',
	'memory': '1'
}

h_a = path.load_npy(a['alpha'], a['type'], a['memory'], 'height.npy')
h_b = path.load_npy(b['alpha'], b['type'], b['memory'], 'height.npy')


for i in map(lambda x:f'{x:02}', range(61)):
	i_a = np.array(Image.open(f'teaser/{a["alpha"]:.2f}_{a["type"]}_{a["memory"]}/{i}.png')).astype(np.float32)/255
	i_b = np.array(Image.open(f'teaser/{b["alpha"]:.2f}_{b["type"]}_{b["memory"]}/{i}.png')).astype(np.float32)/255
	diff = i_a-i_b
	diff[:,:,3] = 1


	fig, ax = plt.subplots(2, 3, figsize=(15,6), constrained_layout=True, height_ratios=[1,5])

	for _a in itertools.chain(*ax):
		_a.axis('off')

	n = 500
	ax[0][0].plot(range(n), h_a[:n])
	ax[0][1].plot(range(n), h_b[:n])

	ax[0][2].text(0.5, 0.5, 'x5 diff',
		fontsize=32,
		verticalalignment='center',
		horizontalalignment='center',
	)

	ax[1][0].imshow(i_a)
	ax[1][1].imshow(i_b)
	ax[1][2].imshow(5*diff)

	fig.savefig(f'teaser/diff/{i}.png')
	plt.close(fig)
