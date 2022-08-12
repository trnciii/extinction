import numpy as np

def cosined_hemisphere(u):
	assert u.ndim == 2 and u.shape[1] == 2

	u1 = 2*np.pi*u[:, 1]
	r = np.sqrt(u[:, 0])
	hemi = np.empty((u.shape[0], 3))
	hemi[:, 0] = r*np.cos(u1)
	hemi[:, 1] = r*np.sin(u1)
	hemi[:, 2] = np.sqrt(1-u[:, 0])
	return hemi, hemi[:, 2]/np.pi

def cosined_hemisphere_angle(u):
	assert u.ndim == 1
	return np.arcsin(np.sqrt(u))


def uniform_hemisphere(u):
	assert u.ndim == 2 and u.shape[1] == 2

	u1 = 2*np.pi*u[:, 1]
	r = np.sqrt(1 - u[:, 0]**2)
	uni = np.empty((u.shape[0], 3))
	uni[:, 0] = r*np.cos(u1)
	uni[:, 1] = r*np.sin(u1)
	uni[:, 2] = u[:, 0]
	return uni, np.array([1/(2*np.pi)]*u.shape[0])

def uniform_hemisphere_angle(u):
	assert u.ndim == 1
	return np.arccos(u)


if __name__ == "__main__":
	import mfgeo
	from matplotlib import pyplot as plt


	rng = np.random.default_rng(seed=0)
	u = rng.uniform(size=(10000, 2))

	uni, p_u = uniform_hemisphere(u)
	cos, p_c = cosined_hemisphere(u)

	uni_a = uniform_hemisphere_angle(u[:,0])
	cos_a = cosined_hemisphere_angle(u[:,0])

	z_u = uni[:, 2]
	z_c = cos[:, 2]

	print('on hemisphere')
	for alpha in np.linspace(0.1, 1, 10):
		sum_u = np.mean(mfgeo.ggx.ndf(np.arccos(z_u), alpha)*z_u) * 2*np.pi
		sum_c = np.mean(mfgeo.ggx.ndf(np.arccos(z_c), alpha)) * np.pi
		print(f'{alpha:.1f} {sum_u:.10f} {sum_c:.10f} | {np.abs(1-sum_u):.10f} {np.abs(1-sum_c):.10f}')

	print()

	a_u = uniform_hemisphere_angle(u.reshape((-1)))
	a_c = cosined_hemisphere_angle(u.reshape((-1)))

	print('angle')
	for alpha in np.linspace(0.1, 1, 10):
		sum_u = np.mean(mfgeo.ggx.ndf(a_u, alpha)*np.cos(a_u)) * 2*np.pi
		sum_c = np.mean(mfgeo.ggx.ndf(a_c, alpha)) * np.pi
		print(f'{alpha:.1f} {sum_u:.10f} {sum_c:.10f} | {np.abs(1-sum_u):.10f} {np.abs(1-sum_c):.10f}')


	print(end='', flush=True)


	fig, ax = plt.subplots(1,1, subplot_kw=dict(projection='3d'), constrained_layout=True)
	n = 800
	ax.scatter(u[:n, 0], u[:n, 1], 0)
	ax.scatter(uni[:n, 0], uni[:n, 1], uni[:n, 2], label='uniform')
	ax.scatter(cos[:n, 0], cos[:n, 1], cos[:n, 2], label='cosined')

	plt.legend()
	plt.show()
