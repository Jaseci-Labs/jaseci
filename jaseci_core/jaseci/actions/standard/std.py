"""Built in actions for Jaseci"""
from operator import itemgetter
from jaseci.utils.utils import app_logger, json_out
from datetime import datetime
from jaseci.jac.machine.jac_value import jac_wrap_value as jwv
from jaseci.actions.live_actions import jaseci_action
from jaseci.element.element import element
import sys
import uuid
import json


@jaseci_action()
def log(*args):
    """Standard built in for printing output to log"""
    result = ''
    for i in args:
        result += json_out(jwv(i))
    app_logger.info(result)
    return result


@jaseci_action()
def out(*args):
    """Standard built in for printing output"""
    args = [json_out(jwv(x)) for x in args]
    print(*args)


@jaseci_action(aliases=['input'])
def js_input(prompt: str = ''):
    """Standard built in for printing output"""
    return input(prompt)


@jaseci_action()
def err(*args):
    """Standard built in for printing to stderr"""
    args = [json_out(jwv(x)) for x in args]
    print(*args, file=sys.stderr)


@jaseci_action()
def sort_by_col(lst: list, col_num: int, reverse: bool = False):
    """
    Sorts in place list of lists by column
    Param 1 - list
    Param 2 - col number
    Param 3 - boolean as to whether things should be reversed

    Return - Sorted list
    """
    return sorted(lst, key=itemgetter(col_num), reverse=reverse)


@jaseci_action()
def time_now(meta):
    """Get utc date time for now in iso format"""
    return datetime.utcnow().isoformat()


@jaseci_action()
def set_global(name: str, value, meta):
    """
    Set global variable visible to all walkers/users
    Param 1 - name
    Param 2 - value (must be json serializable)
    """
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    if(not mast.is_master(super_check=True, silent=False)):
        return False
    mast.global_set(name, json.dumps(value))
    return json.loads(mast.global_get(name)['value'])


@jaseci_action()
def get_global(name: str, meta):
    """
    Set global variable visible to all walkers/users
    Param 1 - name
    """
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    val = mast.global_get(name)['value']
    if(val):
        return json.loads(val)
    else:
        return None


@jaseci_action()
def destroy_global(name: str, meta):
    """Get utc date time for now in iso format"""
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    if(not mast.is_master(super_check=True, silent=False)):
        return False
    return mast.global_delete(name)


@jaseci_action()
def set_perms(obj: element, mode: str, meta):
    """
    Sets object access mode for any Jaseci object
    Param 1 - target element
    Param 2 - valid permission (public, private, read_only)

    Return - true/false whether successful
    """
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    return mast.object_perms_set(obj=obj,
                                 mode=mode)['success']


@jaseci_action()
def get_perms(obj: element):
    """
    Returns object access mode for any Jaseci object
    Param 1 - target element

    Return - Sorted list
    """
    return obj.j_access


@jaseci_action()
def grant_perms(obj: element, mast: element, read_only: bool, meta):
    """
    Grants another user permissions to access a Jaseci object
    Param 1 - target element
    Param 2 - master to be granted permission
    Param 3 - Boolean read_only flag

    Return - Sorted list
    """
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    return mast.object_perms_grant(obj=obj,
                                   mast=mast,
                                   read_only=read_only)['success']


@jaseci_action()
def revoke_perms(obj: element, mast: element, meta):
    """
    Remove permissions for user to access a Jaseci object
    Param 1 - target element
    Param 2 - master to be revoked permission

    Return - Sorted list
    """
    mast = meta['h'].get_obj(meta['m_id'], uuid.UUID(meta['m_id']))
    return mast.object_perms_revoke(obj=obj,
                                    mast=mast)['success']


@jaseci_action()
def get_report(meta):
    """
    Get current report so far for walker run
    """
    return meta['interp'].report
