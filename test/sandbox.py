from mfgeo import noise, figurateur
import numpy as np
from matplotlib import pyplot as plt
import os, path

outdir = path.out()


figs = {}
generator = noise.oneoverf
n_range = [10**e for e in range(3, 8)]
figs[generator.name], axes = plt.subplots(len(n_range), 1, figsize=(20, 10), constrained_layout=True)

for n, ax in zip(n_range, axes):
	rngs = [np.random.default_rng(seed=mu) for mu in range(10)]

	height = np.array([generator.sequence(n, 1, rng) for rng in rngs])

	print(f'type={generator.name} {n=} min={np.amin(height)} max={np.amax(height)} std={np.std(height)}')
	print(flush=True)

	size = height.shape[1]
	# size = 500
	sliced = height[:, -size:]
	figurateur.cloud(ax, np.linspace(1, size, size), sliced)

plt.savefig(os.path.join(outdir, f'{generator.name}.png'.replace('/', '-')))

figurateur.save(figs, out_dir=outdir)
figurateur.show(figs)

