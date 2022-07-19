import extinction, numpy as np

print(extinction.add(1,3))

ar = np.arange(10, dtype=np.float32)
print(ar)
extinction.call_kernel(ar)
print(ar)
