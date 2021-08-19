from operator import itemgetter
from jaseci.utils.utils import logger, app_logger
from datetime import datetime
import sys


def log(param_list, meta):
    """Standard built in for printing output to log"""
    result = ''
    for i in range(len(param_list)):
        if (type(param_list[i]) == bool):
            if (param_list[i]):
                param_list[i] = 'true'
            else:
                param_list[i] = 'false'
        result += str(param_list[i])
    app_logger.info(result)
    return result


def out(param_list, meta):
    """Standard built in for printing output"""
    for i in range(len(param_list)):
        if (type(param_list[i]) == bool):
            if (param_list[i]):
                param_list[i] = 'true'
            else:
                param_list[i] = 'false'
    print(*param_list)


def err(param_list, meta):
    """Standard built in for printing to stderr"""
    for i in range(len(param_list)):
        if (type(param_list[i]) == bool):
            if (param_list[i]):
                param_list[i] = 'true'
            else:
                param_list[i] = 'false'
    print(*param_list, file=sys.stderr)


def sort_by_col(param_list, meta):
    """
    Sorts in place list of lists by column
    Param 1 - list
    Param 2 - col number
    Param 3 - 'reverse' / 'asc' / 'desc' (optional)

    Return - Sorted list
    """
    if (len(param_list) < 2 or isinstance(param_list[0], list) or
            not isinstance(param_list[1], int)):
        logger.error(f'Parameter list {param_list} is not of expected types')
    lst = param_list[0]
    num = param_list[1]
    reverse = False if len(
        param_list) < 3 or param_list[2] == 'asc' else True

    return sorted(lst, key=itemgetter(num), reverse=reverse)


def time_now(param_list, meta):
    """Get utc date time for now in iso format"""
    return datetime.utcnow().isoformat()


def set_env(param_list, meta):
    """
    Set global variable visiable to all walkers/users
    Param 1 - name
    Param 2 - value

    Return - Sorted list
    """
    meta['master'].admin_api_global_set(param_list[0], param_list[1])
    return meta['master'].admin_api_global_get(param_list[0])


def get_env(param_list, meta):
    """Get utc date time for now in iso format"""
    return meta['master'].admin_api_global_get(param_list[0])


def destroy_env(param_list, meta):
    """Get utc date time for now in iso format"""

    return meta['master'].admin_api_global_delete(param_list[0])
