import numpy as np
from matplotlib import pyplot as plt
from mfgeo import dist, acf, g1_distant, g1_distant_single
from scipy.stats import norm
import path
import itertools


def input_ac(e, t):
	length = 2**e
	lin = np.linspace(0, 1000, length)

	def white():
		ac = np.zeros(length)
		ac[0] = 1
		return ac

	def onef(b=0.5):
		return 1/np.power(1+lin, 0.5)

	def cos():
		return np.cos(lin/10)*np.exp(-lin/100)

	def exp():
		return np.exp(-lin/100)

	return {
		'white': white,
		'1f': onef,
		'cos': cos,
		'exp': exp
	}[t]()


def gen_height(ac):
	ac = np.concatenate((ac[:-1], np.flip(ac[1:])))

	psd = np.fft.fft(ac)
	# print('psd')
	# print(psd[:50], '...', psd[-50:], sep='\n')
	# assert np.allclose(psd.imag, 0)
	# assert np.all(psd.real > 0)

	amp = np.sqrt(psd.real)
	freq = np.fft.fftfreq(len(ac))

	rng = np.random.default_rng(seed=0)
	n = len(amp)//2 + 1
	phase = 2j*np.pi*rng.random(n)
	phase_sym = np.concatenate((phase[:-1], np.conj(np.flip(phase[1:]))))

	margin = int(len(ac)*0.2)
	height = np.fft.ifft(amp*phase_sym)[margin:len(ac)-margin]

	# print('height')
	# print(height[:100])

	return height.real/np.amax(height.real)


def gen_height_slope_normalized(ac, alpha):
	height = gen_height(ac)
	slope = np.diff(height.real)

	scale = alpha / (2**0.5 * np.std(slope))

	return height*scale, slope*scale


def plot_heights(height, slope, suffix):
	f, ax = plt.subplots(2, 2, figsize=(20, 3), width_ratios=[4,1], constrained_layout=True)
	(top_l, top_r), (bottom_l, bottom_r) = ax

	top_l.plot(range(len(height)), height, label='height')
	bottom_l.plot(range(len(slope)), slope, label='slope')

	n = 100
	top_r.plot(range(n), height[:n], label='height')
	bottom_r.plot(range(n), slope[:n], label='slope')

	f.savefig(path.out(f'field_{suffix}.png'))


# parameters
for e, alpha, t in itertools.product(
	[23],
	[0.1, 0.2, 0.5, 0.9],
	['white', '1f', 'cos', 'exp']
):
	suffix = f'{e}_{str(alpha).replace("0.", "")}_{t}'

	# figures
	fig, axes = plt.subplots(1, 3, figsize=(19,4), constrained_layout=True)
	(ax_c, ax_d, ax_g) = axes


	# autocorrelation
	ac_in = input_ac(e, t)
	ax_c.plot(range(len(ac_in)), ac_in, label='ac_in')


	# height and slope
	height, slope = gen_height_slope_normalized(ac_in, alpha)

	# height = gen_height(ac_in)
	# slope = np.diff(height.real)

	plot_heights(height, slope, suffix)


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

	ax_d.plot(x, normal, label=f'normal ({mean:.2f},{std:.2f})')


	# compare D
	profile = dist.beckmann
	angle = np.arctan(x)
	theo = profile.ndf(angle, alpha) * np.power(np.cos(angle), 4)
	theo /= np.sum(theo) * (bins[1] - bins[0])

	ax_d.plot(x, theo, label=f'{profile.name()} a={alpha}')


	# compare G
	n = 100
	angle = np.linspace(1/n, np.pi/2, n)

	half = len(height)//2
	starts = np.arange(0, half+1, min(10000, half))
	G = g1_distant_single(height, starts, 1/np.tan(angle))

	ax_g.plot(angle, G, label='tested')
	ax_g.plot(angle, profile.smith_g1(angle, alpha), label=f'{profile.name()} smith')


	print(f'done {suffix}', flush=True)
	for a in axes: a.legend()
	fig.savefig(path.out(f'stat_{suffix}.png'))
	# plt.show()

	plt.close()
