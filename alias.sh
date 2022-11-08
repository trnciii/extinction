ROOT=$(dirname "$(readlink -f "$BASH_SOURCE")")
echo "root: $ROOT"
echo "os: ${OSTYPE}"

if [[ "$OSTYPE" == "darwin"* ]]; then
	alias install='python3 setup.py develop --user'
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
	alias install='python3 setup.py develop --user'
elif [[ "$OSTYPE" == "msys" ]]; then
	alias install='python3 setup.py develop'
else
	echo 'failed to set install alias'
fi
