import logging
import pathlib

logger = logging.getLogger(__name__)


def AutoCreatedDirectoryPath(path):
    path = pathlib.Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
