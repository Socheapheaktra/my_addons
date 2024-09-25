from odoo import models, fields


class PersonInCharge(models.Model):
    _name = "person.in.charge"
    _description = "Helps you keep track on who is responsible for each tasks."

    name = fields.Char(
        string="Name",
        require=True,
    )
    type = fields.Selection(
        selection=[
            ("pmo", "Product Owner"),
            ("dev", "Developer"),
        ],
        default="pmo",
    )
