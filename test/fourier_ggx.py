import numpy as np
import os
from matplotlib import pyplot as plt

path = '../data/ggx-sigma-0-25-0-25_2048-it-150.npy'
f, ax = plt.subplots(3,1,constrained_layout=True, figsize=(30,20))


height = np.load(path)[1024]

print(height)

signal = np.fft.fft(height)
amp = np.abs(signal)
phase = np.angle(signal)
freq = np.fft.fftfreq(height.shape[0])

print(f'{signal.shape=}')
half = signal.shape[0]//2
# half = 200

n = max(2**10, half)
ret = np.pad(phase[:half], (0, n-half), 'symmetric')

print(f'{phase[:half].shape}')
print(f'{phase[:half]=}')

print(f'{ret.shape=}')
print(f'{ret=}')

ax[0].plot(freq, amp)
ax[1].plot(range(ret.shape[0]), ret)
ax[2].plot(range(height.shape[0]), height)

print(flush=True)
plt.show()
