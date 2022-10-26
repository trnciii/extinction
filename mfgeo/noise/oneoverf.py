import numpy as np

name = '1/f'

def sequence(n, b, rng, phase_range=(0, 2*np.pi), silent=False):
	if (not (-1<b<1)) and (not silent):
		print(f'1/f sequence is not stationary. {b=}')

	kmax = n//2

	f = np.linspace(0.5, 1, kmax)/(2*np.pi)
	C = 1/np.abs(f**b)

	phase = (phase_range[1]-phase_range[0])*np.array(rng.random(kmax)) + phase_range[0]
	Cpos = C*np.exp(1j*phase)
	Cneg = np.flip(np.conj(Cpos))

	C = np.concatenate(([0], Cpos, Cneg))
	noise = np.fft.ifft(C)

	re = noise.real[:n]
	return re/np.std(re)


def main():
	from mfgeo import figurateur

	n = 1000
	beta = 0.99
	seqs = 100

	rngs = [np.random.default_rng(seed=i) for i in range(seqs)]
	noises = np.array([sequence(n, beta, rng) for rng in rngs])

	figs = figurateur.inspect_noise(noises)

	figurateur.save(figs, prefix='1_f_')
	figurateur.show(figs, exclude={'noises'})


if __name__ == '__main__':
	main()