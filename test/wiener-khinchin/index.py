import os, json, __main__

here, _ = os.path.split(__main__.__file__)
result = os.path.join(here, 'result')

data = {}
error = []

for d in os.listdir(result):
	try:
		if os.path.isdir(os.path.join(result, d)):
			with open(os.path.join(result, d, 'meta.json')) as f:
				data[d] = json.load(f)
	except Exception as e:
		error.append((d, e))

if len(error)>0:
	print('Error')
	for i, e in error:
		print(i)
		print(f'\t{e}')

with open(os.path.join(here, 'index.js'), 'w') as f:
	f.write(f'const table = {json.dumps(data, indent=2)};')
