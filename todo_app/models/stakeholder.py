from odoo import models, fields


class StakeHolder(models.Model):
    _name = "stakeholder"
    _description = "Helps you define which Stakeholder the tasks belong to"

    name = fields.Char(
        string="Stakeholder Name",
        require=True,
    )
