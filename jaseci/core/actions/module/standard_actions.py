from core.utils.utils import logger
from datetime import datetime


def log(param_list):
    """Standard built in for printing output to log"""
    result = ''
    for i in range(len(param_list)):
        if (type(param_list[i]) == bool):
            if (param_list[i]):
                param_list[i] = 'true'
            else:
                param_list[i] = 'false'
        result += str(param_list[i])
    logger.info(result)
    return result


def out(param_list):
    """Standard built in for printing output"""
    for i in range(len(param_list)):
        if (type(param_list[i]) == bool):
            if (param_list[i]):
                param_list[i] = 'true'
            else:
                param_list[i] = 'false'
    print(*param_list)


def time_now(param_list):
    """Get utc date time for now in iso format"""
    return datetime.utcnow().isoformat()
