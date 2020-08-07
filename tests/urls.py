# -*- coding:utf8 -*-

from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from wagtail.core import urls as wagtail_urls


urlpatterns = [
    url(r"", include(wagtail_urls)),
]
