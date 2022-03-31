import io
import pstats
import cProfile
import pdb
import uuid
import importlib
import pkgutil
import logging
import types
import base64
import json
import functools
import traceback
from time import time
from datetime import datetime
from pprint import pformat


# Get an instance of a logger
def connect_logger_handler(target_logger, handler, level=logging.WARN):
    """Attaches standard formatting and adds handler to logger"""
    target_logger.setLevel(level)
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s: %(message)s')
    )
    target_logger.addHandler(handler)


logger = logging.getLogger('core')
if(len(logger.handlers) < 1):
    connect_logger_handler(logger, logging.StreamHandler(), logging.INFO)

app_logger = logging.getLogger('app')
if(len(app_logger.handlers) < 1):
    connect_logger_handler(app_logger, logging.StreamHandler(), logging.INFO)


def log_var_out(val):
    """Print to log"""
    if(not logging.getLogger('core').disabled):
        logger.info(pformat(val))


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
    if(type(val) == str):
        return val
    try:
        return json.dumps(val)
    except Exception:
        return val


def parse_str_token(s):
    return str(bytes(s, "utf-8").
               decode("unicode_escape")[1:-1])


def get_all_subclasses(cls):
    """Return list of all subclasses of cls"""
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_all_subclasses(c)])


def matching_fields(obj1, obj2):
    """
    Return list of matching member attributes in objects
    (non-private fields only)
    """
    matches = []
    for a in dir(obj1):
        if not a.startswith('_'):
            for b in dir(obj2):
                if a == b:
                    matches.append(a)
    return matches


def map_assignment_of_matching_fields(dest, source):
    """
    Assign the values of identical feild names from source to destination.
    """
    for i in matching_fields(dest, source):
        if (type(getattr(source, i)) == uuid.UUID):
            setattr(dest, i, getattr(source, i).urn)
        elif (type(getattr(source, i)) == datetime):
            setattr(dest, i, getattr(source, i).isoformat())
        elif not callable(getattr(dest, i)):
            setattr(dest, i, getattr(source, i))


obj_class_cache = {}


def build_class_dict(from_where):
    global obj_class_cache
    prefix = from_where.__name__ + "."
    for importer, modname, ispkg in \
            pkgutil.iter_modules(from_where.__path__, prefix):
        if(not ispkg):
            cls = modname.split('.')[-1]
            if(hasattr(importlib.import_module(modname), cls)):
                obj_class_cache[cls] = getattr(
                    importlib.import_module(modname), cls)
        else:
            if hasattr(from_where, modname.split('.')[-1]):
                build_class_dict(
                    getattr(from_where, modname.split('.')[-1])
                )


def find_class_and_import(class_name, from_where):
    """
    Search for class through all core packages

    Classes assumed to have same name as module file
    """
    global obj_class_cache
    if(not obj_class_cache.keys()):
        build_class_dict(from_where)
    return obj_class_cache[class_name]


def copy_func(f, name=None):
    """
    Utility to duplicate function in python.
    Can be used to programatically add methods to classes
    """
    g = types.FunctionType(f.__code__, f.__globals__,
                           name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    g.__name__ = name if name else g.__name__
    return g


def b64decode_str(code):
    """Decode a base 64 encoded string"""
    try:
        code = base64.b64decode(code).decode()
    except UnicodeDecodeError:
        logger.error(
            f'Code encoding invalid!')
    return code


class TestCaseHelper():
    """Helper to pretty print test results"""

    def setUp(self):
        self.logger_off()
        self.stime = time()
        return super().setUp()

    def tearDown(self):
        TY = '\033[33m'
        TG = '\033[32m'
        TR = '\033[31m'
        EC = '\033[m'
        td = super().tearDown()
        result = f'Time: {TY}{time()-self.stime:.3f} ' + \
                 f'- {EC}{self.id().split(".")[-1]}: '
        get_outcome = self.defaultTestResult()
        self._feedErrorsToResult(get_outcome, self._outcome.errors)
        if (len(get_outcome.errors) or len(get_outcome.failures)):
            result += f'{TR}[failed]{EC}'
        elif (len(self._outcome.skipped)):
            result += f'{TY}[skipped]{EC}'
        else:
            result += f'{TG}[passed]{EC}'

        print(result)
        self.logger_on()
        return td

    def logger_off(self):
        """Turn off logging output"""
        logging.getLogger('core').disabled = True
        logging.getLogger('app').disabled = True

    def logger_on(self):
        """Turn on logging output"""
        logging.getLogger('core').disabled = False
        logging.getLogger('app').disabled = False

    def is_logger_off(self):
        return (logging.getLogger('core').disabled and
                logging.getLogger('app').disabled)

    def log(self, val):
        """Print to log"""
        is_off = self.is_logger_off()
        self.logger_on()
        log_var_out(val)
        if(is_off):
            self.logger_off()

    def stopper(self):
        """Force test to fail"""
        self.assertTrue(False)

    def start_perf_test(self):
        self.pr = cProfile.Profile()
        self.pr.enable()

    def stop_perf_test(self):
        self.pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.CUMULATIVE
        ps = pstats.Stats(self.pr, stream=s).sort_stats(sortby)
        ps.print_stats(100)
        print(s.getvalue())


class bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
