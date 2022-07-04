import numpy as np
from matplotlib import pyplot as plt
import sys

import autoregressive
import oneoverf

import figurateur


def acf(x, window=None):
	if window == None: window = len(x)//2
	npcorr = np.correlate(x, x[:window], mode='valid')
	return npcorr/npcorr[0]


figs = {}

for generator in [autoregressive, oneoverf]:

	n = 1000
	num_k = 7

	figs[generator.name], ax = plt.subplots(num_k, 2, tight_layout=True, figsize=(19.2, 10.8))

	rng = np.random.default_rng(seed=1234)

	for k, (ax_nosie, ax_ac) in zip(np.linspace(-1, 1, num_k), ax):
		noise = generator.sequence(n, k, rng)
		ac = acf(noise)

		ax_nosie.plot(np.linspace(1, n, n), noise, linewidth=0.6)
		ax_nosie.set_title('k = {:.3}'.format(k), loc='left')
		ax_ac.plot(np.linspace(1, len(ac), len(ac)), ac, linewidth=0.6)


figurateur.save(figs, prefix='autocorr_')

if not '-b' in sys.argv:
	figurateur.show(figs)

