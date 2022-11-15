import os, json, __main__

here, _ = os.path.split(__main__.__file__)
result = os.path.join(here, 'result')

data = {}

for d in os.listdir(result):
	if os.path.isdir(os.path.join(result, d)):
		with open(os.path.join(result, d, 'meta.json')) as f:
			data[d] = json.load(f)

with open(os.path.join(here, 'index.js'), 'w') as f:
	f.write(f'const table = {json.dumps(data, indent=2)};')
