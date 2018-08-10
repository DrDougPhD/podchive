#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYNOPSIS

	python podchive.py [-h,--help] [-v,--verbose]


DESCRIPTION

	Concisely describe the purpose this script serves.


ARGUMENTS

	-h, --help          show this help message and exit
	-v, --verbose       verbose output


AUTHOR

	Doug McGeehan


LICENSE

	Copyright 2018 Doug McGeehan - GNU GPLv3

"""

__appname__ = "podchive"
__author__ = "Doug McGeehan"
__version__ = "0.0pre0"
__license__ = "GNU GPLv3"
__indevelopment__ = True        # change this to false when releases are ready


import argparse
import logging

import cli

logger = logging.getLogger('podchive')


# Uncomment the import below and add the module corresponding to a subcommand
from podchive.commands import subcommand
enabled_subcommands = [
    subcommand
]

def main(args):
    '''ADD DESCRIPTION HERE'''
    args.func(args=args)


def cli_arguments():
    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=__indevelopment__, help='verbose output')

    cli.add_subcommands(subcmd_modules=enabled_subcommands,
                        parser=parser)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = cli_arguments()
    with cli.prepare(app='podchive', args=args):
        main(args=args)
