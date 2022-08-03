import extinction, numpy as np
from extinction.noise import oneoverf
from extinction import ggx
import time

n = 1000
k_or_beta = 0.0

rngs = [np.random.default_rng(seed=mu) for mu in range(1000)]
timeline = np.linspace(1, n, n)

sigmas = np.array([oneoverf.sequence(n, k_or_beta, rng) for rng in rngs])


steps = 1000
angle = np.linspace(1/steps, np.pi/2, steps)
smith = ggx.smith_g1(angle, 0.5)

slope = 1/np.tan(angle)


t0 = time.time()
tested_cpu = extinction.test.cpu.visibility(sigmas, slope)
t1 = time.time()
print('cpu:', t1-t0)

t0 = time.time()
tested_gpu = extinction.test.gpu.visibility(sigmas, slope)
t1 = time.time()
print('gpu:', t1-t0)

print('allclose', np.allclose(tested_gpu, tested_cpu))