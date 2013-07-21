# coding: utf-8
from __future__ import absolute_import, unicode_literals
from django.db import models
from .base import library
from .templatecolumn import TemplateColumn, GTemplateColumn


@library.register
class DateTimeColumn(TemplateColumn):
    """
    A column that renders datetimes in the local timezone.

    :param format: format string for datetime (optional)
    :type  format: `unicode`
    :param  short: if *format* is not specifid, use Django's
                   ``SHORT_DATETIME_FORMAT``, else ``DATETIME_FORMAT``
    :type   short: `bool`
    """
    def __init__(self, format=None, short=True, *args, **kwargs):  # pylint: disable=W0622
        if format is None:
            format = 'SHORT_DATETIME_FORMAT' if short else 'DATETIME_FORMAT'
        template = '{{ value|date:"%s"|default:default }}' % format
        super(DateTimeColumn, self).__init__(template_code=template, *args, **kwargs)

    @classmethod
    def from_field(cls, field):
        if isinstance(field, models.DateTimeField):
            return cls(verbose_name=field.verbose_name)

class GDateTimeColumn(GTemplateColumn, DateTimeColumn):
    def __init__(self, format=None, short=True, *args, **kwargs):
        if format is None:
            format = 'SHORT_DATETIME_FORMAT' if short else 'DATETIME_FORMAT'
        template = ('{% python from django_tables2.utils import date_format %}'+
                    '${date_format(value, "%s") if value else default}' % format)
        GTemplateColumn.__init__(self, template_code=template, *args, **kwargs)