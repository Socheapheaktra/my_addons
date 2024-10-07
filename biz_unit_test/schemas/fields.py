from marshmallow import fields
from datetime import date, datetime

from odoo.addons.biz_unit_test.utils.consts import Formats


class Date(fields.Field):
    metadata = {
        "format": Formats.DATE,
    }

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, date):
            return value
        else:
            return super(Date, self)._deserialize(value, attr, data, **kwargs)


class DateTime(fields.DateTime):
    metadata = {
        "format": Formats.DATETIME,
    }

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime):
            return value
        else:
            return super(DateTime, self)._deserialize(value, attr, data, **kwargs)
