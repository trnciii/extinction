import numpy as np
from scipy.stats import norm
from mfgeo.noise import oneoverf, autoregressive
from mfgeo import figurateur
from matplotlib import pyplot as plt
import path


def probability(x, sample):
	hist, bin_edges = np.histogram(sample, bins='auto', density=True)
	index = np.digitize(x, bin_edges)
	return np.where((0<index) * (index<hist.size),
		np.take(hist, index-1, mode='clip'),
		0
	)

phase = (0, 0.5*np.pi)

n = 10000
rngs = [np.random.default_rng(seed=mu) for mu in range(1000)]

# for beta in np.linspace(-0.99, 0.99, 3):
beta = 0.99

height = np.array([oneoverf.sequence(n, beta, rng, phase_range=phase) for rng in rngs])
slope = np.diff(height)

hist, bin_edges = np.histogram(slope, bins='auto', density=True)


print(f'{hist.size=}')
print(hist)
print(f'{bin_edges.size=}')
print(bin_edges)

sample_slope = [-1, 0, 1]
print(f'prob={probability(sample_slope, slope)}')

print()

plt.plot(bin_edges[:-1], hist, label=f'{beta=:2} {n=}')

mean, std = norm.fit(slope)
x = np.linspace(-20, 20, 100)
plt.plot(x, norm.pdf(x, mean, std), label=f'fit {beta:2}')

print(flush=True)

plt.xlim((-20, 20))
plt.legend()
plt.savefig(path.out(f'1f_{phase[0]:.1f}-{phase[1]:.1f}_{beta:2}_slope.png'))
plt.show()

# prob=[0.23422628 0.32976402 0.23475671]
