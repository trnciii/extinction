import numpy as np

name = 'AR'

def sequence(n, k, rng, margin=1000, silent=False):
	if (not (-1<k<1)) and (not silent):
		print(f'autoregressive process is not stationary. {k=}')

	ret = np.empty(n+margin)
	ret[0] = rng.normal()
	for i in range(n+margin-1):
		ret[i+1] = k*ret[i] + rng.normal()
	return ret[-n:]


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