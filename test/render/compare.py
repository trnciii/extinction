from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import os
import itertools
import _path as path

src_path = os.path.join(path.here(), 'images')

to_filepath = lambda a,f,t,m:os.path.join(src_path, f'{a:3.2f}_{t}_{m}/frame_{f}.png')


files = os.listdir(src_path)

alphas = [0.1, 0.5, 0.9]
frames = list(range(4))
types = ['white', 'cos', 'exp', 'pow', 'triangle']
memories = [1, 100]

width = len(types) * len(memories) - 1

for alpha in alphas:
	for frame in frames:
		f, axes = plt.subplots(width+1, width+1, constrained_layout=True, figsize=(20,20))

		images = [
			np.asarray(Image.open(
				os.path.join(path.from_spec(alpha, t, m), f'frame_{frame}.png')
			).convert('L'))
			for t,m in itertools.product(types, memories)
			if not (t == 'white' and m == 100)
		]

		axes[0][0].imshow(images[0], cmap='gray')
		axes[0][0].axis('off')

		for i, image in enumerate(images):
			for a in [axes[0][1+i], axes[1+i][0]]:
				a.imshow(image)
				a.axis('off')


		for _a, base in zip(axes[1:], images):
			for a, i in zip(_a[1:], images):
				a.imshow((i - base))
				a.axis('off')

		f.savefig(f'compared/{alpha:3.2f}_{frame}.jpg')
