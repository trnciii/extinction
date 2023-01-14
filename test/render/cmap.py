from matplotlib import pyplot as plt
import numpy as np

fig, ax = plt.subplots(1,1, figsize=(5,0.7), constrained_layout=True)
w, h = 256, 43
cm = np.tile(np.arange(-w, w), h).reshape((h, -1))
ax.imshow(cm, cmap='seismic')
ax.get_yaxis().set_visible(False)
ax.get_xaxis().set_ticks([0, w, 2*w-1], ['-5%', '0%', '+5%'])
plt.savefig('compared/cmap.jpg')