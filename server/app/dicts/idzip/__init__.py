from .api import IdzipFile, compress, decompress
from .api import IdzipWriter as Writer
from .api import open as dzopen
from .compressor import MAX_MEMBER_SIZE, compress_member

# get a copy of the open standard file open before overwriting
fopen = open
open = dzopen


__all__ = [
    "MAX_MEMBER_SIZE", "compress_member",
    "IdzipFile", "compress", "decompress",
    "Writer", "open",
]
