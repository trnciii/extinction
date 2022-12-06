import numpy as np
import os
from matplotlib import pyplot as plt

def plot(x):
	f, ax = plt.subplots(3, 1, constrained_layout=True, figsize=(25, 15))
	ft = np.fft.fft(x)
	amp = np.abs(ft)
	phase = np.angle(ft)
	freq = np.fft.fftfreq(x.shape[0])

	ax[0].title.set_text('signal')
	ax[0].plot(range(x.shape[0]), x)

	ax[1].title.set_text('amp')
	ax[1].plot(freq, amp)

	ax[2].title.set_text('phase')
	ax[2].plot(freq, phase)

	return ft, amp, phase, freq


path = '../data/ggx-sigma-0-25-0-25_2048-it-150.npy'
height = np.load(path)[1024]

_, _, phase, _ = plot(height)

plot(phase[:200])


print(flush=True)
plt.show()
