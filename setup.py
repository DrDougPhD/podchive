#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='Podchive',
    version='0.2.0',
    description='Utility to download all episodes of a podcast',
    author='Doug McGeehan',
    author_email='doug@kmnr.org',
    packages=[
        'podchive',
        'podchive.commands',
    ],
)