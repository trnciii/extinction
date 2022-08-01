import sys

try:
    from skbuild import setup
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise

from setuptools import find_packages

setup(
    name="extinction",
    version="0.0.1",
    packages=find_packages(),
    cmake_install_dir="extinction",
    include_package_data=True,
    python_requires=">=3.8",
)