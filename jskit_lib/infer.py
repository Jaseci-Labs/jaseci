from jaseci.utils.utils import logger
import jaseci.actions.standard.date as jsdate
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def year_from_date(param_list, meta):
    logger.warning('Deprecated! Use date.quantlize_...')
    return jsdate.quantize_to_year(param_list, meta)


@jaseci_action()
def month_from_date(param_list, meta):
    logger.warning('Deprecated! Use date.quantlize_...')
    return jsdate.quantize_to_month(param_list, meta)


@jaseci_action()
def week_from_date(param_list, meta):
    logger.warning('Deprecated! Use date.quantlize_...')
    return jsdate.quantize_to_week(param_list, meta)


@jaseci_action()
def day_from_date(param_list, meta):
    logger.warning('Deprecated! Use date.quantlize_...')
    return jsdate.quantize_to_day(param_list, meta)
