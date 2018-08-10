#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download episodes of 'My Brother, My Brother, and Me' from
http://maximumfun.org/shows/my-brother-my-brother-and-me"""

import logging
import argparse
import sys

import config

logger = logging.getLogger(__name__)


def cli(subcommand):
    '''Add command-line arguments to this subcommand
    '''
    subcommand.add_argument(
        '-o', '--output-directory',
        type=argparse.FileType('r'),
        default=config.defaults.output_directory,
        help='input file',
    )
    subcommand.set_defaults(func=main)


def main(args):
    # read from file system to learn about albums that have been ripped
    raise NotImplementedError('{0} {1} subcommand is not implemented!'.format(
        *sys.argv
    ))
