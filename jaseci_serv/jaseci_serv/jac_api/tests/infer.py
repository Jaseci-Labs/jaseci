import jaseci.actions.standard.date as jsdate
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def year_from_date(date: str):
    return jsdate.quantize_to_year(date)


@jaseci_action()
def month_from_date(date: str):
    return jsdate.quantize_to_month(date)


@jaseci_action()
def week_from_date(date: str):
    return jsdate.quantize_to_week(date)


@jaseci_action()
def day_from_date(date: str):
    return jsdate.quantize_to_day(date)


@jaseci_action()
def date_day_diff(start_date: str, end_date: str):
    return jsdate.date_day_diff(start_date, end_date)
