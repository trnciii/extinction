import numpy as np

name = '1/f'

def sequence(n, b, rng, silent=False):
	if (not (-1<b<1)) and (not silent):
		print(f'1/f sequence is not stationary. {b=}')

	kmax = n//2

	f = np.linspace(0.5, 1, kmax)/(2*np.pi)
	C = 1/np.abs(f**b)

	phase = np.array(2*np.pi*rng.random(kmax))
	Cpos = C*np.exp(1j*phase)
	Cneg = np.flip(np.conj(Cpos))

	C = np.concatenate(([0], Cpos, Cneg))
	noise = np.fft.ifft(C)

	re = noise.real[:n]
	return re/np.std(re)

	return noise.real[:n]



def main():
	from extinction import figurateur

	n = 1000
	beta = 1
	seqs = 100

	rngs = [np.random.default_rng(seed=i) for i in range(seqs)]
	noises = np.array([sequence(n, beta, rng) for rng in rngs])

	figs = figurateur.inspect_noise(noises)

	figurateur.save(figs, prefix='1_f_')
	figurateur.show(figs, exclude={'noises'})


if __name__ == '__main__':
	main()