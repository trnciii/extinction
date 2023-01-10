import os, __main__, json
import _path as path

here = path.here()
sources = path.sources()
blend = os.path.join(here, 'sphere.blend')

os.system(f'python3 {os.path.join(here, "../wiener-khinchin/index.py")} clean')

for i in os.listdir(sources):
	d = os.path.join(sources, i)

	with open(os.path.join(d, 'meta.json')) as f:
		meta = json.load(f)

	out = os.path.join(path.from_meta(meta), 'frame_#')

	print('source', d)
	print('out   ', out)
	print(flush=True)

	for f in range(4):
		os.system(f'blender -b {blend} -o {out} -f {f} --visibility {d}')