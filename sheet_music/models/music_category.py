from odoo import models, fields


class MusicCategory(models.Model):
    _name = "music.category"
    _description = "Music Category"

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Cannot have duplicate music category!")
    ]

    name = fields.Char(
        string="Name",
        required=True,
    )
