import os, json

def here():
	import __main__
	return os.path.split(__main__.__file__)[0]

def sources():
	return os.path.join(here(), '../wiener-khinchin/result')

def from_meta(meta):
	return os.path.join(here(), f'images/{meta["alpha"]:.2f}_{meta["type"]}_{meta["memory"]}')

def from_spec(a, t, m):
	return os.path.join(here(), f'images/{a:.2f}_{t}_{m}')

def load_meta(a, t, m):
	with open(os.path.join(from_spec(a, t, m), 'meta.json')) as f:
		return json.load(f)

def load_npy(a, t, m, filename):
	import numpy as np
	return np.load(os.path.join(sources(), load_meta(a, t, m)['id'], filename))
