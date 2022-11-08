from . import cpu

try:
	from . import gpu
	gpu_found = True
except ImportError:
	gpu_found = False

from .cpu import g1_distant, g1_distant_single