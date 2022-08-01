import numpy as np
from . import core

from .core import visibility

ggx_smith_g1 = np.vectorize(core.ggx_smith_g1)
ggx_ndf = np.vectorize(core.ggx_ndf)
