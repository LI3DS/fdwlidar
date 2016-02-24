import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def find_version(*file_paths):
    """
    see https://github.com/pypa/sampleproject/blob/master/setup.py
    """
    with open(os.path.join(here, *file_paths), 'r') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string. "
                       "Should be at the first line of __init__.py.")

setup(
    name='fdwlidar',
    version=find_version('fdwlidar', '__init__.py'),
    description="fdwlidar",
    url='',
    author='oslandia',
    author_email='contact@oslandia.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages()
)