import mfgeo
from mfgeo import ggx
import numpy as np


direction = np.vectorize(lambda th: np.array([np.sin(th), 0, np.cos(th)]))


size = 10000

rng = np.random.default_rng(seed=0)
u = rng.uniform(size=(size, 2))

alpha = 0.95

for alpha in np.linspace(0.1, 1, 10):
	print(f'{alpha=:.3f}')
	m, nd = mfgeo.sample.uniform_hemisphere(u)
	D = ggx.ndf(np.arccos(m[:, 2]), alpha) * m[:, 2]

	th = np.linspace(0, np.pi/2, 10)
	smith = ggx.smith_g1(th, alpha)

	wo = np.zeros((th.size, 3))
	wo[:, 0] = np.sin(th)
	wo[:, 2] = np.cos(th)

	mo = np.array([np.maximum(np.dot(m, _wo), 0) for _wo in wo])
	sum_D = np.mean(mo*ggx.ndf(np.arccos(m[:, 2]), alpha), axis=1) * 2*np.pi
	area = wo[:, 2]/sum_D
	diff = np.abs(area-smith)

	print('\n'.join(f'{th:0.3f} {area=:.10f} {smith=:.10f} {diff:.10f}'
		for th, area, smith, diff in zip(th, area, smith, diff)))

	print()