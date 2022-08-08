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
	u = rng.uniform(size=(1000, 2))

	hemi = uniform_hemisphere(u)
	chemi = cosined_hemisphere(u)


	fig, ax = plt.subplots(1,1, subplot_kw=dict(projection='3d'))
	ax.scatter(u[:, 0], u[:, 1], 0)
	ax.scatter(hemi[:, 0], hemi[:, 1], hemi[:, 2], label='uniform')
	ax.scatter(chemi[:, 0], chemi[:, 1], chemi[:, 2], label='cosined')

	plt.legend()
	plt.show()
