from jaseci.jsorc.live_actions import jaseci_action
from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.storage_svc import StorageService


def storage():
    return JsOrc.svc("store", StorageService)


@jaseci_action()
def upload(file: str, provider: str = None, container: str = None, meta: dict = {}):
    """temp"""
    from jaseci.utils.file_handler import FileHandler

    file_handler: FileHandler = meta["h"].get_file_handler(file)

    return storage().upload(file=file_handler, provider=provider, container=container)


@jaseci_action()
def download(file: str, provider: str = None, container: str = None, meta: dict = {}):
    """temp"""
    return meta["h"].add_file_handler(storage().download(file, provider, container))


@jaseci_action()
def delete(file: str, provider: str = None, container: str = None):
    """temp"""
    return storage().delete(file, provider, container)


@jaseci_action()
def create_container(name: str, provider: str = None):
    """temp"""
    return storage().create_container(name, provider) != None


@jaseci_action()
def has_container(name: str, provider: str = None):
    """temp"""
    return storage().has_container(name, provider)


@jaseci_action()
def delete_container(name: str, provider: str = None):
    """temp"""
    return storage().delete_container(name, provider)
