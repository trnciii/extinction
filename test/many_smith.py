import extinction, numpy as np
from matplotlib import pyplot as plt
from extinction.bruteforce import ggx_smith_g1

n = 1000

for alpha in np.linspace(0.1, 1, 10):
	steps = 1000
	angle = np.linspace(1/steps, np.pi/2, steps)
	smith = ggx_smith_g1(angle, alpha)

	plt.plot(angle, smith, label=f'{alpha:.1}')

plt.legend()
plt.savefig('result/smith.png')
plt.show()