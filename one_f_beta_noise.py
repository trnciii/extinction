import numpy as np
from matplotlib import pyplot as plt


def one_f_beta(n, beta, rng=np.random.default_rng()):
	kmax = n//2

	f = np.linspace(1, kmax, kmax)/(2*np.pi)
	C = 1/np.abs(f**beta)

	phase = 2*np.pi*rng.random(kmax)
	Cpos = C*np.exp(1j*phase)
	Cneg = np.flip(np.conj(Cpos))

	noise = np.fft.ifft(np.concatenate(([0], Cpos, Cneg)))

	return noise.real[:n]



if __name__ == '__main__':
	n = 1000
	beta = 1

	rng = np.random.default_rng(0)

	noise = one_f_beta(n, beta, rng)

	timeline = np.linspace(0, 1, n)
	plt.plot(timeline, noise)
	plt.show()