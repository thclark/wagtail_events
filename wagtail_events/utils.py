# -*- coding:utf8 -*-
"""
Wagtail events utilities
"""

from __future__ import unicode_literals

import calendar
import datetime

from django.utils import timezone


_DATE_FORMAT_RE = '^([0-9]){4}\.([0-9]){2}\.([0-9]){2}$'


def date_to_datetime(date, time_choice='min'):
    """
    Convert date to datetime.

    :param date: date to convert
    :param time_choice: max or min
    :return: datetime
    """
    choice = getattr(datetime.datetime, 'min' if time_choice == 'min' else 'max').time()
    return timezone.make_aware(
        datetime.datetime.combine(date, choice),
        timezone.get_current_timezone(),
    )


def add_months(date, months):
    """
    Add months to the date.

    :param date:
    :param months:
    :return:
    """
    month = date.month - 1 + months
    year = int(date.year + month / 12)
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def remove_months(date, months):
    """
    Add months to the date.

    :param date:
    :param months:
    :return:
    """
    month = date.month - 1 - months
    year = int(date.year + month / 12)
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
