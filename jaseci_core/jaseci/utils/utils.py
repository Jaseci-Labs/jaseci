import io
import os
import pstats
import cProfile
import pdb
import importlib
import pkgutil
import logging
import types
import base64
import re
import json
import sys
import functools
import traceback
import inspect
import unittest
from time import time

from pprint import pformat

from jaseci.utils.log_utils import LimitedSlidingBuffer


class ColCodes:
    TY = "\033[33m"
    TG = "\033[32m"
    TR = "\033[31m"
    EC = "\033[m"


def master_from_meta(meta):
    """Return master from meta in actions"""
    return meta["h"].get_obj(meta["m_id"], meta["m_id"])


# Get an instance of a logger
def connect_logger_handler(target_logger, handler, level=logging.WARN):
    """Attaches standard formatting and adds handler to logger"""
    target_logger.setLevel(level)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s: %(message)s")
    )
    target_logger.addHandler(handler)


logger = logging.getLogger("core")
logger.propagate = False
logs = LimitedSlidingBuffer()
if len(logger.handlers) < 1:
    connect_logger_handler(logger, logging.StreamHandler(), logging.INFO)
    connect_logger_handler(logger, logging.StreamHandler(stream=logs), logging.INFO)

app_logger = logging.getLogger("app")
app_logger.propagate = False
if len(app_logger.handlers) < 1:
    connect_logger_handler(app_logger, logging.StreamHandler(), logging.INFO)
    connect_logger_handler(app_logger, logging.StreamHandler(stream=logs), logging.INFO)


def log_var_out(val):
    """Print to log"""
    if not logging.getLogger("core").disabled:
        logger.info(pformat(val))


camel_to_snake_re = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(name):
    return camel_to_snake_re.sub("_", name).lower()


def bp():
    pdb.set_trace()
    breakpoint()


def dummy_bp(inspect):
    traceback.print_stack()
    print(inspect)
    input()


def print_stack_to_log():
    tb = traceback.extract_stack()
    log_var_out(tb)


def exc_stack_as_str_list():
    return traceback.format_exception(*sys.exc_info())


uuid_re = re.compile(
    "([a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89aAbB][a-f0-9]{3}-?[a-f0-9]{12})"
)


def is_urn(s: str):
    """Test if is uuid string in urn format"""
    return type(s) == str and s.startswith("urn:uuid:")


def is_jsonable(x):
    """Test if object can be json serialized"""
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def json_out(val):
    if type(val) == str:
        return val
    try:
        return json.dumps(val)
    except Exception:
        return val


def parse_str_token(s):
    return str(bytes(s, "utf-8").decode("unicode_escape")[1:-1])


def get_all_subclasses(cls):
    """Return list of all subclasses of cls"""
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_all_subclasses(c)]
    )


def matching_fields(obj1, obj2):
    """
    Return list of matching member attributes in objects
    (non-private fields only)
    """
    matches = []
    for a in dir(obj1):
        if not a.startswith("_"):
            for b in dir(obj2):
                if a == b:
                    matches.append(a)
    return matches


obj_class_cache = {}


def build_class_dict(from_where):
    global obj_class_cache
    prefix = from_where.__name__ + "."
    for importer, modname, ispkg in pkgutil.iter_modules(from_where.__path__, prefix):
        if not ispkg:
            clsmembers = inspect.getmembers(
                importlib.import_module(modname), inspect.isclass
            )
            for cls, obj in clsmembers:
                obj_class_cache[camel_to_snake(cls)] = getattr(
                    importlib.import_module(modname), cls
                )
        else:
            if hasattr(from_where, modname.split(".")[-1]):
                build_class_dict(getattr(from_where, modname.split(".")[-1]))


def find_class_and_import(class_name, from_where):
    """
    Search for class through all core packages

    Classes assumed to have same name as module file
    """
    global obj_class_cache
    if not obj_class_cache.keys():
        build_class_dict(from_where)
    return obj_class_cache[class_name]


def copy_func(f, name=None):
    """
    Utility to duplicate function in python.
    Can be used to programatically add methods to classes
    """
    g = types.FunctionType(
        f.__code__,
        f.__globals__,
        name=f.__name__,
        argdefs=f.__defaults__,
        closure=f.__closure__,
    )
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    g.__name__ = name if name else g.__name__
    return g


def b64decode_str(code):
    """Decode a base 64 encoded string"""
    try:
        code = base64.b64decode(code).decode()
    except UnicodeDecodeError:
        logger.error("Code encoding invalid!")
    return code


def perf_test_start():
    perf_prof = cProfile.Profile()
    perf_prof.enable()
    return perf_prof


def perf_test_stop(perf_prof, save_to_file=False):
    perf_prof.disable()
    if save_to_file:
        perf_prof.dump_stats(f"{id(perf_prof)}.prof")
    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(perf_prof, stream=s).sort_stats(sortby)
    ps.print_stats()
    s = s.getvalue()
    s = "ncalls" + s.split("ncalls")[-1]
    s = "\n".join([",".join(line.rstrip().split(None, 5)) for line in s.split("\n")])
    return s


def perf_test_to_b64(perf_prof, do_delete=True):
    s = ""
    fn = f"{id(perf_prof)}.prof"
    if os.path.exists(fn):
        with open(fn, "rb") as image_file:
            s = base64.b64encode(image_file.read()).decode()
        if do_delete:
            os.remove(fn)
    return s


class TestCaseHelper:
    """Helper to pretty print test results"""

    def setUp(self):
        self.logger_off()
        self.stime = time()
        return super().setUp()

    def tearDown(self):
        td = super().tearDown()
        result = (
            f"Time: {ColCodes.TY}{time()-self.stime:.3f} "
            + f'- {ColCodes.EC}{self.id().split(".")[-1]}: '
        )
        get_outcome = self.defaultTestResult()
        self._feedErrorsToResult(get_outcome, self._outcome.errors)
        if len(get_outcome.errors) or len(get_outcome.failures):
            result += f"{ColCodes.TR}[failed]{ColCodes.EC}"
        elif len(self._outcome.skipped):
            result += f"{ColCodes.TY}[skipped]{ColCodes.EC}"
        else:
            result += f"{ColCodes.TG}[passed]{ColCodes.EC}"

        print(result)
        self.logger_on()
        return td

    def logger_off(self):
        """Turn off logging output"""
        logging.getLogger("core").disabled = True
        logging.getLogger("app").disabled = True

    def logger_on(self):
        """Turn on logging output"""
        logging.getLogger("core").disabled = False
        logging.getLogger("app").disabled = False

    def is_logger_off(self):
        return logging.getLogger("core").disabled and logging.getLogger("app").disabled

    def log(self, *val):
        """Print to log"""
        is_off = self.is_logger_off()
        self.logger_on()
        for i in val:
            log_var_out(i)
        if is_off:
            self.logger_off()

    def stopper(self):
        """Force test to fail"""
        self.assertTrue(False)

    def perf_test_start(self):
        self.pr = perf_test_start()

    def perf_test_stop(self):
        print(perf_test_stop(self.pr))

    def skip_test(self, msg="No reason provided"):
        raise unittest.SkipTest("Skipping: " + msg)


def is_true(val):
    return (
        val.lower() == "true"
        if type(val) is str
        else val is True  # is_async might be non bool
    )
