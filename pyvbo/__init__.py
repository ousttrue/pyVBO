from logging import getLogger, Handler, DEBUG, WARNING, ERROR
logger = getLogger(__name__)

import pathlib
from . import pmd


def load(path: pathlib.Path):
    return load_bytes(path.read_bytes(), path)


def load_bytes(data: bytes, path: pathlib.Path):
    if data[0:3] == b'Pmd':
        return pmd.load_bytes(data, path)
    else:
        raise NotImplementedError()
