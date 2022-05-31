import numpy as np
from matplotlib import pyplot as plt


whitenoise = lambda rng, n: rng.random(n)


sigmas = []
sigmas_averaged = []

for mu in range(50):
	n = 100
	rng = np.random.default_rng(seed=mu)

	t = np.linspace(1/n, 1, n)
	sigmas.append(whitenoise(rng, n))
	sigmas_averaged.append(np.cumsum(sigmas[-1])/t)


	# print(sigma)
	# print(sigma_averaged)


figs = {}

# color, order, line width
line_top = ('salmon', 1, 1.5)
line_cloud = ('#77777777', 0, 1)

figs['sigma'] = plt.figure()
for i in range(len(sigmas)):
	c, order, w = line_top if i == 0 else line_cloud
	plt.plot(t, sigmas[i], color=c, linewidth=w, zorder=order)

figs['sigma_averaged'] = plt.figure()
for i in range(len(sigmas_averaged)):
	c, order, w = line_top if i == 0 else line_cloud
	plt.plot(t, sigmas_averaged[i], color=c, linewidth=w, zorder=order)


shown = {'sigma_averaged'}
for f in [v for k, v in figs.items() if k not in shown]:
	plt.close(f)
plt.show()

for k, v in figs.items():
	v.savefig('./result/{}.png'.format(k), dpi=150)
