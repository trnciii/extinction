import sys, re, os

try:
    from skbuild import setup
    import nanobind
except ImportError:
    print("The preferred way to invoke 'setup.py' is via pip, as in 'pip "
          "install .'. If you wish to run the setup script directly, you must "
          "first install the build dependencies listed in pyproject.toml!",
          file=sys.stderr)
    raise

setup(
    name="visibility",
    version="0.0.1",
    author="trnciii",
    url="https://github.com/trnciii/extinction",
    license="BSD",
    packages=['visibility'],
    package_dir={'': 'visibility'},
    cmake_install_dir="visibility/visibility",
    include_package_data=True,
    python_requires=">=3.8"
)
