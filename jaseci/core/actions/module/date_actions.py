from datetime import datetime
from datetime import timedelta


def year_from_date(param_list):
    date = datetime.fromisoformat(param_list[0])
    date = date.replace(month=1, day=1, hour=0, minute=0,
                        second=0, microsecond=0)
    return date.isoformat()


def month_from_date(param_list):
    date = datetime.fromisoformat(param_list[0])
    date = date.replace(day=1, hour=0, minute=0,
                        second=0, microsecond=0)
    return date.isoformat()


def week_from_date(param_list):
    date = datetime.fromisoformat(param_list[0])
    date = date.replace(hour=0, minute=0,
                        second=0, microsecond=0)
    date = date - timedelta(days=date.weekday())
    return date.isoformat()


def day_from_date(param_list):
    date = datetime.fromisoformat(param_list[0])
    date = date.replace(hour=0, minute=0,
                        second=0, microsecond=0)
    return date.isoformat()


def date_day_diff(param_list):
    date_1 = datetime.fromisoformat(param_list[0])
    date_2 = datetime.fromisoformat(param_list[1])

    delta = date_1 - date_2

    return delta.days
