import os, __main__, json

here, _ = os.path.split(__main__.__file__)
sources = os.path.join(here, '../wiener-khinchin/result')
blend = os.path.join(here, 'sphere.blend')

os.system(f'python3 {os.path.join(here, "../wiener-khinchin/index.py")} clean')

for i in os.listdir(sources):
	d = os.path.join(sources, i)

	with open(os.path.join(d, 'meta.json')) as f:
		meta = json.load(f)

	alpha = meta['alpha']
	_type = meta['type']

	out = os.path.join(here, f'result/{alpha:.2f}_####_{_type}')

	print(d)
	print(out)
	print(flush=True)

	for f in range(4):
		os.system(f'blender -b {blend} -o {out} -f {f} --visibility {d}')