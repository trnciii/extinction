import numpy as np

name = 'AR'

def sequence(n, k, rng):
	if k>1: k = 1
	if k<-1: k = -1

	ret = np.empty(n)
	ret[0] = rng.normal()
	for i in range(n-1):
		ret[i+1] = k*ret[i] + rng.normal()
	return ret/np.std(ret)


def main():
	from extinction import figurateur

	n = 1000
	k = 1
	seqs = 100

	rngs = [np.random.default_rng(seed=i) for i in range(seqs)]
	noises = np.array([sequence(n, k, rng) for rng in rngs])

	figs = figurateur.inspect_noise(noises)

	figurateur.save(figs, prefix='ar_')
	figurateur.show(figs)

if __name__ == '__main__':
	main()