import numpy as np
from matplotlib import pyplot as plt
from mfgeo.autocorrelation import acf


def input_ac():
	length = 2**10
	lin = np.arange(length)

	ac = 1/np.power(1+lin, 0.5)

	# ac = np.cos(lin/10)*np.exp(-lin/10)

	# ac = np.zeros(length)
	# ac[0] = 1

	# ac = np.exp(-lin)

	return ac


def gen_height(ac):
	psd = np.fft.fft(ac)
	fft = np.sqrt(psd)
	freq = np.fft.fftfreq(len(ac))

	rng = np.random.default_rng(seed=0)
	phase = np.array(2j*np.pi*rng.random(len(fft)//2 + 1))
	phase_sym = np.concatenate((phase[:-1], np.conj(np.flip(phase[1:]))))

	margin = int(len(ac)*0.15)
	height = np.fft.ifft(fft*phase_sym)[margin:len(ac)-margin]

	return height



ac_in = input_ac()
plt.plot(range(len(ac_in)), ac_in, label='ac_in')


height = gen_height(ac_in)
plt.plot(range(len(height)), height, label='height')


ac_r = acf(height)
plt.plot(range(len(ac_r)), ac_r/ac_r[0], label='ac_result')


print(flush=True)
plt.legend()
plt.show()
