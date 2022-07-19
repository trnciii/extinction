ROOT=$(dirname "$(realpath "$BASH_SOURCE")")
echo "root: $ROOT"

alias install='python3 -m pip install -e $ROOT'
