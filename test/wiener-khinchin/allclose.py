import numpy as np
import os
import __main__

def load(i, name):
	cur, _ = os.path.split(__main__.__file__)
	return np.load(os.path.join(cur, 'result', i, f'{name}.npy'))


if __name__ == '__main__':
	import sys
	assert len(sys.argv) == 4
	_, a, b, name = sys.argv
	print(np.allclose(load(a, name), load(b, name)))
