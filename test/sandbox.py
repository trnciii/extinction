from mfgeo import noise, figurateur
import numpy as np
from matplotlib import pyplot as plt
import os, path

outdir = path.out()


figs = {}
generator = noise.oneoverf
n_range = [10**e for e in range(3, 6)]
figs[generator.name], axes = plt.subplots(len(n_range), 1, figsize=(20, 10), constrained_layout=True)

for n, ax in zip(n_range, axes):
	rngs = [np.random.default_rng(seed=mu) for mu in range(10)]

	height = np.array([generator.sequence(n, 0.99, rng) for rng in rngs])
	slope = np.diff(height)

	target = height[:, :200]


	print(f'type={generator.name} {n=} min={np.amin(target)} max={np.amax(target)} std={np.std(target)}')
	print(flush=True)

	size = target.shape[1]
	# size = 500
	sliced = target[:, -size:]
	figurateur.cloud(ax, np.linspace(1, size, size), sliced)

plt.savefig(os.path.join(outdir, f'{generator.name}.png'.replace('/', '-')))

figurateur.save(figs, out_dir=outdir)
figurateur.show(figs)
