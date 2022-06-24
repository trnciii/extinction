import numpy as np
from matplotlib import pyplot as plt


def one_f_beta(n, beta, rngs=[np.random.default_rng(seed=0)]):
	if type(rngs) is not list:
		rngs = [rngs]

	kmax = n//2
	seqs = len(rngs)


	f = np.tile( np.linspace(1, kmax, kmax), (seqs, 1) ) / (2*np.pi)
	C = 1/np.abs(f**beta)

	phase = np.array([2*np.pi*rng.random((kmax)) for rng in rngs])
	Cpos = C*np.exp(1j*phase)
	Cneg = np.flip(np.conj(Cpos))

	C = np.concatenate((np.zeros((seqs, 1)), Cpos, Cneg), axis=1)
	noise = np.fft.ifft(C)

	return noise.real[:, :n]



if __name__ == '__main__':
	n = 1000
	beta = 1
	seqs = 200

	rngs = [np.random.default_rng(seed=i) for i in range(seqs)]
	noises = one_f_beta(n, beta, rngs)


	fig, ax = plt.subplots(1, 2)

	# color, order, line width
	line_top = 'salmon', 1, 2
	line_cloud = '#77777777', 0, 1

	timeline = np.linspace(0, 1, n)
	for i in range(len(noises)):
		c, order, w = line_top if i == 0 else line_cloud
		ax[0].plot(timeline, noises[i], color=c, linewidth=w, zorder=order)
	ax[0].set_position((0.1, 0.05, 0.7, 0.95))


	ax[1].hist(noises.reshape((-1)), bins=20, orientation='horizontal')
	ax[1].set_position((0.8, 0.05, 0.2, 0.95))
	# ax[1].set_box_aspect(4)
	ax[1].get_xaxis().set_visible(False)
	ax[1].get_yaxis().set_visible(False)



	plt.show()