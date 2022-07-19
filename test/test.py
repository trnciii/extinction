import visibility, numpy as np

print(visibility.add(1,3))

ar = np.arange(10, dtype=np.float32)
print(ar)
visibility.call_kernel(ar)
print(ar)
