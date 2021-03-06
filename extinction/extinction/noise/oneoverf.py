import numpy as np

name = '1/f'

def sequence(n, beta, rng):
	kmax = n//2

	f = np.linspace(1, kmax, kmax)/(2*np.pi)
	C = 1/np.abs(f**beta)

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