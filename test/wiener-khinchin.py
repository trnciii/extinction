import numpy as np
from matplotlib import pyplot as plt
from mfgeo import dist, acf
from scipy.stats import norm


def input_ac():
	length = 2**10
	lin = np.arange(length)

	ac = 1/np.power(1+lin, 0.2)

	# s = length/100
	# ac = np.cos(lin/s)*np.exp(-lin/s)

	# ac = np.zeros(length)
	# ac[0] = 1

	# s = length/10
	# ac = np.exp(-lin/s)

	return ac


def gen_height(ac):
	psd = np.fft.fft(ac)
	fft = np.sqrt(psd)
	freq = np.fft.fftfreq(len(ac))

	rng = np.random.default_rng(seed=0)
	n = len(fft)//2 + 1
	phase = 2j*np.pi*rng.random(n)
	phase_sym = np.concatenate((phase[:-1], np.conj(np.flip(phase[1:]))))

	margin = int(len(ac)*0.2)
	height = np.fft.ifft(fft*phase_sym)[margin:len(ac)-margin]

	return height


def plot_heights(height, slope):
	_, (ax_h, ax_s) = plt.subplots(2, 1, figsize=(20, 5), constrained_layout=True)
	ax_h.plot(range(len(height)), height, label='height')
	ax_s.plot(range(len(slope)), slope, label='slope')



_, (ax_c, ax_d) = plt.subplots(1, 2, figsize=(14,4), constrained_layout=True)

ac_in = input_ac()
ax_c.plot(range(len(ac_in)), ac_in, label='ac_in')


# height and slope
height = gen_height(ac_in)
slope = np.diff(height.real)

# plot_heights(height, slope)


# autocorrelation
ac_r = acf(height)
ax_c.plot(range(len(ac_r)), ac_r/ac_r[0], label='ac_result')


# numerical distribution
hist, bins = np.histogram(slope, bins='auto', density=True)
x = bins[:-1]

ax_d.plot(x, hist, label='numerical')


# normal distribution
mean = np.mean(slope)
std = np.std(slope)
normal = norm.pdf(x, loc=mean, scale=std)

ax_d.plot(x, normal, label=f'normal {mean:.2f} {std:.2f}')


# common distribution
profile = dist.beckmann
alpha = 0.4
angle = np.arctan(x)
theo = profile.ndf(angle, alpha) * np.power(np.cos(angle), 4)
theo /= np.sum(theo) * (bins[1] - bins[0])

ax_d.plot(x, theo, label=f'{profile.name()} a={alpha}')


print(flush=True)
ax_c.legend()
ax_d.legend()
plt.show()
