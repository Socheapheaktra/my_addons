from marshmallow import Schema, fields

from odoo.addons.biz_unit_test.schemas.fields import Date


class EmployeeCreateSchema(Schema):
    fname = fields.String(required=True, allow_none=False)
    lname = fields.String(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    working_date = Date(allow_none=True, load_default=None)
    working_time = fields.Integer(allow_none=True, load_default=None)


class EmployeeContractSchema(Schema):
    name = fields.String(required=True, allow_none=False)
    employee_id = fields.Integer(required=True, allow_none=False)
    date_start = Date(required=True, allow_none=False)
    structure_type_id = fields.Integer(required=True, allow_none=False)
    resource_calendar_id = fields.Integer(required=True, allow_none=False)
    wage = fields.Float(required=True, allow_none=False, validate=lambda x: x > 0)
