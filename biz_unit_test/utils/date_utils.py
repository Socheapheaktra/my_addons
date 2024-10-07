import pytz
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo.addons.biz_unit_test.utils.decorator import blueprint as blp
from odoo.addons.biz_unit_test.schemas.helper_schema import *
from odoo.addons.biz_unit_test.utils.consts import Formats


@blp.argument(DateRangeSchema())
def date_range(start, end, interval=relativedelta(days=1)):
    """
    Return Date Generator from the given start and end.

    :param date start: Date Start
    :param date end: Date End
    :param relativedelta interval: Date Increment Per Interval, default to 1 day
    :return: Range of Dates
    """
    if start > end:
        raise ValueError("Start Date must not be greater than End Date.")

    # Prevent infinite loop in case someone use negative relativedelta
    init_start = start

    while end >= start >= init_start:
        yield start
        start += interval


@blp.argument(DateTimeSchema())
def datetime_to_pp(dt):
    """
    Convert a naive datetime to Phnom Penh Timezone

    :param datetime dt: Naive Datetime
    :return: DateTime in Phnom Penh Timezone
    :rtype: datetime
    """
    tz = pytz.timezone("Asia/Phnom_Penh")
    return pytz.utc.localize(dt).astimezone(tz).replace(tzinfo=None)


@blp.argument(DateTimeSchema())
def datetime_to_utc(dt):
    """
    Convert a naive datetime to UTC Timezone

    :param datetime dt: Naive Datetime
    :return: DateTime in UTC Timezone
    :rtype: datetime
    """
    tz = pytz.timezone("Asia/Phnom_Penh")
    return tz.localize(dt).astimezone(pytz.utc).replace(tzinfo=None)


def datetime_to_string(dt):
    return datetime.strftime(dt, Formats.DATETIME)


def datetime_from_string(dt_str):
    return datetime.strptime(dt_str, Formats.DATETIME)


def date_to_string(d):
    return datetime.strftime(d, Formats.DATE)


def date_from_string(d_str):
    return datetime.strptime(d_str, Formats.DATE)
