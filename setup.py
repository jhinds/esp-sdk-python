#!/usr/bin/env python
from setuptools import setup
import sys
if sys.version_info[0] == 2:
    from io import open

packages = [
    'esp',
    'esp.packages',
    'esp.packages.requests'
]

with open('./README.rst', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='esp',
    version='0.1.0',
    description='Evident Security Platform (ESP) SDK for Python',
    long_description=readme,
    author='Kyle Terry',
    author_email='kyle@evident.io',
    packages=packages,
    py_modules=['esp'],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
    install_requires=[
        'requests',
        'six',
        'coverage',
        'mock',
        'nose',
        'unittest2',
    ],
)
