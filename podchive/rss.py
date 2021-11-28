import datetime
import logging
import pathlib
import urllib.parse

import feedparser
import pathvalidate
import requests

from .utilities import AutoCreatedDirectoryPath

logger = logging.getLogger(__name__)


class PodcastRSSEntry(object):
    def __init__(self, rss_entry, podcast):
        self.podcast = podcast
        self.raw_rss_entry = rss_entry

        self.title = rss_entry['title']

        subtitle = rss_entry.get('subtitle').strip().split('\n')
        if len(subtitle) > 1 and len(subtitle[0]) < 120:
            first_line = subtitle[0]
            self.title += f' - {first_line}'

        self.published_date = datetime.date(*rss_entry['published_parsed'][:3])

        links = sorted(
            filter(lambda link: 'length' in link,
                   rss_entry['links']),
            key=lambda link: int(link['length'])
        )
        audio_links = [
            link['href']
            for link in links
            if 'audio' in link['type']
        ]
        if len(audio_links) > 1:
            logger.exception(f'Unexpected number of files found for podcast episode! {len(audio_links)}')
            import sys
            sys.exit(1)

        self.audio_url = urllib.parse.urlparse(audio_links[-1])
        logger.debug(f'Chosen URL: {self.audio_url}')

    @property
    def filename(self):
        download_extension = pathlib.Path(self.audio_url.path).suffix
        filename = f'{self.published_date} - {pathvalidate.sanitize_filename(self.title)}{download_extension}'
        return filename

    def download(self, to):
        url = urllib.parse.urlunparse(self.audio_url)
        path = AutoCreatedDirectoryPath(to.directory/self.podcast.title)/self.filename

        logger.info(f'Downloading {url} to {path}')

        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with path.open('wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            # size = response.headers.get('Content-Length')
            # progress_max_val = int(size) if size is not None else progressbar.UnknownLength
            # count = 0
            # with progressbar.ProgressBar(max_value=progress_max_val) as progress, path.open('wb') as file:
            #     for chunk in response.iter_content(chunk_size=8192):
            #         count += len(chunk)
            #         progress.update(count)
            #
            #         file.write(chunk)
        return path


class PodcastRSSFeed(object):
    """
    Base class for podcasts that offer an RSS feed of their episodes.
    """

    def __init__(self, url: urllib.parse.ParseResult):
        self.rss_feed_url = url
        self.cached_feed = None

    @property
    # TODO: decorate with a cached?
    def feed(self):
        """JSON representation of podcast's RSS feed."""
        # import json
        # feed_cache_file = AutoCreatedDirectoryPath('.cache') / f'{self.__class__.__name__}.json'
        # if feed_cache_file.exists():
        #     logger.debug(f'Loading RSS feed from cache: {feed_cache_file}')
        #     return json.load(feed_cache_file.open())
        if self.cached_feed is None:
            self.cached_feed = feedparser.parse(urllib.parse.urlunparse(self.rss_feed_url))
        return self.cached_feed

    @property
    def title(self):
        """Title of podcast."""
        return self.feed['feed']['title']

    @property
    def download_directory_name(self):
        """File-system safe directory name for this podcast's downloaded files."""
        return pathvalidate.sanitize_filename(self.title)

    def __iter__(self):
        for rss_raw_entry in self.feed['entries']:
            yield PodcastRSSEntry(rss_entry=rss_raw_entry, podcast=self)

    def __repr__(self):
        return str(self)
