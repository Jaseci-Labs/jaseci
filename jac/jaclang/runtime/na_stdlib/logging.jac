import sys;
import time;

glob:pub CRITICAL: int = 50,
     FATAL: int = 50,
     ERROR: int = 40,
     WARNING: int = 30,
     WARN: int = 30,
     INFO: int = 20,
     DEBUG: int = 10,
     NOTSET: int = 0,
     BASIC_FORMAT: str = "%(levelname)s:%(name)s:%(message)s",
     raiseExceptions: bool = True;

glob _DEFAULT_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S",
     _START_TIME: float = time.time();

glob _KIND_STDERR: int = 0,
     _KIND_STDOUT: int = 1,
     _KIND_FILE: int = 2;


obj _Names {
    has extra: dict[str, str];

    def init;
}

glob _NAMES: _Names = _Names();


def:pub getLevelName(level: int) -> str;


def:pub addLevelName(level: int, levelName: str);


def:pub getLevelNamesMapping -> dict[str, int];


def _pad3(v: int) -> str;


obj:pub LogRecord {
    has name: str,
        levelno: int,
        levelname: str,
        msg: str,
        pathname: str,
        lineno: int,
        funcName: str,
        created: float,
        msecs: float,
        relativeCreated: float;

    def init(
        name: str = "root",
        level: int = 0,
        pathname: str = "",
        lineno: int = 0,
        msg: str = "",
        args: (list[any] | None) = None,
        exc_info: (list[any] | None) = None,
        func: str = "",
        sinfo: str = ""
    );

    def getMessage -> str;
}


def _sub(text: str, token: str, value: str) -> str;


obj:pub Formatter {
    has _fmt: str,
        datefmt: str;

    def init(fmt: str = "", datefmt: str = "", style: str = "%");
    def formatTime(record: LogRecord, datefmt: str = "") -> str;
    def formatMessage(record: LogRecord) -> str;
    def format(record: LogRecord) -> str;
}


def _f6(v: float) -> str;


def _basename(path: str) -> str;


def _modname(path: str) -> str;


obj:pub Handler {
    has level: int,
        _kind: int,
        _stream: int,
        _formatter: Formatter | None,
        _closed: bool;

    def init(level: int = 0, kind: int = 0, stream: int = 0);
    def setLevel(level: int);
    def setFormatter(fmt: Formatter);
    def format(record: LogRecord) -> str;
    def emit(record: LogRecord);
    def handle(record: LogRecord) -> bool;
    def flush;
    def close;
}

glob _DEFAULT_FORMATTER: Formatter = Formatter(fmt="%(message)s");


def:pub StreamHandler(stream: str = "stderr") -> Handler;


def:pub FileHandler(
    filename: str, mode: str = "a", encoding: str = "", delay: bool = False
) -> Handler;


obj:pub Logger {
    has name: str,
        level: int,
        propagate: bool,
        disabled: bool,
        handlers: list[Handler],
        parent: Logger | None;

    def init(name: str = "root", level: int = 0);
    def setLevel(level: int);
    def addHandler(hdlr: Handler) -> None;
    def removeHandler(hdlr: Handler) -> None;
    def hasHandlers -> bool;
    def getEffectiveLevel -> int;
    def isEnabledFor(level: int) -> bool;
    def callHandlers(record: LogRecord) -> int;
    def handle(record: LogRecord) -> None;
    def _log(level: int, msg: str) -> None;
    def debug(msg: str);
    def info(msg: str);
    def warning(msg: str);
    def error(msg: str);
    def critical(msg: str);
    def fatal(msg: str);
    def exception(msg: str);
    def log(level: int, msg: str);
    def getChild(suffix: str) -> Logger;
}


obj _RootCfg {
    has disable: int,
        configured: bool;

    def init;
}

glob _ROOTCFG: _RootCfg = _RootCfg(),
     _ROOT: Logger = Logger(name="root", level=WARNING);


obj _Registry {
    has known: dict[str, Logger];

    def init;
}

glob _REG: _Registry = _Registry();


def _parent_for(name: str) -> Logger;


def:pub getLogger(name: str = "") -> Logger;


def:pub basicConfig(
    level: int = -1,
    format: str = "",
    datefmt: str = "",
    style: str = "%",
    filename: str = "",
    filemode: str = "a",
    stream: str = "",
    force: bool = False,
    encoding: str = "",
    errors: str = ""
);


