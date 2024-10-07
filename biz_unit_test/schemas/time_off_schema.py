from marshmallow import Schema, fields

from odoo.addons.biz_unit_test.schemas.fields import Date, DateTime


class TimeOffCreateSchema(Schema):
    name = fields.String(required=True, allow_none=False)
    employee_id = fields.Integer(required=True, allow_none=False)
    holiday_status_id = fields.Integer(required=True, allow_none=False)
    request_date_from = Date(required=True, allow_none=False)
    request_date_to = Date(required=True, allow_none=False)
    date_from = DateTime(required=True, allow_none=False)
    date_to = DateTime(required=True, allow_none=False)
    request_unit_half = fields.Boolean(required=False, load_default=False)
