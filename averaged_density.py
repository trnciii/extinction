import numpy as np
from matplotlib import pyplot as plt


n = 100

rngs = [np.random.default_rng(seed=mu) for mu in range(50)]
timeline = np.linspace(1/n, 1, n)

sigmas = np.array([rng.random(n) for rng in rngs])
sigmas_averaged = np.cumsum(sigmas, axis=1)/timeline


figs = {}

# color, order, line width
line_top = ('salmon', 1, 1.5)
line_cloud = ('#77777777', 0, 1)

figs['sigma'] = plt.figure()
for i in range(len(sigmas)):
	c, order, w = line_top if i == 0 else line_cloud
	plt.plot(timeline, sigmas[i], color=c, linewidth=w, zorder=order)

figs['sigma_averaged'] = plt.figure()
for i in range(len(sigmas_averaged)):
	c, order, w = line_top if i == 0 else line_cloud
	plt.plot(timeline, sigmas_averaged[i], color=c, linewidth=w, zorder=order)


shown = {'sigma', 'sigma_averaged'}
for f in [v for k, v in figs.items() if k not in shown]:
	plt.close(f)
plt.show()

for k, v in figs.items():
	v.savefig('./result/{}.png'.format(k), dpi=150)
