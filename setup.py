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
    name="extinction",
    packages=['extinction'],
    package_dir={'': 'extinction'},
    cmake_install_dir="extinction/extinction",
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy',
    ],
)
