import io
import pstats
import cProfile
import pdb
import uuid
import importlib
import pkgutil
import logging
from logging.handlers import HTTPHandler
import types
import json
import functools
from time import time
from datetime import datetime
from pprint import pformat


# Get an instance of a logger
def connect_logger_handler(target_logger, handler):
    """Attaches standard formatting and adds handler to logger"""
    target_logger.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s: %(message)s')
    )
    target_logger.addHandler(handler)


def connect_http_logging(target_logger, host, port, url):
    for i in target_logger.handlers:
        if(i.__class__.__name__ == 'HTTPHandler'):
            target_logger.removeHandler(i)

    connect_logger_handler(
        target_logger, HTTPHandler(host=f'{host}:{port}',
                                   url=url, method='POST'))


def connect_http_logging_check(target_logger):
    for i in target_logger.handlers:
        if(i.__class__.__name__ == 'HTTPHandler'):
            return True
    return False


logger = logging.getLogger('core')
if(len(logger.handlers) < 1):
    connect_logger_handler(logger, logging.StreamHandler())

app_logger = logging.getLogger('app')
if(len(app_logger.handlers) < 1):
    connect_logger_handler(app_logger, logging.StreamHandler())


def bp():
    pdb.set_trace()
    breakpoint()


def dummy_bp(inspect):
    import traceback
    traceback.print_stack()
    print(inspect)
    input()


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


def find_class_and_import(class_name, from_where):
    """
    Search for class through all core packages

    Classes assumed to have same name as module file
    """
    prefix = from_where.__name__ + "."
    res = None
    for importer, modname, ispkg in \
            pkgutil.iter_modules(from_where.__path__, prefix):
        if(not ispkg and modname.split('.')[-1] == class_name):
            res = getattr(importlib.import_module(modname), class_name)
            break
        if(ispkg):
            res2 = find_class_and_import(
                class_name, getattr(from_where, modname.split('.')[-1])
            ) if hasattr(from_where, modname.split('.')[-1]) else None
            if(res2):
                res = res2
    return res


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
        EC = '\033[m'  # noqa
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

    def log(self, val):
        """Print to log"""
        logger.info(pformat(val))

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
