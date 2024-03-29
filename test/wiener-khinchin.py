import numpy as np
from matplotlib import pyplot as plt
from mfgeo import dist, acf, g1_distant, g1_distant_single
from scipy import stats
import path
import itertools
import os, json, inspect


def input_ac(e, t, memory):
	length = 2**e
	lin = np.linspace(0, 1/memory, length)

	if t == 'white':
		ac = np.zeros(length)
		ac[0] = 1
		return ac

	elif t == 'pow':
		return 1/np.power(1+lin*1000, 0.5)

	elif t == 'cos':
		return np.cos(lin*20000)*np.exp(-lin*1000)

	elif t == 'exp':
		return np.exp(-lin*1000)

	elif t == 'triangle':
		return np.maximum(1 - lin*200, 0)

	else:
		raise NotImplementedError


def gen_height(ac, rng):
	ac = np.concatenate((ac[:-1], np.flip(ac[1:])))

	psd = np.fft.fft(ac)
	np.save(out('psd'), psd)
	# print('psd')
	# print(psd[:50], '...', psd[-50:], sep='\n')
	# assert np.allclose(psd.imag, 0)
	# assert np.all(psd.real > 0)

	amp = np.sqrt(psd.real)

	n = len(amp)//2 + 1
	phase = 2*np.pi*rng.random(n)
	phase_sym = np.concatenate((phase[:-1], -np.flip(phase[1:])))

	height = np.fft.ifft(amp*np.exp(1j * phase_sym))
	np.save(out('height_complex'), height)


	print(f'{np.max(height.imag)}')

	return height.real


def gen_height_slope_normalized(ac, alpha, rng):
	height = gen_height(ac, rng)
	slope = np.diff(height.real)

	scale = alpha / (2**0.5 * np.std(slope))

	return height*scale, slope*scale


def plot_heights(height, slope, file):
	f, ax = plt.subplots(2, 2, figsize=(20, 3), constrained_layout=True)
	(top_l, top_r), (bottom_l, bottom_r) = ax

	top_l.plot(range(len(height)), height, label='height')
	bottom_l.plot(range(len(slope)), slope, label='slope')

	n = 400
	top_r.plot(range(n), height[:n], label='height')
	bottom_r.plot(range(n), slope[:n], label='slope')

	f.savefig(file)
	plt.close(f)


# parameters
for e, alpha, t, mem in itertools.product(
	[18],

	[0.1, 0.5, 0.9],
	# [0.5],

	['white', 'cos', 'exp', 'pow', 'triangle'],
	[1, 100],
):
	print()
	try:
		_o = path.out()
		out = lambda file: os.path.join(_o, file)

		meta = {
			'id': os.path.split(os.path.split(_o)[0])[1],
			'length': e,
			'alpha': alpha,
			'type': t,
			'memory': mem,
			'code': path.code()
		}

		# figures
		fig, axes = plt.subplots(1, 5, figsize=(20,4), constrained_layout=True)
		(ax_c, ax_ch, ax_d, ax_qq, ax_g) = axes


		# autocorrelation
		ac_in = input_ac(e, t, mem)

		np.save(out('ac_input'), ac_in)


		# height and slope
		rng = np.random.default_rng(seed=0)
		height, slope = gen_height_slope_normalized(ac_in, alpha, rng)

		meta['cov'] = str(np.cov(height[:-1], slope))
		# height = gen_height(ac_in)
		# slope = np.diff(height.real)

		np.save(out('height'), height)
		np.save(out('slope'), slope)
		plot_heights(height, slope, file=out('height.png'))

		stats.probplot(slope, plot=ax_qq)
		meta['shapiro'] = stats.kstest(slope, 'norm')
		print('shapiro', meta['shapiro'])

		# autocorrelation
		ac_r = acf(height)
		ac_r /= ac_r[0]

		np.save(out('ac_generated'), ac_r)


		# plot autocorrelations
		ax_c.plot(range(len(ac_in)), ac_in, label='ac_input')
		ax_c.plot(range(len(ac_r)), ac_r, label='ac_generated')

		_n = 200
		ax_ch.plot(range(_n), ac_in[:_n], label='ac_input')
		ax_ch.plot(range(_n), ac_r[:_n], label='ac_generated')


		# numerical distribution
		hist, bins = np.histogram(slope, bins='auto', density=True)
		x = bins[:-1]

		# common distribution
		profile = dist.beckmann
		angle = np.arctan(x)
		theo = profile.ndf(angle, alpha) * np.power(np.cos(angle), 4)
		theo /= np.sum(theo) * (bins[1] - bins[0])

		# plot ndfs
		ax_d.plot(x, hist, label='generated')
		ax_d.plot(x, theo, label=f'{profile.name()} a={alpha}')
		# ax_d.plot(x, normal, label=f'normal ({mean:.2f},{std:.2f})')


		# visibility
		n = 100
		angle = np.linspace(1/n, np.pi/2, n)

		ax_g.plot(angle, profile.smith_g1(angle, alpha), label=f'{profile.name()} smith',
			color='C0', zorder=1000)

		meta['starts size'] = {}

		step = 100
		G = np.ones((step, n))
		for i in range(step):
			mu = i/step * np.pi - 0.5*np.pi

			theta = np.arctan(-slope[:len(height)//2])
			starts = np.where((mu <= theta) & (theta < mu + np.pi/step))[0]

			meta['starts size'][mu] = starts.shape[0]
			G[i,:] = g1_distant_single(height, starts, 1/np.tan(angle))

		np.save(out('visibility'), G)

		for g in G:
			ax_g.plot(angle, g, color='gray', zorder=0)


		with open(out('meta.json'), 'w') as f:
			f.write(json.dumps(meta, indent=2))

		print(f'done ( {e=} {alpha=} {t=} {mem=})', flush=True)
		# for a in axes: a.legend()
		fig.savefig(out('stat.png'))
		# plt.show()

		os.system(f'python3 {os.path.join(path.cur(), "wiener-khinchin", "index.py")}')

	except Exception as exception:
		import traceback
		print(f'Error at ( {e} {alpha} {t} )')
		traceback.print_exception(exception)
		os.system(f'python3 {os.path.join(path.cur(), "wiener-khinchin", "index.py")} clean')

	finally:
		plt.close(fig)