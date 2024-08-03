import base64

from odoo import models, fields, api
from odoo.modules.module import get_module_resource


class MusicComposer(models.Model):
    _name = "music.composer"
    _description = "Music Composer"
    _inherit = ["image.mixin"]

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Composer name already exist!")
    ]

    @api.model
    def _get_default_image(self):
        image_path = get_module_resource("sheet_music", "static/src/img", "avatar.png")
        return base64.b64encode(open(image_path, "rb").read())

    name = fields.Char(
        string="Name",
        required=True,
    )
    image_1920 = fields.Image(default=_get_default_image)

    description = fields.Text(
        string="Description",
    )
