import numpy as np
from matplotlib import pyplot as plt
from mfgeo.autocorrelation import acf


length = 2**10

ac = 1/np.power(1+np.arange(length), 0.5)

# ac = np.zeros(length)
# ac[0] = 1

# ac = np.exp(-np.arange(length))

plt.plot(range(len(ac)), ac, label='ac_in')


psd = np.fft.fft(ac)
fft = np.sqrt(psd)
freq = np.fft.fftfreq(len(ac))

# plt.plot(freq, psd.real, label='psd.real')
# plt.plot(freq, psd.imag, label='psd.imag')

# plt.scatter(freq, fft.real, label='fft.real')
# plt.scatter(freq, fft.imag, label='fft.imag')


rng = np.random.default_rng(seed=0)
phase = np.array(2j*np.pi*rng.random(len(fft)//2 + 1))
phase_sym = np.concatenate((phase[:-1], np.conj(np.flip(phase[1:]))))


margin = int(length*0.15)
height = np.fft.ifft(fft*phase_sym)[margin:length-margin]
print(height)

plt.plot(range(len(height)), height, label='height')

ac = acf(height)
print('ac')
print(ac)
plt.plot(range(len(ac)), ac/ac[0], label='ac_result')


print(flush=True)
plt.legend()
plt.show()
