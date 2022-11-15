import os
import __main__
from datetime import datetime

def out(file=''):
	d, f = os.path.split(__main__.__file__)
	now = str(datetime.now().timestamp()).replace('.','').ljust(16,'0')
	p = os.path.join(d, 'result', f.replace('.py', ''), now)
	os.makedirs(p, exist_ok=True)
	return os.path.join(p, file)

def cur():
	d, _ = os.path.split(__main__.__file__)
	return d
