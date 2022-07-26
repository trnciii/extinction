from extinction.bruteforce import ggx_ndf, ggx_smith_g1
from extinction import figurateur
import numpy as np
from matplotlib import pyplot as plt


ref_g1 = [9.4031686e-01, 9.3310797e-01, 9.2485082e-01, 9.1534841e-01, 9.0435863e-01,
			 8.9158219e-01, 8.7664890e-01, 8.5909742e-01, 8.3835226e-01, 8.1369340e-01,
			 7.8421932e-01, 7.4880326e-01, 7.0604056e-01, 6.5419233e-01, 5.9112519e-01,
			 5.1425743e-01, 4.2051861e-01, 3.0633566e-01, 1.6765384e-01, 1.0861372e-06]
ref_arngle = np.linspace(np.pi/3, np.pi/2, 20)

g = ggx_smith_g1(ref_arngle, 0.1**0.5)
print(g)
print(ref_g1)
# assert np.allclose(g, ref_g1, atol=1e-2)


# seems to be matching https://www.researchgate.net/figure/Longer-tail-of-GG-X-distribution-shown-for-alpha-value-of-04_fig6_350052593
scale = 0.4
theta = np.linspace(1/100, np.pi/2, 100)
D = ggx_ndf(theta, scale)
G1 = ggx_smith_g1(theta, scale)


plt.plot(theta, D, label=f'D in angular space. a={scale}')
plt.plot(theta, G1, label=f'G1 in angular space. a={scale}')
plt.plot(ref_arngle, ref_g1, label=f'mitsuba a=0.1')
plt.plot(ref_arngle, g, label='mine a=0.1**0.5')


plt.legend()
plt.savefig('result/distribution.png', dpi=150)
plt.show()
