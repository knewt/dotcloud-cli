#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'dotcloud2',
    author = 'dotCloud Inc.',
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
