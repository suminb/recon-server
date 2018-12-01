#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

import recon


def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except:
        return '(Could not read from README.rst)'


setup(
    name='recon',
    version=recon.__version__,
    description='',
    long_description=readme(),
    url='http://github.com/suminb/recon-server',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'recon = recon.__main__:cli'
        ]
    },
)
