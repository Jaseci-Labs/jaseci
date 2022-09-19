from os.path import dirname, join


def get_ver():
    with open(join(dirname(__file__), "VERSION")) as version_file:
        return version_file.read().strip()


__version__ = get_ver()
__creator__ = "Jason Mars"
__url__ = "https://jaseci.org"


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


load_standard()
