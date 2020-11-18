import datetime
import logging
import feedparser
import pathvalidate

from podchive.utilities import AutoCreatedDirectoryPath

logger = logging.getLogger(__name__)


class PodcastRSSEntry(object):
    def __init__(self, rss_entry):
        self.title = rss_entry['title']
        self.published_date = datetime.date(*rss_entry['published_parsed'][:3])

        links = sorted(
            filter(lambda link: 'length' in link,
                   rss_entry['links']),
            key=lambda link: int(link['length'])
        )
        logger.debug(links)
        audio_links = [
            link['href']
            for link in links
            if 'audio' in link['type']
        ]
        if len(audio_links) > 1:
            logger.exception(f'Unexpected number of files found for podcast episode! {len(audio_links)}')
            import sys
            sys.exit(1)

        self.audio_url = audio_links[-1]
        logger.debug(f'Chosen URL: {self.audio_url}')

    @property
    def filename(self):
        return pathvalidate.sanitize_filename(self.title) + '.'


class PodcastRSSFeed(object):
    """
    Base class for podcasts that offer an RSS feed of their episodes.
    """

    def __init__(self):
        self.cached_feed = None

    @property
    def rss_feed_url(self):
        """URL to this podcast's RSS feed. Must be defined as a static
        variable in subclasses."""
        raise NotImplementedError(
            f'{self.__class__.__name__}.rss_feed_url is not defined! '
            f'Please set this to the RSS feed URL for this podcast.'
        )

    @property
    def podcast_title(self):
        """Podcast's title, used when searching for podcasts based on title
        in the command-line arguments."""
        raise NotImplementedError(
            f'{self.__class__.__name__}.podcast_title is not defined! '
            f'Please set this as a static variable on this subclass.'
        )

    @property
    def feed(self):
        """JSON representation of podcast's RSS feed."""
        import json
        feed_cache_file = (AutoCreatedDirectoryPath(f'.cache') / f'{self.__class__.__name__}.json')
        if feed_cache_file.exists():
            logger.debug(f'Loading RSS feed from cache: {feed_cache_file}')
            return json.load(feed_cache_file.open())

        if self.cached_feed is None:
            self.cached_feed = feedparser.parse(self.rss_feed_url)
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
            yield PodcastRSSEntry(rss_entry=rss_raw_entry)

    def __repr__(self):
        return str(self)
