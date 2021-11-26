#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download episodes of 'My Brother, My Brother, and Me' from
http://maximumfun.org/shows/my-brother-my-brother-and-me"""

import logging

from .. import config
from ..rss import PodcastRSSFeed
from ..utilities import AutoCreatedDirectoryPath

logger = logging.getLogger(__name__)


def cli(subcommand):
    '''Add command-line arguments to this subcommand
    '''
    subcommand.add_argument(
        '-o', '--output-directory',
        type=AutoCreatedDirectoryPath,
        default=config.defaults.output_directory,
        help=f'directory to download into '
             f'(default: {config.defaults.output_directory})',
    )
    subcommand.set_defaults(func=main)


class MBMBaMDownloader(PodcastRSSFeed):
    podcast_title = 'My Brother, My Brother And Me'
    rss_feed_url = 'https://feeds.simplecast.com/wjQvYtdl'

    def __str__(self):
        return f'{self.__class__.__name__}'

    def download(self):
        """Download all podcasts episodes."""
        # import json
        # with open(f'{self.__class__.__name__}.json', 'w') as f:
        #     json.dump(self.feed, f, indent=4)
        feed = self.feed

        for entry in self:
            entry.download_to()

        return None


def main(args):
    # read from file system to learn about albums that have been ripped
    downloader = MBMBaMDownloader()
    downloader.download()
