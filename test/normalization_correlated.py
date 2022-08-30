import mfgeo
from mfgeo import ggx
from mfgeo.noise import oneoverf
import numpy as np
from matplotlib import pyplot as plt


direction = np.vectorize(lambda th: np.array([np.sin(th), 0, np.cos(th)]))


rows = 3
fig, ax = plt.subplots(rows, 1, figsize=(10, 10), constrained_layout=True)


size = 10000
rngs = [np.random.default_rng(seed=i) for i in range(1000)]
u = rngs[0].uniform(size=(size, 2))


alpha = 1
for beta, ax in zip(range(-1, -1 + rows + 1, 1), ax):
	print(f'{beta=}')

	height = np.array([oneoverf.sequence(size, beta, rng) for rng in rngs])

	graph = {
		'th': [],
		'area': [],
		'correlated': [],
	}

	for th in np.linspace(0, np.pi/2, 100):
		wo = direction(th)

		m, nd = mfgeo.sample.uniform_hemisphere(u)
		mo = np.maximum(np.dot(m, wo), 0)
		D = ggx.ndf(np.arccos(m[:, 2]), alpha) * m[:, 2]

		sum_D = np.mean(mo * ggx.ndf(np.arccos(m[:, 2]), alpha)) * 2*np.pi

		area = wo[2]/sum_D
		slope = 1/np.tan(th)/alpha
		correlated = mfgeo.g1_distant(height, [slope])[0]
		diff = np.abs(area-correlated)

		graph['th'].append(th)
		graph['area'].append(area)
		graph['correlated'].append(correlated)
		print(f'{th:0.3f} {area=:.10f} {correlated=:.10f} {diff:.10f}')

	print()

	for name in ['area', 'correlated']:
		ax.plot(graph['th'], graph[name], label=name)

	ax.legend()

print(flush=True)
plt.savefig('result/normalization_corr.png', dpi=150)
plt.show()