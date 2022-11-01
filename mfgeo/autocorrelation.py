import numpy as np

def w_k(x):
	size = 2**np.ceil(np.log2(2*len(x) - 1)).astype('int')
	fft = np.fft.fft(x, size)
	pwr = np.abs(fft)**2
	corr = np.fft.ifft(pwr).real[:len(x)]
	return corr/corr[0]


def full(x):
	corr = np.correlate(x, x, 'full')[len(x)-1:]
	return corr/corr[0]


def valid(x, window=None):
	if window == None: window = len(x)//2
	corr = np.correlate(x, x[:window], mode='valid')
	return corr/corr[0]


def same(x):
	corr = np.correlate(x, x, mode='same')[len(x)//2:]
	return corr/corr[0]


acf = full


def runall():
	from matplotlib import pyplot as plt

	rng = np.random.default_rng(seed=0)
	x = rng.random(100)
	for name, f in [('w_k', w_k), ('full', full), ('valid', valid), ('same', same)]:
		co = f(x)
		print(name, len(co))
		print(co)
		plt.plot(range(len(co)), co, label=name)

	print(flush=True)
	plt.legend()
	plt.show()


if __name__ == '__main__':

	runall()
	exit()

	from matplotlib import pyplot as plt
	import sys

	from noise import autoregressive
	from noise import oneoverf

	import figurateur


	figs = {}

	for generator in [autoregressive, oneoverf]:

		n = 1000
		num_k = 5

		figs[generator.name], ax = plt.subplots(num_k, 2, tight_layout=True, figsize=(19.2, 10.8))

		rng = np.random.default_rng(seed=1234)

		for k, (ax_nosie, ax_ac) in zip(np.linspace(-0.99, 0.99, num_k), ax):
			noise = generator.sequence(n, k, rng)
			ac = acf(noise)

			ax_nosie.plot(range(n), noise, linewidth=0.6)
			ax_nosie.set_title('k = {:.3}'.format(k), loc='left')
			ax_ac.plot(range(ac.shape[0]), ac, linewidth=0.6)


	figurateur.save(figs, prefix='autocorr_')

	if not '-b' in sys.argv:
		figurateur.show(figs)