"""Built in actions for Jaseci"""
from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
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
def datetime_now():
    """Get utc date time for now in iso format"""
    return datetime.utcnow().isoformat()


@jaseci_action()
def date_now():
    """Get utc date time for now in iso format"""
    return datetime.utcnow().date().isoformat()


@jaseci_action()
def timestamp_now():
    """Get utc date time for now in iso format"""
    return int(datetime.utcnow().timestamp())


@jaseci_action()
def date_day_diff(start_date: str, end_date: str = None):
    # Try to deal with some incompatible date in old nodes
    # Due date has not been saving in isoformat so this doesn't work
    # for example,'2021-03-31T04:00:00.000Z'
    start_date = datetime.fromisoformat(jtu(start_date.split("T")[0]))

    if end_date is None:
        end_date = datetime.utcnow()
    else:
        end_date = datetime.fromisoformat(jtu(end_date.split("T")[0]))

    delta = end_date - start_date

    return delta.days


@jaseci_action()
def phrase_to_date(phrase: str):
    today = date.today()
    datephrasefound = {}
    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]
    weekdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    numbers = [
        "31",
        "30",
        "29",
        "28",
        "27",
        "26",
        "25",
        "24",
        "23",
        "22",
        "21",
        "20",
        "19",
        "18",
        "17",
        "16",
        "15",
        "14",
        "13",
        "12",
        "11",
        "10",
        "9",
        "8",
        "7",
        "6",
        "5",
        "4",
        "3",
        "2",
        "1",
    ]
    numberwords = [
        "thirty one",
        "thirty",
        "twenty nine",
        "twenty eight",
        "twenty seven",
        "twenty six",
        "twenty five",
        "twenty four",
        "twenty three",
        "twenty two",
        "twenty one",
        "twenty",
        "nineteen",
        "eighteen",
        "seventeen",
        "sixteen",
        "fifteen",
        "fourteen",
        "thirteen",
        "twelve",
        "eleven",
        "ten",
        " nine ",
        " eight ",
        " seven ",
        " six ",
        " five ",
        " four ",
        " three ",
        " two ",
        " one ",
    ]
    slangs = ["month", "week", "day", "yesterday", "today"]

    for month in months:
        capital = month.capitalize()
        if phrase.find(month) != -1 or phrase.find(capital) != -1:
            datephrasefound["month"] = month
            break

    for day in weekdays:
        capital = day.capitalize()
        if phrase.find(day) != -1 or phrase.find(capital) != -1:
            datephrasefound["weekDay"] = day
            break

    for (number, numberword) in zip(numbers, numberwords):
        if (
            phrase.find(number) != -1
            or phrase.find(numberword) != -1
            or phrase.find(" " + number) != -1
        ):
            datephrasefound["number"] = number
            break

    for slang in slangs:
        if (
            phrase.find(slang) != -1
            or phrase.find(" " + slang) != -1
            or phrase.find(slang + "s") != -1
        ):
            datephrasefound["slang"] = slang
            break

    if len(datephrasefound) == 1:
        if "month" in datephrasefound:
            firstoffset = (months.index(datephrasefound["month"]) + 1) - today.month
            if firstoffset < 0:
                rdate = today + relativedelta(months=firstoffset)
                return rdate.strftime("%Y-%m-%d")

            else:
                thisyear = today + relativedelta(months=firstoffset)
                rdate = thisyear - relativedelta(years=1)
                return rdate.strftime("%Y-%m-%d")

        elif "weekDay" in datephrasefound:
            firstoffset = (weekdays.index(datephrasefound["weekDay"])) - today.weekday()
            if firstoffset < 0:
                rdate = today + timedelta(days=firstoffset)
                return rdate.strftime("%Y-%m-%d")
            else:
                thisdate = today + timedelta(days=firstoffset)
                rdate = thisdate - timedelta(days=7)
                return rdate.strftime("%Y-%m-%d")

        elif "slang" in datephrasefound:
            if datephrasefound["slang"] == "week":
                rdate = today - timedelta(days=7)
                return rdate.strftime("%Y-%m-%d")
            elif datephrasefound["slang"] == "month":
                rdate = today - relativedelta(months=1)
                return rdate.strftime("%Y-%m-%d")
            elif (
                datephrasefound["slang"] == "day"
                or datephrasefound["slang"] == "yesterday"
            ):
                yesterday = today - timedelta(days=1)
                return yesterday.strftime("%Y-%m-%d")

            elif datephrasefound["slang"] == "today":
                return today.strftime("%Y-%m-%d")

    if len(datephrasefound) > 1:
        if "month" in datephrasefound and "number" in datephrasefound:
            firstoffset = (months.index(datephrasefound["month"]) + 1) - today.month
            if firstoffset < 0:
                rdate = datetime(
                    2022,
                    (months.index(datephrasefound["month"]) + 1),
                    int(datephrasefound["number"]),
                )
                return rdate.strftime("%Y-%m-%d")

            else:
                rdate = datetime(
                    2021,
                    (months.index(datephrasefound["month"]) + 1),
                    int(datephrasefound["number"]),
                )
                return rdate.strftime("%Y-%m-%d")

        elif "weekDay" in datephrasefound and "number" in datephrasefound:
            rdate = today
            firstoffset = weekdays.index(datephrasefound["weekDay"]) - rdate.weekday()

            if firstoffset < 0:
                rdate = today + timedelta(days=firstoffset)
            else:
                thisdate = today + timedelta(days=firstoffset)
                rdate = thisdate - timedelta(days=7)
            days = 7 * (int(datephrasefound["number"]) - 1)
            rdate = rdate - timedelta(days=days)

            return rdate.strftime("%Y-%m-%d")

        elif "slang" in datephrasefound and "number" in datephrasefound:
            if datephrasefound["slang"] == "week":
                rdate = today - timedelta(days=7 * int(datephrasefound["number"]))
                return rdate.strftime("%Y-%m-%d")

            elif datephrasefound["slang"] == "month":
                rdate = today - relativedelta(months=1 * int(datephrasefound["number"]))
                return rdate.strftime("%Y-%m-%d")

            elif datephrasefound["slang"] == "day":
                rdate = today - timedelta(days=int(datephrasefound["number"]))
                return rdate.strftime("%Y-%m-%d")

    else:
        return today.strftime("%Y-%m-%d")
