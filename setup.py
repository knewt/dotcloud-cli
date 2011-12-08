#!/usr/bin/env python

from setuptools import setup
VERSION = '0.9.0'

setup(
    name = 'dotcloud2',
    author = 'dotCloud Inc.',
    version = VERSION,
    packages = [
        'dotcloud.ui',
        'dotcloud.client'
    ],
    scripts  = [
        'bin/dotcloud2'
    ],
    install_requires = ['argparse'],
    zip_safe = False
)
