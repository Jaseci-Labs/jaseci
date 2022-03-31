"""Built in actions for Jaseci"""
from datetime import datetime
from datetime import timedelta
from jaseci.jac.machine.jac_value import jac_type_unwrap as jtu
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def quantize_to_year(date: str):
    date = datetime.fromisoformat(jtu(date))
    date = date.replace(month=1, day=1, hour=0, minute=0,
                        second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def quantize_to_month(date: str):
    date = datetime.fromisoformat(jtu(date))
    date = date.replace(day=1, hour=0, minute=0,
                        second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def quantize_to_week(date: str):
    date = datetime.fromisoformat(jtu(date))
    date = date.replace(hour=0, minute=0,
                        second=0, microsecond=0)
    date = date - timedelta(days=date.weekday())
    return date.isoformat()


@jaseci_action()
def quantize_to_day(date: str):
    date = datetime.fromisoformat(jtu(date))
    date = date.replace(hour=0, minute=0,
                        second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def date_day_diff(start_date: str, end_date: str):
    # Try to deal with some incompatible date in old nodes
    # Due date has not been saving in isoformat so this doesn't work
    # for example,'2021-03-31T04:00:00.000Z'
    start_date = datetime.fromisoformat(jtu(start_date.split('T')[0]))
    end_date = datetime.fromisoformat(jtu(end_date.split('T')[0]))

    delta = end_date - start_date

    return delta.days
