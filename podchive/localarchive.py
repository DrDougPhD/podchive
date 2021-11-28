import pathlib

from podchive.rss import PodcastRSSEntry


class LocalPodcastArchive(object):
    def __init__(self, directory: pathlib.Path):
        directory.mkdir(parents=True, exist_ok=True)
        self.directory = directory

    def __contains__(self, episode: PodcastRSSEntry) -> bool:
        podcast_directory = self.directory / episode.podcast.title
        if not podcast_directory.is_dir():
            return False

        podcast_file = podcast_directory / episode.filename
        if not podcast_file.exists():
            return False

        return True
