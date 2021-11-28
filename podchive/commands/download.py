#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download episodes of a podcast given its RSS feed URL"""

import logging
import time
import urllib.parse

import progressbar

from .. import config
from ..localarchive import LocalPodcastArchive
from ..rss import PodcastRSSFeed
from ..utilities import AutoCreatedDirectoryPath

logger = logging.getLogger(__name__)


def cli(subcommand):
    '''Add command-line arguments to this subcommand
    '''
    subcommand.add_argument(
        '-u', '--rss-url',
        type=urllib.parse.urlparse,
        help=f'RSS feed URL from which to download podcast episodes',
    )
    subcommand.add_argument(
        '-o', '--output-directory',
        type=AutoCreatedDirectoryPath,
        default=config.defaults.output_directory,
        help=f'directory to download into '
             f'(default: {config.defaults.output_directory})',
    )
    subcommand.set_defaults(func=main)


def main(args):
    feed = PodcastRSSFeed(url=args.rss_url)
    local_archive = LocalPodcastArchive(directory=args.output_directory)

    episodes_to_download = [
        episode
        for episode in feed
        if episode not in local_archive
    ]

    if len(episodes_to_download) == 0:
        logger.info(f'No new episodes of "{feed.title}" to download.')
    else:
        logger.info(f'{len(episodes_to_download)} episodes to download of "{feed.title}".')

    with progressbar.ProgressBar(max_value=len(episodes_to_download)) as progress:
        for i, episode in enumerate(episodes_to_download):
            progress.update(i)
            episode.download(to=local_archive)
            time.sleep(3)