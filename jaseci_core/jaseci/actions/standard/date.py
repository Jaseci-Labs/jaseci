"""Built in actions for Jaseci"""
from datetime import datetime
from datetime import timedelta
from jaseci.utils.utils import logger
from jaseci.jac.machine.jac_value import jac_type_unwrap as jtu
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def quantize_to_year(param_list, meta):
    date = datetime.fromisoformat(jtu(param_list[0]))
    date = date.replace(month=1, day=1, hour=0, minute=0,
                        second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def quantize_to_month(param_list, meta):
    date = datetime.fromisoformat(jtu(param_list[0]))
    date = date.replace(day=1, hour=0, minute=0,
                        second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def quantize_to_week(param_list, meta):
    date = datetime.fromisoformat(jtu(param_list[0]))
    date = date.replace(hour=0, minute=0,
                        second=0, microsecond=0)
    date = date - timedelta(days=date.weekday())
    return date.isoformat()


@jaseci_action()
def quantize_to_day(param_list, meta):
    date = datetime.fromisoformat(jtu(param_list[0]))
    date = date.replace(hour=0, minute=0,
                        second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def date_day_diff(param_list, meta):
    # Try to deal with some incompatible date in old nodes
    # Due date has not been saving in isoformat so this doesn't work
    # for example,'2021-03-31T04:00:00.000Z'
    param_1 = param_list[0].split('T')[0]
    param_2 = param_list[1].split('T')[0]

    date_1 = datetime.fromisoformat(jtu(param_1))
    date_2 = datetime.fromisoformat(jtu(param_2))

    delta = date_1 - date_2

    return delta.days
