import os, __main__, json
import _path as path

here = path.here()
sources = path.sources()
blend = './bd/Dragon.blend'

os.system(f'python3 {os.path.join(here, "../wiener-khinchin/index.py")} clean')

a = {
	'alpha': 0.50,
	'type': 'white',
	'memory': '1'
}

b = {
	'alpha': 0.50,
	'type': 'cos',
	'memory': '1'
}

for i in [path.load_meta(x['alpha'], x['type'], x['memory'])['id'] for x in [a, b]]:
	d = os.path.join(sources, i)

	with open(os.path.join(d, 'meta.json')) as f:
		meta = json.load(f)

	if meta['memory']>1: continue

	out = os.path.join('teaser', f'{meta["alpha"]:.2f}_{meta["type"]}_{meta["memory"]}', '##')

	print('source', d)
	print('out   ', out)
	print(flush=True)

	os.system(f'blender -b {blend} -o {out} -a --visibility {d}')
