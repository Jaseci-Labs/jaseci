import io
import os
import pstats
import cProfile
import pdb
import importlib
import pkgutil
import logging
import logging.handlers as handlers
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
from pathlib import Path
from pprint import pformat
from typing import Union
from jaseci.utils.log_utils import LimitedSlidingBuffer
from jaseci.utils.gprof2dot import (
    PstatsParser,
    DotWriter,
    Profile,
    TEMPERATURE_COLORMAP,
)

LOGS_DIR = ".jaseci_logs/"


class ColCodes:
    TY = "\033[33m"
    TG = "\033[32m"
    TR = "\033[31m"
    EC = "\033[m"


def master_from_meta(meta):
    """Return master from meta in actions"""
    return meta["h"].get_obj(meta["m_id"], meta["m_id"])


def connect_logger_handler(target_logger, handler, level=logging.WARN):
    """Attaches standard formatting and adds handler to logger"""
    target_logger.setLevel(level)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s: %(message)s")
    )
    target_logger.addHandler(handler)


# Get an instance of a logger
logger = logging.getLogger("core")
logger.propagate = False
logs = LimitedSlidingBuffer()
# Create the logs folder
os.makedirs(LOGS_DIR, exist_ok=True)
if len(logger.handlers) < 1:
    connect_logger_handler(logger, logging.StreamHandler(), logging.INFO)
    connect_logger_handler(logger, logging.StreamHandler(stream=logs), logging.INFO)
    # set up a timed rotating file handler
    core_rotating_file_handler = handlers.TimedRotatingFileHandler(
        os.path.join(LOGS_DIR, "core.log"), when="midnight", backupCount=180
    )
    connect_logger_handler(logger, core_rotating_file_handler, logging.INFO)


app_logger = logging.getLogger("app")
app_logger.propagate = False
if len(app_logger.handlers) < 1:
    connect_logger_handler(app_logger, logging.StreamHandler(), logging.INFO)
    connect_logger_handler(app_logger, logging.StreamHandler(stream=logs), logging.INFO)
    # set up a timed rotating file handler
    app_rotating_file_handler = handlers.TimedRotatingFileHandler(
        os.path.join(LOGS_DIR, "app.log"), when="midnight", backupCount=180
    )
    connect_logger_handler(app_logger, app_rotating_file_handler, logging.INFO)


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


def generate_stack_as_str_list(error=None):
    stack = traceback.format_stack()
    stack.pop()  # format_stack
    stack.pop()  # generate_stack_as_str_list
    if error:
        stack.append(error)
    return stack


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


class MyPstatsParser(PstatsParser):
    def __init__(self, stats_obj):
        self.stats = stats_obj
        self.profile = Profile()
        self.function_ids = {}


def perf_test_start():
    perf_prof = cProfile.Profile()
    perf_prof.enable()
    return perf_prof


def perf_test_stop(perf_prof):
    perf_prof.disable()
    stats = pstats.Stats(perf_prof)
    profile = MyPstatsParser(stats).parse()
    profile.prune(
        node_thres=0.01, edge_thres=0.002, paths="", color_nodes_by_selftime=False
    )
    graph_str = io.StringIO()
    dot = DotWriter(graph_str)
    dot.graph(profile, TEMPERATURE_COLORMAP)
    calls_str = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(perf_prof, stream=calls_str).sort_stats(sortby)
    ps.print_stats()
    calls_str = calls_str.getvalue()
    calls_str = "ncalls" + calls_str.split("ncalls")[-1]
    calls_str = "\n".join(
        [",".join(line.rstrip().split(None, 5)) for line in calls_str.split("\n")]
    )
    return calls_str, graph_str.getvalue()


def format_jac_profile(jac_profile, sort_by="cum_time"):
    """Format a JAC profile to a csv string"""
    entries = []
    for k in jac_profile.keys():
        c = jac_profile[k]["calls"]
        u = jac_profile[k]["u_calls"]
        t = jac_profile[k]["tot_time"]
        p = jac_profile[k]["cum_time"]
        jac_profile[k]["avg_time"] = t / c
        jac_profile[k]["per_call"] = p / c
        jac_profile[k]["name"] = k
        entries.append(jac_profile[k])
    sorted_entries = sorted(entries, key=lambda x: x[sort_by], reverse=True)
    csv = "name,calls,r_calls,avg_time,per_call,tot_time,cum_time\n"
    for e in sorted_entries:
        csv += (
            f"{e['name']},{e['calls']},{e['calls']-e['u_calls']},"
            + f"{e['avg_time']},{e['per_call']},{e['tot_time']},{e['cum_time']}\n"
        )
    return csv


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


class InvalidApiException(Exception):
    pass


def find_first_api(api_name, **api_endpoints):
    for path, api_list in api_endpoints.items():
        api = next(filter(lambda x: api_name == "_".join(x["groups"]), api_list), None)
        if api:
            return path, api
    raise InvalidApiException(f"api {api_name} is not existing!")


cache_root = Path(Path.home(), ".jaseci/models")


def model_base_path(cache_dir: Union[str, Path]) -> Path:
    cache_dir = Path(cache_dir)

    if not os.path.isabs(cache_dir):
        model_cache = cache_root / cache_dir
    else:
        model_cache = cache_dir
    return model_cache
