from setuptools import setup
from Cython.Build import cythonize

setup(
    name='kalaha_AI',
    ext_modules=cythonize("kalaha_new.py"),
    zip_safe=False,
)