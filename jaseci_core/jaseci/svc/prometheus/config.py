import os


PROMON_CONFIG = {
    "enabled": False,
    "quiet": True,
    "url": (
        f'http://{os.getenv("PROMON_HOST", "localhost")}'
        f':{os.getenv("PROMON_PORT", "9090")}'
    ),
}
