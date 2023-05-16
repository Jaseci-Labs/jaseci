from os.path import dirname, join


def get_ver():
    with open(join(dirname(__file__), "VERSION")) as version_file:
        return version_file.read().strip()


__version__ = get_ver()
__creator__ = "Jason Mars and friends"
__url__ = "https://jaseci.org"


def load_standard():
    import jaseci.extens.act_lib.net  # noqa
    import jaseci.extens.act_lib.rand  # noqa
    import jaseci.extens.act_lib.request  # noqa
    import jaseci.extens.act_lib.std  # noqa
    import jaseci.extens.act_lib.file  # noqa
    import jaseci.extens.act_lib.file_handler  # noqa
    import jaseci.extens.act_lib.storage  # noqa
    import jaseci.extens.act_lib.vector  # noqa
    import jaseci.extens.act_lib.date  # noqa
    import jaseci.extens.act_lib.jaseci  # noqa
    import jaseci.extens.act_lib.mail  # noqa
    import jaseci.extens.act_lib.task  # noqa
    import jaseci.extens.act_lib.internal  # noqa
    import jaseci.extens.act_lib.zip  # noqa
    import jaseci.extens.act_lib.webtool  # noqa
    import jaseci.extens.act_lib.elastic  # noqa
    import jaseci.extens.act_lib.url  # noqa
    import jaseci.extens.act_lib.stripe  # noqa
    import jaseci.extens.act_lib.regex  # noqa
    import jaseci.extens.act_lib.maths  # noqa


load_standard()
