import mfgeo
from mfgeo import ggx
import numpy as np


def direction(th):
	return np.array([np.sin(th), 0, np.cos(th)])


size = 10000

rng = np.random.default_rng(seed=0)
u = rng.uniform(size=(size, 2))

alpha = 0.95

for alpha in np.linspace(0.1, 1, 10):
	print(f'{alpha=}')
	for th in np.linspace(0, np.pi/2, 10):
		wo = direction(th)

		m, nd = mfgeo.sample.uniform_hemisphere(u)
		mo = np.maximum(np.dot(m, wo), 0)
		D = ggx.ndf(np.arccos(m[:, 2]), alpha) * m[:, 2]

		sum_D = np.mean(mo * ggx.ndf(np.arccos(m[:, 2]), alpha)) * 2*np.pi

		area = wo[2]/sum_D
		g1 = ggx.smith_g1(th, alpha)
		diff = np.abs(area-g1)

		print(f'{th:0.3f} {area=:.10f} {g1=:.10f} {diff:.10f}')
	print()