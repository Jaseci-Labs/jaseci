"""BCSAI runner scripts."""

import sys
from multiprocessing import cpu_count
from os import getenv

from gunicorn.app.wsgiapp import run as grun

from uvicorn import run as urun


def dev() -> None:
    """Run dev BCSAI BE."""
    workers = int(workers) if (workers := getenv("WORKER")) else ((cpu_count() * 2) + 1)

    urun(
        "jac_splice_orc.main:app",
        host=getenv("HOST", "0.0.0.0"),
        port=int(getenv("PORT", "8000")),
        reload=workers < 2,
        workers=workers,
    )


def prod() -> None:
    """Run prod BCSAI BE."""
    sys.argv = [
        "gunicorn",
        "-b",
        f'{getenv("HOST", "0.0.0.0")}:{getenv("PORT", "8000")}',
        "-w",
        getenv("WORKER", str((cpu_count() * 2) + 1)),
        "-k",
        "uvicorn.workers.UvicornWorker",
        "jac_splice_orc.main:app",
    ]
    grun()
