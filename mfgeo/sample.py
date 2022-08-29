import numpy as np

def cosined_hemisphere(u):
	u1 = 2*np.pi*u[:, 1]
	r = np.sqrt(u[:, 0])
	hemi = np.empty((u.shape[0], 3))
	hemi[:, 0] = r*np.cos(u1)
	hemi[:, 1] = r*np.sin(u1)
	hemi[:, 2] = np.sqrt(1-u[:, 0])
	return hemi


def uniform_hemisphere(u):
	u1 = 2*np.pi*u[:, 1]
	r = np.sqrt(1 - u[:, 0]**2)
	uni = np.empty((u.shape[0], 3))
	uni[:, 0] = r*np.cos(u1)
	uni[:, 1] = r*np.sin(u1)
	uni[:, 2] = u[:, 0]
	return uni


if __name__ == "__main__":
	import mfgeo
	from matplotlib import pyplot as plt


	rng = np.random.default_rng()
	u = rng.uniform(size=(5000, 2))

	uni = uniform_hemisphere(u)
	cos = cosined_hemisphere(u)

	z = uni[:, 2]

	for alpha in np.linspace(0, 1, 11):
		print(f'{alpha:.2f}', np.mean(mfgeo.ggx.ndf(np.arccos(z), alpha)*z) * (2*np.pi))


	fig, ax = plt.subplots(1,1, subplot_kw=dict(projection='3d'), constrained_layout=True)
	n = 800
	ax.scatter(u[:n, 0], u[:n, 1], 0)
	ax.scatter(uni[:n, 0], uni[:n, 1], uni[:n, 2], label='uniform')
	ax.scatter(cos[:n, 0], cos[:n, 1], cos[:n, 2], label='cosined')

	plt.legend()
	plt.show()
