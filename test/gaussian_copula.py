import numpy as np, scipy
from mfgeo import figurateur
from mfgeo.autocorrelation import acf
from matplotlib import pyplot as plt

ndim = 100

ac_ref = np.array([1 if i ==0 else 0.8 if i==1 else 0 for i in range(ndim)])
print('ac_ref')
print(ac_ref)

sigma = np.array([ np.concatenate((np.flip(ac_ref[1:i+1]), ac_ref[:ndim-i]))  for i in range(ndim)])
print('sigma')
print(sigma)

A = scipy.linalg.sqrtm(sigma)

Z = np.random.multivariate_normal(np.zeros(ndim), A, 100)
print('Z')
print(Z)

ac_sampled = np.array([acf(z) for z in Z])
print('ac_sampled')
print(ac_sampled)


print(flush=True)


f, (top, bottom) = plt.subplots(2,1, constrained_layout=True)

figurateur.cloud(top, np.linspace(0, 1, Z.shape[1]), Z)

x = np.linspace(0, 1, ac_sampled.shape[1])
figurateur.cloud(bottom, x, ac_sampled)
bottom.plot(x, np.mean(ac_sampled, axis=0), label='mean', color='yellow')
bottom.plot(np.linspace(0, 1, ac_ref.shape[0]), ac_ref, label='reference')
bottom.legend()

plt.show()
