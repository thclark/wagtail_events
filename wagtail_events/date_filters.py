from datetime import datetime, timedelta
from isoweek import Week

from wagtail_events import utils


def get_year_agenda(model, queryset, start_date):
    """
    Get list of events that will occur in the given year.

    :param queryset: EventInstance queryset
    :param start_date: period start_date
    :type start_date: datetime.datetime()
    :return: data dictionary
    """

    start_date = datetime(start_date.year, 1, 1)
    end_date = utils.add_months(start_date, 12)

    return {
        'start_date': start_date,
        'end_date': end_date,
        'scope': 'Year',
        'items': model.objects.in_date_range(
            start_date,
            utils.date_to_datetime(end_date, 'max')
        ).filter(event_series__in=queryset),
        'next_date': utils.date_to_datetime(
            utils.add_months(start_date.date(), 12)
        ),
        'previous_date': utils.date_to_datetime(
            utils.remove_months(start_date.date(), 12)
        ),
    }


def get_month_agenda(model, queryset, start_date):
    """
    Get list of events that will occur in the given week.

    :param queryset: EventInstance queryset
    :param start_date: period start_date
    :type start_date: datetime.datetime()
    :return: data dictionary
    """
    start_date = datetime(start_date.year, start_date.month, 1)
    end_date = utils.date_to_datetime(
        utils.add_months(start_date.date(), 1),
        'max'
    )
    return {
        'start_date': start_date,
        'end_date': end_date,
        'scope': 'Month',
        'items': model.objects.in_date_range(start_date, end_date).filter(
            event_series__in=queryset
        ),
        'next_date': utils.date_to_datetime(
            utils.add_months(start_date.date(), 1)
        ),
        'previous_date': utils.date_to_datetime(
            utils.remove_months(start_date.date(), 1)
        ),
    }


def get_week_agenda(model, queryset, start_date):
    """
    Get list of events that will occur in the given week.

    :param queryset: EventInstance queryset
    :param start_date: period start_date
    :type start_date: datetime.datetime()
    :return: data dictionary
    """
    period = Week(start_date.year, start_date.date().isocalendar()[1])
    end_date = utils.date_to_datetime(period.sunday(), 'max')
    start_date = utils.date_to_datetime(period.monday())
    return {
        'start_date': start_date,
        'end_date': end_date,
        'scope': 'Week',
        'items': model.objects.in_date_range(start_date, end_date).filter(
            event_series__in=queryset
        ),
        'next_date': start_date + timedelta(days=7),
        'previous_date': start_date + timedelta(days=-7),
    }


def get_day_agenda(model, queryset, start_date):
    """
    Get list of events that will occur in the given date

    :param queryset: EventInstance queryset
    :param start_date: period start_date
    :type start_date: datetime.datetime()
    :return: data dictionary
    """
    next_date = start_date + timedelta(days=1)
    return {
        'start_date': start_date,
        'end_date': utils.date_to_datetime(start_date.date(), 'max'),
        'scope': 'Day',
        'items': model.objects.in_date_range(start_date, next_date).filter(
            event_series__in=queryset
        ),
        'next_date': next_date,
        'previous_date': start_date + timedelta(days=-1),
    }
