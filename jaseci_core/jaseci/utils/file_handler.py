import mimetypes
from os import unlink
from io import BytesIO
from uuid import uuid4
from base64 import b64encode
from tempfile import _TemporaryFileWrapper
import re

filename_from_disposition = re.compile(r"filename=(['\"])(.*?)\1")


class FileHandler:
    ###################################################
    #                     BUILDER                     #
    ###################################################

    def __init__(
        self,
        name: str = None,
        content_type: str = None,
        field: str = None,
        persist: bool = False,
    ):
        self.id = str(uuid4())
        self.name = name
        self.content_type = content_type or mimetypes.guess_type(name)[0]
        self.field = field
        self.absolute_name = f"{self.id}-{name}"
        self.absolute_path = self.absolute_name
        self.persist = persist
        self.buffer = None

    @classmethod
    def fromTemporaryFileWrapper(
        cls,
        file: _TemporaryFileWrapper,
        name: str,
        content_type: str,
        field: str = None,
    ):
        file_handler = cls(name, content_type, field)
        file_handler.absolute_path = file.name

        file._closer.delete = False
        file.close()

        return file_handler

    @classmethod
    def fromBytesIO(
        cls, file: BytesIO, name: str, content_type: str, field: str = None
    ):
        file_handler = cls(name, content_type, field)

        with open(file_handler.absolute_path, "wb") as f:
            f.write(file.getbuffer())
        file.close()

        return file_handler

    @classmethod
    def fromRequest(cls, content: bytes, content_disposition: str):
        name = "tmp"
        searcher = filename_from_disposition.search(content_disposition)
        if len(searcher.groups()):
            name = searcher.group(2)

        file_handler = cls(name)

        with open(file_handler.absolute_path, "wb") as f:
            f.write(content)

        return file_handler

    ###################################################
    #                     CONTROL                     #
    ###################################################

    def read(self, offset: int = None) -> str:
        if self.buffer:
            if offset != None:
                self.buffer.seek(offset)
            content = self.buffer.read()
        else:
            self.open()
            content = self.buffer.read()
            self.close()

        return content

    def open(
        self, mode: str = "r", encoding: str = "utf-8", detached: bool = False, **kwargs
    ):
        if detached:
            return open(self.absolute_path, mode, encoding=encoding, **kwargs)

        if not self.buffer:
            self.buffer = open(self.absolute_path, mode, encoding=encoding, **kwargs)

    def write(self, content: str):
        if self.buffer:
            self.buffer.write(content)

    def seek(self, offset: int, whence: int = 0):
        if self.buffer:
            self.buffer.seek(offset, whence)

    def flush(self):
        if self.buffer:
            self.buffer.flush()

    def close(self):
        if self.buffer:
            self.buffer.close()
            self.buffer = None

    def delete(self):
        self.close()
        try:
            unlink(self.absolute_path)
        except Exception:
            pass

    def base64(self, offset: int = None):
        return b64encode(self.read(offset).encode()).decode()

    def is_open(self) -> bool:
        return self.buffer != None

    def info(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "content_type": self.content_type,
            "field": self.field,
            "absolute_name": self.absolute_name,
            "absolute_path": self.absolute_path,
            "persist": self.persist,
        }
