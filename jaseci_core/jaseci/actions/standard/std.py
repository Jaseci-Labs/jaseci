"""Built in actions for Jaseci"""
from operator import itemgetter
from jaseci.utils.utils import logger, app_logger, json_out
from datetime import datetime
from jaseci.jac.machine.jac_value import jac_wrap_value as jwv
from jaseci.actions.live_actions import jaseci_action
import sys
import uuid
import json


@jaseci_action()
def log(param_list, meta):
    """Standard built in for printing output to log"""
    result = ''
    for i in param_list:
        result += json_out(jwv(i))
    app_logger.info(result)
    return result


@jaseci_action()
def out(param_list, meta):
    """Standard built in for printing output"""
    param_list = [json_out(jwv(x)) for x in param_list]
    print(*param_list)


@jaseci_action()
def err(param_list, meta):
    """Standard built in for printing to stderr"""
    param_list = [json_out(jwv(x)) for x in param_list]
    print(*param_list, file=sys.stderr)


@jaseci_action()
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


@jaseci_action()
def time_now(param_list, meta):
    """Get utc date time for now in iso format"""
    return datetime.utcnow().isoformat()


@jaseci_action()
def set_global(param_list, meta):
    """
    Set global variable visible to all walkers/users
    Param 1 - name
    Param 2 - value

    Return - Sorted list
    """
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    if(not mast.is_master(super_check=True, silent=False)):
        return False
    mast.global_set(param_list[0], json.dumps(param_list[1]))
    return json.loads(mast.global_get(param_list[0])['value'])


@jaseci_action()
def get_global(param_list, meta):
    """
    Set global variable visible to all walkers/users
    Param 1 - name
    Param 2 - value

    Return - Sorted list
    """
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    val = mast.global_get(param_list[0])['value']
    if(val):
        return json.loads(val)
    else:
        return None


@jaseci_action()
def destroy_global(param_list, meta):
    """Get utc date time for now in iso format"""
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    if(not mast.is_master(super_check=True, silent=False)):
        return False
    return mast.global_delete(param_list[0])


@jaseci_action()
def set_perms(param_list, meta):
    """
    Sets object access mode for any Jaseci object
    Param 1 - target element
    Param 2 - valid permission (public, private, read_only)

    Return - true/false whether successful
    """
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    return mast.object_perms_set(obj=param_list[0],
                                 mode=param_list[1])['success']


@jaseci_action()
def get_perms(param_list, meta):
    """
    Returns object access mode for any Jaseci object
    Param 1 - target element

    Return - Sorted list
    """
    return param_list[0].j_access


@jaseci_action()
def grant_perms(param_list, meta):
    """
    Grants another user permissions to access a Jaseci object
    Param 1 - target element
    Param 2 - master to be granted permission
    Param 3 - Boolean read_only flag

    Return - Sorted list
    """
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    return mast.object_perms_grant(obj=param_list[0],
                                   mast=param_list[1],
                                   read_only=param_list[3])['success']


@jaseci_action()
def revoke_perms(param_list, meta):
    """
    Remove permissions for user to access a Jaseci object
    Param 1 - target element
    Param 2 - master to be revoked permission

    Return - Sorted list
    """
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    return mast.object_perms_revoke(obj=param_list[0],
                                    mast=param_list[1])['success']