def _ensure_root;


def:pub disable(level: int = 50);


def:pub debug(msg: str);


def:pub info(msg: str);


def:pub warning(msg: str);


def:pub error(msg: str);


def:pub critical(msg: str);


def:pub exception(msg: str);


def log_msg(level: int, msg: str);


def shutdown_handlers;

impl _Names.init {
    self.extra = {};
}


impl getLevelName(level: int) -> str {
    if level == CRITICAL {
        return "CRITICAL";
    }
    if level == ERROR {
        return "ERROR";
    }
    if level == WARNING {
        return "WARNING";
    }
    if level == INFO {
        return "INFO";
    }
    if level == DEBUG {
        return "DEBUG";
    }
    if level == NOTSET {
        return "NOTSET";
    }
    key: str = str(level);
    if key in _NAMES.extra {
        return _NAMES.extra[key];
    }
    return "Level " + key;
}


impl addLevelName(level: int, levelName: str) {
    _NAMES.extra[str(level)] = levelName;
}


impl getLevelNamesMapping -> dict[str, int] {
    out: dict[str, int] = {};
    out["CRITICAL"] = CRITICAL;
    out["FATAL"] = FATAL;
    out["ERROR"] = ERROR;
    out["WARN"] = WARN;
    out["WARNING"] = WARNING;
    out["INFO"] = INFO;
    out["DEBUG"] = DEBUG;
    out["NOTSET"] = NOTSET;
    return out;
}


impl _pad3(v: int) -> str {
    if v >= 100 {
        return str(v);
    }
    if v >= 10 {
        return "0" + str(v);
    }
    return "00" + str(v);
}


impl LogRecord.init(
    name: str = "root",
    level: int = 0,
    pathname: str = "",
    lineno: int = 0,
    msg: str = "",
    args: (list[any] | None) = None,
    exc_info: (list[any] | None) = None,
    func: str = "",
    sinfo: str = ""
) {
    now: float = time.time();
    self.name = name;
    self.levelno = level;
    self.levelname = getLevelName(level);
    self.msg = msg;
    self.pathname = pathname;
    self.lineno = lineno;
    self.funcName = func;
    self.created = now;
    self.msecs = (now - float(int(now))) * 1000.0;
    self.relativeCreated = (now - _START_TIME) * 1000.0;
}

impl LogRecord.getMessage -> str {
    return self.msg;
}


impl _sub(text: str, token: str, value: str) -> str {
    if token not in text {
        return text;
    }
    return value.join(text.split(token));
}


impl Formatter.init(fmt: str = "", datefmt: str = "", style: str = "%") {
    if fmt == "" {
        self._fmt = "%(message)s";
    } else {
        self._fmt = fmt;
    }
    self.datefmt = datefmt;
}

impl Formatter.formatTime(record: LogRecord, datefmt: str = "") -> str {
    spec: str = datefmt;
    if spec == "" {
        spec = self.datefmt;
    }
    if spec != "" {
        return log_strftime(spec, int(record.created));
    }
    base: str = log_strftime(_DEFAULT_TIME_FORMAT, int(record.created));
    return base + "," + _pad3(int(record.msecs));
}

impl Formatter.formatMessage(record: LogRecord) -> str {
    line: str = self._fmt;
    if "%(asctime)s" in line {
        line = _sub(line, "%(asctime)s", self.formatTime(record));
    }
    line = _sub(line, "%(levelname)s", record.levelname);
    line = _sub(line, "%(levelno)s", str(record.levelno));
    line = _sub(line, "%(levelno)d", str(record.levelno));
    line = _sub(line, "%(name)s", record.name);
    line = _sub(line, "%(message)s", record.getMessage());
    line = _sub(line, "%(pathname)s", record.pathname);
    line = _sub(line, "%(filename)s", _basename(record.pathname));
    line = _sub(line, "%(module)s", _modname(record.pathname));
    line = _sub(line, "%(lineno)s", str(record.lineno));
    line = _sub(line, "%(lineno)d", str(record.lineno));
    line = _sub(line, "%(funcName)s", record.funcName);
    line = _sub(line, "%(created)f", _f6(record.created));
    line = _sub(line, "%(msecs)d", str(int(record.msecs)));
    line = _sub(line, "%(relativeCreated)d", str(int(record.relativeCreated)));
    return line;
}

