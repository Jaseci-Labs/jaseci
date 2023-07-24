"""Built in actions for Jaseci"""
import mimetypes

from requests import get
from jaseci.jsorc.live_actions import jaseci_action


@jaseci_action(act_group=["fh"])
def load(path: str, meta: dict = {}):
    """temp"""
    from jaseci.utils.file_handler import FileHandler

    return meta["h"].add_file_handler(FileHandler.fromPath(path))


@jaseci_action(act_group=["fh"])
def new(
    name: str,
    content_type: str = None,
    field: str = None,
    persist: bool = False,
    meta: dict = {},
):
    """temp"""
    from jaseci.utils.file_handler import FileHandler

    return meta["h"].add_file_handler(
        FileHandler(name=name, content_type=content_type, field=field, persist=persist)
    )


@jaseci_action
def guess_type(filename: str) -> tuple:
    """temp"""
    return mimetypes.guess_type(filename)


@jaseci_action(act_group=["fh"])
def update(
    id: str,
    name: str = None,
    content_type: str = None,
    field: str = None,
    persist: bool = None,
    meta: dict = {},
):
    """temp"""
    from jaseci.utils.file_handler import FileHandler

    file_handler: FileHandler = meta["h"].get_file_handler(id)
    if name:
        file_handler.name = name
        if not content_type:
            file_handler.content_type = mimetypes.guess_type(name)[0]

    if content_type:
        file_handler.content_type = content_type

    if field:
        file_handler.field = field

    if persist != None:
        file_handler.persist = persist

    return file_handler.attr()


@jaseci_action(act_group=["fh"])
def read(
    id: str, offset: int = None, mode: str = "r", encoding: str = None, meta: dict = {}
):
    """temp"""
    return meta["h"].get_file_handler(id).read(offset, mode, encoding)


@jaseci_action(act_group=["fh"])
def seek(id: str, offset: int, whence: int = 0, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).seek(offset, whence)


@jaseci_action(act_group=["fh"])
def open(id: str, mode: str = "r", encoding: str = None, meta: dict = {}, **kwargs):
    """temp"""
    meta["h"].get_file_handler(id).open(mode, encoding, False, **kwargs)


@jaseci_action(act_group=["fh"])
def is_open(id: str, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).is_open()


@jaseci_action(act_group=["fh"])
def exists(id: str, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).exists()


@jaseci_action(act_group=["fh"])
def write(id: str, content: str, meta: dict = {}):
    """temp"""
    meta["h"].get_file_handler(id).write(content)


@jaseci_action(act_group=["fh"])
def flush(id: str, meta: dict = {}):
    """temp"""
    meta["h"].get_file_handler(id).flush()


@jaseci_action(act_group=["fh"])
def close(id: str, meta: dict = {}):
    """temp"""
    meta["h"].get_file_handler(id).close()


@jaseci_action(act_group=["fh"])
def detach(id: str, persist: bool = None, meta: dict = {}):
    """temp"""
    from jaseci.utils.file_handler import FileHandler

    file_handler: FileHandler = meta["h"].pop_file_handler(id)
    file_info = file_handler.attr()

    if (persist is None and not file_handler.persist) or persist is False:
        file_handler.delete()
    else:
        file_handler.close()

    return file_info


@jaseci_action(act_group=["fh"])
def delete(id: str, meta: dict = {}):
    """temp"""
    meta["h"].pop_file_handler(id).delete()


@jaseci_action(act_group=["fh"])
def attr(id: str, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).attr()


@jaseci_action(act_group=["fh"])
def to_bytes(id: str, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).to_bytes()


@jaseci_action(act_group=["fh"])
def to_base64(id: str, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).to_base64()


@jaseci_action(act_group=["fh"])
def to_json(id: str, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).to_json()


@jaseci_action(act_group=["fh"])
def dump_json(id: str, json, indent: int = None, meta: dict = {}):
    """temp"""
    meta["h"].get_file_handler(id).dump_json(json, indent)


@jaseci_action(act_group=["fh"])
def download(url: str, header: dict = {}, meta: dict = {}):
    """Standard built in for download file from url"""
    from jaseci.utils.file_handler import FileHandler

    tmp = FileHandler("tmp")
    meta["h"].add_file_handler(tmp)

    with get(url, stream=True, headers=header) as res:
        res.raise_for_status()
        tmp.open("wb")
        for chunk in res.iter_content(chunk_size=8192):
            tmp.buffer.write(chunk)
        tmp.close()

    return tmp.id
