# -*- coding:utf8 -*-

from __future__ import unicode_literals

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def querystring(context, *args, **kwargs):
    """
    Display all GET values (except page) encoded as url params

    :param context: template context
    :return: string|encoded params as urlstring
    """
    try:
        params = context['request'].GET.dict()
    except (KeyError, AttributeError):
        params = {}
    else:
        for value in args:
            params.pop(value, None)
        for key, value in kwargs.items():
            params[key] = value
    return urlencode(params)


def _patch(context, key, data):
    """
    Patch the GET value

    :param context: template context dict
    :param key: item name
    :param data: item value
    :return: patched url params
    """
    getvars = dict(context['request'].GET)
    getvars[key] = [data]
    return '?{0}'.format(urlencode(getvars, doseq=True))


@register.simple_tag(takes_context=True)
def patch_scope(context, scope):
    """
    Prepare scope for agenda

    :param context:
    :param scope:
    :return:
    """
    return _patch(context, 'scope', scope)


@register.simple_tag(takes_context=True)
def patch_start_date(context, date):
    """
    Prepare `start_date` url for agenda

    :param context: template context dict
    :param date: start_date
    :return:
    """
    return _patch(context, 'start_date', date.strftime('%Y.%m.%d'))
