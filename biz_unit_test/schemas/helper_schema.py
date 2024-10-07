from marshmallow import Schema, fields, ValidationError, post_load, validate

from odoo.addons.biz_unit_test.utils.consts import Formats
from odoo.addons.biz_unit_test.schemas.fields import Date, DateTime


class DateSchema(Schema):
    d = Date(required=True, allow_none=False)


class DateTimeSchema(Schema):
    dt = DateTime(required=True, allow_none=False)


class DateRangeSchema(Schema):
    start = Date(required=True, allow_none=False)
    end = Date(required=True, allow_none=False)

    @post_load()
    def validate_start_end(self, data, *args, **kwargs):
        if data.get("start") > data.get("end"):
            raise ValidationError("Start Date must not be greater than End Date.")
        return data


class AssertMessageSchema(Schema):
    title = fields.String(allow_none=True, load_default="")
    status = fields.String(
        required=True,
        allow_none=False,
        validate=validate.OneOf(
            choices=["PASSED", "FAILED"],
            error="Status can only be one of 'PASSED' or 'FAILED'.",
        ),
    )
    msg = fields.String(allow_none=True, load_default="")
