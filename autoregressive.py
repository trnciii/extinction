import numpy as np

def sequence(n, k, rng):
	if k>=1: k = 0.99
	if k<=-1: k = -0.99

	mean = lim_mean(k)

	ret = np.empty(n)
	ret[0] = rng.uniform() * 2*mean
	for i in range(n-1):
		ret[i+1] = k*ret[i] + rng.uniform()*np.sqrt(1-k*k)
	return ret

def lim_mean(k):
	return np.sqrt(1-k*k) / (2*(1-k))

def lim_std(k):
	return np.sqrt((1-k*k)/12)/(1-k)

def mean(x0, n, k):
	term1 = (x0 * (1-k**n)) / (n*(1-k))
	term2 = lim_mean(k)
	term3 = (np.sqrt(1-k*k) * (1-k**n)) / (2*n*(1-k)*(1-k))

	return term1 + term2 + term3


if __name__ == '__main__':

	import figurateur

	n = 1000
	k = 1
	seqs = 100

	rngs = [np.random.default_rng(seed=i) for i in range(seqs)]
	noises = np.array([sequence(n, k, rng) for rng in rngs])

	figs = figurateur.inspect_noise(noises)

	figurateur.save(figs, prefix='ar_')
	figurateur.show(figs)
