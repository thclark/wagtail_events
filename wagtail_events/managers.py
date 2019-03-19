# -*- coding:utf8 -*-
"""
Wagtail events model managers
"""

from __future__ import unicode_literals

from django.db.models import Manager


class EventOccurrenceManager(Manager):
    @staticmethod
    def _get_min_time(dt):
        """
        Makes clock to 00:00:00
        :param dt: datetime
        :return: datetime
        """
        return dt.replace(hour=0, minute=0, second=0)

    def in_date_range(self, start, end):
        """
        Get event dates that appear between the start and end dates
        :return: Filtered django model queryset
        """
        start = self._get_min_time(start)
        end = self._get_min_time(end)
        return self.filter(start_date__gte=start, start_date__lte=end)