impl Formatter.format(record: LogRecord) -> str {
    return self.formatMessage(record);
}


impl _f6(v: float) -> str {
    return format(v, ".6f");
}


impl _basename(path: str) -> str {
    cut: int = path.rfind("/");
    if cut < 0 {
        return path;
    }
    return path[cut + 1:];
}


impl _modname(path: str) -> str {
    base: str = _basename(path);
    cut: int = base.rfind(".");
    if cut <= 0 {
        return base;
    }
    return base[0:cut];
}


impl Handler.init(level: int = 0, kind: int = 0, stream: int = 0) {
    self.level = level;
    self._kind = kind;
    self._stream = stream;
    self._formatter = None;
    self._closed = False;
}

impl Handler.setLevel(level: int) {
    self.level = level;
}

impl Handler.setFormatter(fmt: Formatter) {
    self._formatter = fmt;
}

impl Handler.format(record: LogRecord) -> str {
    f: Formatter | None = self._formatter;
    if f is not None {
        return f.format(record);
    }
    return _DEFAULT_FORMATTER.format(record);
}

impl Handler.emit(record: LogRecord) {
    line: str = self.format(record) + "\n";
    if self._kind == _KIND_STDOUT {
        sys.stdout.write(line);
    } elif self._kind == _KIND_FILE {
        if self._stream != 0 {
            log_fputs(self._stream, line);
            log_fflush(self._stream);
        }
    } else {
        sys.stderr.write(line);
    }
}

impl Handler.handle(record: LogRecord) -> bool {
    if record.levelno < self.level {
        return False;
    }
    self.emit(record);
    return True;
}

impl Handler.flush {
    if self._kind == _KIND_FILE and self._stream != 0 {
        log_fflush(self._stream);
    }
}

impl Handler.close {
    if self._kind == _KIND_FILE and self._stream != 0 and not self._closed {
        log_fclose(self._stream);
        self._closed = True;
    }
}


impl StreamHandler(stream: str = "stderr") -> Handler {
    kind: int = _KIND_STDERR;
    if stream == "stdout" {
        kind = _KIND_STDOUT;
    }
    return Handler(level=NOTSET, kind=kind, stream=0);
}


impl FileHandler(
    filename: str, mode: str = "a", encoding: str = "", delay: bool = False
) -> Handler {
    fp: int = log_fopen(filename, mode);
    if fp == 0 {
        raise FileNotFoundError("cannot open log file: " + filename);
    }
    return Handler(level=NOTSET, kind=_KIND_FILE, stream=fp);
}


impl Logger.init(name: str = "root", level: int = 0) {
    self.name = name;
    self.level = level;
    self.propagate = True;
    self.disabled = False;
    fresh: list[Handler] = [];
    self.handlers = fresh;
    self.parent = None;
}

impl Logger.setLevel(level: int) {
    self.level = level;
}

impl Logger.addHandler(hdlr: Handler) -> None {
    i: int = 0;
    while i < len(self.handlers) {
        if self.handlers[i] is hdlr {
            return;
        }
        i += 1;
    }
    self.handlers.append(hdlr);
}

impl Logger.removeHandler(hdlr: Handler) -> None {
    i: int = 0;
    while i < len(self.handlers) {
        if self.handlers[i] is hdlr {
            self.handlers.pop(i);
            return;
        }
        i += 1;
    }
}

impl Logger.hasHandlers -> bool {
    if len(self.handlers) > 0 {
        return True;
    }
    if not self.propagate {
        return False;
    }
    p: Logger | None = self.parent;
    if p is None {
        return False;
    }
    pp: Logger = p;
    return pp.hasHandlers();
}

impl Logger.getEffectiveLevel -> int {
    if self.level != NOTSET {
        return self.level;
    }
    p: Logger | None = self.parent;
    if p is None {
        return NOTSET;
    }
    pp: Logger = p;
    return pp.getEffectiveLevel();
}

impl Logger.isEnabledFor(level: int) -> bool {
    if self.disabled {
        return False;
    }
    if level <= _ROOTCFG.disable {
        return False;
    }
    return level >= self.getEffectiveLevel();
}

