from os.path import dirname, join


def get_ver():
    with open(join(dirname(__file__), "VERSION")) as version_file:
        return version_file.read().strip()


__version__ = get_ver()
__creator__ = "Jason Mars and friends"
__url__ = "https://jaseci.org"
