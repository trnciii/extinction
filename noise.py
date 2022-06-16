import numpy as np

def noise(n, k, rng):
	mean = noise_lim_mean(k)

	ret = np.empty(n)
	ret[0] = rng.uniform() * 2*mean
	for i in range(n-1):
		ret[i+1] = k*ret[i] + rng.random()*np.sqrt(1-k*k)
	return ret

def noise_lim_mean(k):
	return np.sqrt(1-k*k) / (2*(1-k))

def noise_mean(x0, n, k):
	term1 = (x0 * (1-k**n)) / (n*(1-k))
	term2 = noise_lim_mean(k)
	term3 = (np.sqrt(1-k*k) * (1-k**n)) / (2*n*(1-k)*(1-k))

	return term1 + term2 + term3, term2
