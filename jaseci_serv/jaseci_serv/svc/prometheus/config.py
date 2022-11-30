import os

PROMON_CONFIG = {
    "enabled": True,
    "quiet": False,
    "url": f'http://{os.getenv("PROMON_HOST", "localhost")}:{os.getenv("PROMON_PORT", "9090")}',
}
