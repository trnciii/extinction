import extinction, numpy as np
from extinction.noise import oneoverf
from extinction import figurateur
from extinction.bruteforce import ggx_smith_g1
import time
from matplotlib import pyplot as plt


n = 10000
rngs = [np.random.default_rng(seed=mu) for mu in range(10000)]

angle_steps = 100
angle = np.linspace(1/angle_steps, np.pi/2, angle_steps)

adjusted_alpha = 0.5
sigma_ref = np.array([oneoverf.sequence(n, 0, rng) for rng in rngs])
slope_base = 1/np.tan(angle)
ref = np.array(extinction.visibility(sigma_ref, slope_base/adjusted_alpha))


for beta in np.linspace(-2, 3, 6):
	print(f'b : {beta}')
	t0 = time.time()
	sigmas = np.array([oneoverf.sequence(n, beta, rng) for rng in rngs])

	def tested(a):
		return extinction.visibility(sigmas, slope_base/a)

	def dist(a):
		return np.sum((tested(a) - ref)**2)

	def diff(a):
		return dist(a+0.05) - dist(a)

	def fall():
		a = 0.5
		d = diff(a)
		while np.abs(d)>0.05:
			d = diff(a)
			a -= 0.05*d

		t1 = time.time()
		print('d :', d)
		print('a :', a)
		print('time :', t1-t0, flush=True)
		return a, dist(a)

	a, d = fall()

	plt.plot(angle, tested(a), label=f'b={beta:.2f}, a={a:.2f}, diff={d:.2f}')


plt.plot(angle, ref, label=f'b={0:.2f} (ref). a = {adjusted_alpha:.2f}', linewidth=4)
plt.legend()

plt.tight_layout()
plt.savefig('result/fit_to_b0.png', dpi=200)
plt.show()
