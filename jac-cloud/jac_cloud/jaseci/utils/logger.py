"""Jaseci Log Handlers."""

from datetime import time as dtime
from enum import IntEnum
from io import text_encoding
from logging import FileHandler, LogRecord, getLogger
from logging.handlers import (
    BaseRotatingHandler,
    RotatingFileHandler,
    TimedRotatingFileHandler,
)
from os import getenv, remove, rename, stat
from os.path import exists, isfile
from pathlib import Path
from re import ASCII, compile
from stat import ST_MTIME
from time import gmtime, localtime, strftime, time as ttime
from typing import Any

from ecs_logging import StdlibFormatter


class MixedTimedRotatingFileHandler(TimedRotatingFileHandler, RotatingFileHandler):
    """Merge TimedRotatingFileHandler and RotatingFileHandler."""

    # mypy bug: Incompatible types in assignment
    # (expression has type "int", base class "RotatingFileHandler" defined the type as "str")
    # even RotatingHandler declared as int
    maxBytes: int  # type: ignore[assignment] # noqa: N815

    def __init__(
        self,
        filename: str,
        when: str = "h",
        interval: int = 1,
        max_bytes: int = 0,
        backup_count: int = 0,
        encoding: str | None = None,
        delay: bool = False,
        utc: bool = False,
        at_time: dtime | None = None,
        errors: str | None = None,
    ) -> None:
        """Override __init__."""
        encoding = text_encoding(encoding)
        BaseRotatingHandler.__init__(
            self, filename, "a", encoding=encoding, delay=delay, errors=errors
        )

        file_path = Path(self.baseFilename)
        self.file_folder = file_path.parent.absolute()
        self.file_name = file_path.stem
        self.file_ext = file_path.suffix

        self.maxBytes: int = max_bytes
        self.when = when.upper()
        self.backupCount = backup_count
        self.utc = utc
        self.atTime = at_time
        if self.when == "S":
            self.interval = 1
            self.suffix = "%Y-%m-%d-%H-%M-%S"
            ext_match = r"(?<!\d)\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(?!\d)"
        elif self.when == "M":
            self.interval = 60
            self.suffix = "%Y-%m-%d-%H-%M"
            ext_match = r"(?<!\d)\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(?!\d)"
        elif self.when == "H":
            self.interval = 60 * 60
            self.suffix = "%Y-%m-%d-%H"
            ext_match = r"(?<!\d)\d{4}-\d{2}-\d{2}_\d{2}(?!\d)"
        elif self.when == "D" or self.when == "MIDNIGHT":
            self.interval = 60 * 60 * 24
            self.suffix = "%Y-%m-%d"
            ext_match = r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)"
        elif self.when.startswith("W"):
            self.interval = 60 * 60 * 24 * 7
            if len(self.when) != 2:
                raise ValueError(
                    f"You must specify a day for weekly rollover from 0 to 6 (0 is Monday): {self.when}"
                )
            if self.when[1] < "0" or self.when[1] > "6":
                raise ValueError(
                    f"Invalid day specified for weekly rollover: {self.when}"
                )
            self.dayOfWeek = int(self.when[1])
            self.suffix = "%Y-%m-%d"
            ext_match = r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)"
        else:
            raise ValueError(f"Invalid rollover interval specified: {self.when}")

        self.extMatch = compile(ext_match, ASCII)
        self.interval = self.interval * interval
        filename = self.baseFilename
        if exists(filename):
            t = stat(filename)[ST_MTIME]
        else:
            t = ttime()
        self.rolloverAt = self.computeRollover(int(t))

    def build_file_name(self, prefix: str, part: int) -> str:
        """Override rotation_filename."""
        name = f"{self.file_folder}/{prefix}-{self.file_name}-{part}{self.file_ext}"

        if not callable(self.namer):
            return name
        else:
            return self.namer(name)

    def doRollover(self) -> None:  # noqa: N802
        """Override doRollover."""
        current_time = int(ttime())
        t = self.rolloverAt - self.interval
        if self.utc:
            time_tuple = gmtime(t)
        else:
            time_tuple = localtime(t)
            dst_now = localtime(current_time)[-1]
            dst_then = time_tuple[-1]
            if dst_now != dst_then:
                if dst_now:
                    addend = 3600
                else:
                    addend = -3600
                time_tuple = localtime(t + addend)
        prefix = strftime(self.suffix, time_tuple)

        if self.stream:
            self.stream.close()
            self.stream = None  # type: ignore[assignment]
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.build_file_name(prefix, i)
                dfn = self.build_file_name(prefix, i + 1)
                if exists(sfn):
                    if exists(dfn):
                        remove(dfn)
                    rename(sfn, dfn)
            dfn = self.build_file_name(prefix, 1)
            if exists(dfn):
                remove(dfn)
            self.rotate(self.baseFilename, dfn)
        else:
            part = 1
            while True:
                dfn = self.build_file_name(prefix, part)
                if not exists(dfn):
                    self.rotate(self.baseFilename, dfn)
                    break
                part += 1

        if not self.delay:
            self.stream = self._open()

    def shouldRollover(self, record: LogRecord) -> bool:  # noqa: N802
        """Override shouldRollover."""
        t = int(ttime())
        if exists(self.baseFilename) and not isfile(self.baseFilename):
            self.rolloverAt = self.computeRollover(t)
            return False
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return True
        if t >= self.rolloverAt:
            self.rolloverAt = self.computeRollover(t)
            return True
        return False


class Level(IntEnum):
    """Log Level Enum."""

    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0


logger = getLogger(getenv("LOGGER_NAME", "app"))
logger.setLevel(Level[getenv("LOGGER_LEVEL", "DEBUG")].value)

if getenv("ELASTIC_LOGGER") == "true":
    handler = FileHandler(getenv("LOGGER_FILE_PATH", "elastic-log.json"))
    handler.setFormatter(StdlibFormatter())
    logger.addHandler(handler)
else:
    handler = MixedTimedRotatingFileHandler(
        getenv("LOGGER_FILE_PATH", "jac-cloud.log"),
        when="d",
        backup_count=int(getenv("LOGGER_DAILY_MAX_FILE", "-1")),
        max_bytes=int(getenv("LOGGER_MAX_FILE_SIZE", "10000000")),
    )
    handler.setFormatter(StdlibFormatter())
    logger.addHandler(handler)


def log_entry(
    api: str, caller: str | None, payload: dict[str, Any], node: str | None = None
) -> dict[str, Any]:
    """Log metadata on entry."""
    log: dict[str, Any] = {
        "api_name": api,
        "caller_name": caller,
        "payload": payload,
        "entry_node": node,
    }
    msg = str(
        f"Incoming call from {log["caller_name"]}"
        f" to {log["api_name"]}"
        f" with payload: {log["payload"]}"
        f" at entry node: {log["entry_node"]}"
    )
    log["extra_fields"] = list(log.keys())
    logger.info(msg, extra=log)

    return log


def log_exit(response: dict[str, Any], log: dict[str, Any] | None = None) -> None:
    """Log metadata on exit."""
    log = log or {}
    log["api_response"] = response
    log["extra_fields"] = list(log.keys())
    log_msg = str(
        f"Returning call from {log["caller_name"]}"
        f" to {log["api_name"]}"
        f" with payload: {log["payload"]}"
        f" at entry node: {log["entry_node"]}"
        f" with response: {log["api_response"]}"
    )
    logger.info(
        log_msg,
        extra=log,
    )