impl Logger.callHandlers(record: LogRecord) -> int {
    found: int = 0;
    for h in self.handlers {
        found += 1;
        h.handle(record);
    }
    if not self.propagate {
        return found;
    }
    p: Logger | None = self.parent;
    if p is None {
        return found;
    }
    pp: Logger = p;
    return found + pp.callHandlers(record);
}

impl Logger.handle(record: LogRecord) -> None {
    if self.disabled {
        return;
    }
    if self.callHandlers(record) == 0 {
        if record.levelno >= WARNING {
            sys.stderr.write(record.getMessage() + "\n");
        }
    }
}

impl Logger._log(level: int, msg: str) -> None {
    if not self.isEnabledFor(level) {
        return;
    }
    self.handle(LogRecord(name=self.name, level=level, msg=msg));
}

impl Logger.debug(msg: str) {
    self._log(DEBUG, msg);
}

impl Logger.info(msg: str) {
    self._log(INFO, msg);
}

impl Logger.warning(msg: str) {
    self._log(WARNING, msg);
}

impl Logger.error(msg: str) {
    self._log(ERROR, msg);
}

impl Logger.critical(msg: str) {
    self._log(CRITICAL, msg);
}

impl Logger.fatal(msg: str) {
    self._log(CRITICAL, msg);
}

impl Logger.exception(msg: str) {
    self._log(ERROR, msg);
}

impl Logger.log(level: int, msg: str) {
    self._log(level, msg);
}

impl Logger.getChild(suffix: str) -> Logger {
    if self.name == "root" {
        return getLogger(suffix);
    }
    return getLogger(self.name + "." + suffix);
}


impl _RootCfg.init {
    self.disable = 0;
    self.configured = False;
}


impl _Registry.init {
    self.known = {};
}


impl _parent_for(name: str) -> Logger {
    cut: int = name.rfind(".");
    if cut <= 0 {
        return _ROOT;
    }
    return getLogger(name[0:cut]);
}


impl getLogger(name: str = "") -> Logger {
    if name == "" or name == "root" {
        return _ROOT;
    }
    if name in _REG.known {
        return _REG.known[name];
    }
    fresh: Logger = Logger(name=name, level=NOTSET);
    _REG.known[name] = fresh;
    fresh.parent = _parent_for(name);
    return fresh;
}


impl basicConfig(
    level: int = -1,
    format: str = "",
    datefmt: str = "",
    style: str = "%",
    filename: str = "",
    filemode: str = "a",
    stream: str = "",
    force: bool = False,
    encoding: str = "",
    errors: str = ""
) {
    if force {
        for h in _ROOT.handlers {
            h.close();
        }
        cleared: list[Handler] = [];
        _ROOT.handlers = cleared;
    }
    if len(_ROOT.handlers) == 0 {
        hdlr: Handler = StreamHandler("stderr");
        if filename != "" {
            hdlr = FileHandler(filename, filemode);
        } elif stream == "stdout" {
            hdlr = StreamHandler("stdout");
        }
        spec: str = format;
        if spec == "" {
            spec = BASIC_FORMAT;
        }
        hdlr.setFormatter(Formatter(fmt=spec, datefmt=datefmt));
        _ROOT.addHandler(hdlr);
    }
    if level >= 0 {
        _ROOT.setLevel(level);
    }
    _ROOTCFG.configured = True;
}


impl _ensure_root {
    if len(_ROOT.handlers) == 0 {
        basicConfig();
    }
}


impl disable(level: int = 50) {
    _ROOTCFG.disable = level;
}


impl debug(msg: str) {
    _ensure_root();
    _ROOT.debug(msg);
}


impl info(msg: str) {
    _ensure_root();
    _ROOT.info(msg);
}


impl warning(msg: str) {
    _ensure_root();
    _ROOT.warning(msg);
}


impl error(msg: str) {
    _ensure_root();
    _ROOT.error(msg);
}


impl critical(msg: str) {
    _ensure_root();
    _ROOT.critical(msg);
}


impl exception(msg: str) {
    _ensure_root();
    _ROOT.error(msg);
}


impl log_msg(level: int, msg: str) {
    _ensure_root();
    _ROOT.log(level, msg);
}


impl shutdown_handlers {
    for h in _ROOT.handlers {
        h.flush();
        h.close();
    }
}
