import os

USER = os.environ.get("POSTGRES_USER", "postgres")

DATABASE_CONFIG = {
    "enabled": True,
    "quiet": False,
    "host": os.environ.get("POSTGRES_HOST", "jaseci-db"),
    "db": os.environ.get("POSTGRES_HOST", "postgres"),
    "name": USER,
    "user": USER,
    "password": os.environ.get("POSTGRES_PASSWORD", "lifelogifyjaseci"),
    "PORT": os.getenv("POSTGRES_PORT", 5432),
}
