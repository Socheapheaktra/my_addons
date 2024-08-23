from odoo import models, fields, api


class SheetMusic(models.Model):
    _name = "sheet.music"
    _description = "Sheet Music"

    name = fields.Char(
        string="Title",
        required=True,
    )
    composer_id = fields.Many2one(
        string="Composer",
        comodel_name="music.composer",
        required=True,
    )
    category_ids = fields.Many2many(
        string="Category",
        comodel_name="music.category",
        relation="sheet_music_category_rel",
        column1="sheet_music_id",
        column2="category_id",
    )
    attachment = fields.Binary(
        string="File",
        attachment=False,
    )
    youtube_link = fields.Char(
        string="Youtube Link",
    )

    @api.model
    def create(self, vals):
        res = super(SheetMusic, self).create(vals)

        if "attachment" in vals:
            attachment_data = {
                "name": res.name,
                "datas": vals["attachment"],
                "res_model": self._name,
                "res_id": res.id,
                "res_field": "attachment",
            }
            self.env["ir.attachment"].create([attachment_data])

        return res

    def action_view_pdf(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_url",
            "url": f"/sheet_music/{self.id}/view_pdf",
            "target": "new",
        }

        return action

    def action_download(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_url",
            "url": f"/sheet_music/{self.id}/download",
            "target": "new"
        }

        return action
