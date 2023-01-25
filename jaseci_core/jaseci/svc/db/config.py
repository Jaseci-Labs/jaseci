import os


DB_CONFIG = {
    "enabled": True,
    "quiet": False,
    "host": os.getenv("JASECI_DB_HOST", "localhost"),
    "port": os.getenv("JASECI_DB_PORT", 6379),
    "user": os.getenv("JASECI_DB_USER", None),
    "password": os.getenv("JASECI_DB_PASSWORD", None),
    "database": os.getenv("JASECI_DB_NAME", None),
}
