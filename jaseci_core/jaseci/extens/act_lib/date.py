"""Built in actions for Jaseci"""
from datetime import datetime, timedelta
from jaseci.jsorc.live_actions import jaseci_action
from dateutil.relativedelta import relativedelta


@jaseci_action()
def quantize_to_year(date: str):
    date = datetime.fromisoformat(date)
    date = date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def quantize_to_month(date: str):
    date = datetime.fromisoformat(date)
    date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def quantize_to_week(date: str):
    date = datetime.fromisoformat(date)
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    date = date - timedelta(days=date.weekday())
    return date.isoformat()


@jaseci_action()
def quantize_to_day(date: str):
    date = datetime.fromisoformat(date)
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def datetime_now():
    """Get utc date time now in iso format"""
    return datetime.utcnow().isoformat()


@jaseci_action()
def date_now():
    """Get utc date now in iso format"""
    return datetime.utcnow().date().isoformat()


@jaseci_action()
def timestamp_now():
    """Get utc date time for now in iso format"""
    return int(datetime.utcnow().timestamp())


@jaseci_action()
def datetime_obj(date: str = None):
    """Get utc date time now or parse one to dict format"""
    if date:
        date = datetime.fromisoformat(date)
    else:
        date = datetime.utcnow()

    return {
        "year": date.year,
        "month": date.month,
        "weekday": date.isoweekday(),
        "day": date.day,
        "hour": date.hour,
        "minute": date.minute,
        "second": date.second,
        "microsecond": date.microsecond,
        "iso": date.isoformat(),
    }


@jaseci_action()
def datetime_add(date: str = None, **kwargs):
    """
    Get utc date time now or parse one then add timedelta
    kwargs: this should be valid timedelta arguments
    """
    if date:
        date = datetime.fromisoformat(date)
    else:
        date = datetime.utcnow()

    return (date + relativedelta(**kwargs)).isoformat()


@jaseci_action()
def datetime_sub(date: str = None, **kwargs):
    """
    Get utc date time now or parse one then subtract timedelta
    kwargs: this should be valid timedelta arguments
    """
    if date:
        date = datetime.fromisoformat(date)
    else:
        date = datetime.utcnow()

    return (date - relativedelta(**kwargs)).isoformat()


@jaseci_action()
def date_day_diff(start_date: str, end_date: str = None):
    # Try to deal with some incompatible date in old nodes
    # Due date has not been saving in isoformat so this doesn't work
    # for example,'2021-03-31T04:00:00.000Z'
    start_date = datetime.fromisoformat(start_date.split("T")[0])

    if end_date is None:
        end_date = datetime.utcnow()
    else:
        end_date = datetime.fromisoformat(end_date.split("T")[0])

    delta = end_date - start_date

    return delta.days
