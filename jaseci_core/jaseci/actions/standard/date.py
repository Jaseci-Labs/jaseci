"""Built in actions for Jaseci"""
from datetime import datetime
from datetime import timedelta
from jaseci.jac.machine.jac_value import jac_type_unwrap as jtu
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def quantize_to_year(date: str):
    date = datetime.fromisoformat(jtu(date))
    date = date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def quantize_to_month(date: str):
    date = datetime.fromisoformat(jtu(date))
    date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def quantize_to_week(date: str):
    date = datetime.fromisoformat(jtu(date))
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    date = date - timedelta(days=date.weekday())
    return date.isoformat()


@jaseci_action()
def quantize_to_day(date: str):
    date = datetime.fromisoformat(jtu(date))
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return date.isoformat()


@jaseci_action()
def date_day_diff(start_date: str, end_date: str):
    # Try to deal with some incompatible date in old nodes
    # Due date has not been saving in isoformat so this doesn't work
    # for example,'2021-03-31T04:00:00.000Z'
    start_date = datetime.fromisoformat(jtu(start_date.split("T")[0]))
    end_date = datetime.fromisoformat(jtu(end_date.split("T")[0]))

    delta = end_date - start_date

    return delta.days


@jaseci_action()
def phrase_to_date(phrase: str):
    today = date.today()
    if phrase == "yesterday" or phrase == "Yesterday":
        yesterday = today - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    elif phrase == "today" or phrase == "Today":
        return today.strftime("%Y-%m-%d")

    elif phrase.find("month") != -1 or phrase.find("Month") != -1:
        rdate = today - relativedelta(months=1)
        return rdate.strftime("%Y-%m-%d")

    elif phrase.find("sunday") != -1 or phrase.find("Sunday") != -1:
        firstoffset = 6 - today.weekday()
        if firstoffset < 0:
            rdate = today + timedelta(days=firstoffset)
            return rdate.strftime("%Y-%m-%d")
        else:
            thisdate = today + timedelta(days=firstoffset)
            rdate = thisdate - timedelta(days=7)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("Saturday") != -1 or phrase.find("saturday") != -1:
        firstoffset = 5 - today.weekday()
        if firstoffset < 0:
            rdate = today + timedelta(days=firstoffset)
            return rdate.strftime("%Y-%m-%d")
        else:
            thisdate = today + timedelta(days=firstoffset)
            rdate = thisdate - timedelta(days=7)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("friday") != -1 or phrase.find("Friday") != -1:
        firstoffset = 4 - today.weekday()
        if firstoffset < 0:
            rdate = today + timedelta(days=firstoffset)
            return rdate.strftime("%Y-%m-%d")
        else:
            thisdate = today + timedelta(days=firstoffset)
            rdate = thisdate - timedelta(days=7)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("thursday") != -1 or phrase.find("Thursday") != -1:
        firstoffset = 3 - today.weekday()
        if firstoffset < 0:
            rdate = today + timedelta(days=firstoffset)
            return rdate.strftime("%Y-%m-%d")
        else:
            thisdate = today + timedelta(days=firstoffset)
            rdate = thisdate - timedelta(days=7)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("wednesday") != -1 or phrase.find("Wednesday") != -1:
        firstoffset = 2 - today.weekday()
        if firstoffset < 0:
            rdate = today + timedelta(days=firstoffset)
            return rdate.strftime("%Y-%m-%d")
        else:
            thisdate = today + timedelta(days=firstoffset)
            rdate = thisdate - timedelta(days=7)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("tuesday") != -1 or phrase.find("Tuesday") != -1:
        firstoffset = 1 - today.weekday()
        if firstoffset < 0:
            rdate = today + timedelta(days=firstoffset)
            return rdate.strftime("%Y-%m-%d")
        else:
            thisdate = today + timedelta(days=firstoffset)
            rdate = thisdate - timedelta(days=7)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("monday") != -1 or phrase.find("Monday") != -1:
        firstoffset = 0 - today.weekday()
        if firstoffset < 0:
            rdate = today + timedelta(days=firstoffset)
            return rdate.strftime("%Y-%m-%d")
        else:
            thisdate = today + timedelta(days=firstoffset)
            rdate = thisdate - timedelta(days=7)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("january") != -1 or phrase.find("January") != -1:
        firstoffset = 1 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("february") != -1 or phrase.find("February") != -1:
        firstoffset = 2 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("march") != -1 or phrase.find("March") != -1:
        firstoffset = 3 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("april") != -1 or phrase.find("April") != -1:
        firstoffset = 4 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("may") != -1 or phrase.find("May") != -1:
        firstoffset = 5 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("june") != -1 or phrase.find("June") != -1:
        firstoffset = 6 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("july") != -1 or phrase.find("July") != -1:
        firstoffset = 7 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("august") != -1 or phrase.find("August") != -1:
        firstoffset = 8 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("september") != -1 or phrase.find("September") != -1:
        firstoffset = 9 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("october") != -1 or phrase.find("October") != -1:
        firstoffset = 10 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("november") != -1 or phrase.find("November") != -1:
        firstoffset = 11 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    elif phrase.find("december") != -1 or phrase.find("December") != -1:
        firstoffset = 12 - today.month
        if firstoffset < 0:
            rdate = today + relativedelta(months=firstoffset)
            return rdate.strftime("%Y-%m-%d")

        else:
            thisyear = today + relativedelta(months=firstoffset)
            rdate = thisyear - relativedelta(years=1)
            return rdate.strftime("%Y-%m-%d")

    else:
        return None
