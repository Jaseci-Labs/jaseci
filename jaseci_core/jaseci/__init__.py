from os.path import dirname, join
from .jsorc_settings import JsOrcSettings
from .jsorc import State, JsOrc


def get_ver():
    with open(join(dirname(__file__), "VERSION")) as version_file:
        return version_file.read().strip()


__version__ = get_ver()
__creator__ = "Jason Mars and friends"
__url__ = "https://jaseci.org"
__all__ = ["State", "JsOrc", "JsOrcSettings"]


def load_standard():
    import jaseci.actions.standard.net  # noqa
    import jaseci.actions.standard.rand  # noqa
    import jaseci.actions.standard.request  # noqa
    import jaseci.actions.standard.std  # noqa
    import jaseci.actions.standard.file  # noqa
    import jaseci.actions.standard.vector  # noqa
    import jaseci.actions.standard.date  # noqa
    import jaseci.actions.standard.jaseci  # noqa
    import jaseci.actions.standard.mail  # noqa
    import jaseci.actions.standard.task  # noqa
    import jaseci.actions.standard.internal  # noqa
    import jaseci.actions.standard.zlib  # noqa
    import jaseci.actions.standard.webtool  # noqa
    import jaseci.actions.standard.elastic  # noqa
    import jaseci.actions.standard.url  # noqa
    import jaseci.actions.standard.stripe  # noqa


load_standard()
