from datetime import datetime
from isoweek import Week
from wagtail_events import utils


def get_year_range(start_date):
    """
    Get the start and end datetimes for the year

    :param start_date: period start_date
    :type start_date: datetime.datetime()
    :return: tuple start_datetime, end_datetime
    """
    start_date = datetime(start_date.year, 1, 1)
    end_date = utils.date_to_datetime(utils.add_months(start_date, 12), 'max')
    return start_date, end_date


def get_month_range(start_date):
    """
    Get the start and end datetimes for the month

    :param start_date: period start_date
    :type start_date: datetime.datetime()
    :return: tuple start_datetime, end_datetime
    """
    start_date = datetime(start_date.year, start_date.month, 1)
    end_date = utils.date_to_datetime(
        utils.add_months(start_date.date(), 1),
        'max'
    )
    return start_date, end_date


def get_week_range(start_date):
    """
    Get the start and end datetimes for the week

    :param start_date: period start_date
    :type start_date: datetime.datetime()
    :return: tuple start_datetime, end_datetime
    """
    period = Week(start_date.year, start_date.date().isocalendar()[1])
    start_date = utils.date_to_datetime(period.monday())
    end_date = utils.date_to_datetime(period.sunday(), 'max')
    return start_date, end_date


def get_day_range(start_date):
    """
    Get the start and end datetimes for the day

    :param start_date: period start_date
    :type start_date: datetime.datetime()
    :return: tuple start_datetime, end_datetime
    """
    start_date = utils.date_to_datetime(start_date.date(), 'min')
    end_date = utils.date_to_datetime(start_date.date(), 'max')
    print('start_date', start_date)
    print('end_date', end_date)
    return start_date, end_date
