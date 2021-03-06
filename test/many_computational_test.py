import extinction, numpy as np
from extinction.noise import oneoverf
from extinction import figurateur

from matplotlib import pyplot as plt

n = 1000

rngs = [np.random.default_rng(seed=mu) for mu in range(1000)]
timeline = np.linspace(1, n, n)

rows = 6

fig = plt.figure(figsize=(16, 12), constrained_layout=True)
figs_s, figs_v = fig.subfigures(1, 2, width_ratios=[2.5,1])
ax_v = figs_v.subplots(rows, 1)
ax_s = figs_s.subplots(rows, 1)


for beta, ax_s, ax_v in zip(np.linspace(-2, 3, rows), ax_s, ax_v):
	key = f'b{beta:+.1f}'

	sigmas = np.array([oneoverf.sequence(n, beta, rng) for rng in rngs])
	figurateur.cloud(ax_s, timeline, sigmas[:20])
	ax_s.set_title(f'b = {beta}')

	for alpha in np.linspace(0.1, 1, 10):
		steps = 1000
		angle = np.linspace(1/steps, np.pi/2, steps)

		slope = 1/np.tan(angle)/alpha
		tested = extinction.visibility(sigmas, slope)

		ax_v.plot(angle, tested, label=f'{alpha:.1}')


fig.savefig('result/betas.png')
plt.show()
