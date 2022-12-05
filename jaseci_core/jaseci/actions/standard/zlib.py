"""Built in actions for Jaseci"""
from jaseci.actions.live_actions import jaseci_action
from base64 import b64decode, b64encode
import zlib

import logging

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()


@jaseci_action()
def compress(data_b64: str):
    """
    Compress data
    Param 1 - data in base64

    Return - compressed data in base64
    """
    data_bytes = b64decode(data_b64.encode("ascii"))
    data_compressed_bytes = zlib.compress(data_bytes)
    data_compressed_b64 = b64encode(data_compressed_bytes).decode("ascii")
    mylogger.info(data_compressed_b64)
    return data_compressed_b64


def decompress(data_b64: str):
    """
    Decompress data
    Param 1 - data in base64

    Return - decompressed data in base64
    """
    data_bytes = b64decode(data_b64.encode("ascii"))
    data_decompressed_bytes = zlib.decompress(data_bytes)
    data_decompressed_b64 = b64encode(data_decompressed_bytes).decode("ascii")
    mylogger.info(data_decompressed_b64)
    return data_decompressed_b64
