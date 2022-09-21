import os
import __main__

def out(file=''):
	d, f = os.path.split(__main__.__file__)
	p = os.path.join(d, 'result', f.replace('.py', ''))
	os.makedirs(p, exist_ok=True)
	return os.path.join(p, file)
