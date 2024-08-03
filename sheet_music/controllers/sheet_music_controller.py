from odoo.http import Controller, route, request
from odoo.addons.web.controllers.main import Binary


class SheetMusicController(Controller):
    @route("/sheet_music/<int:id>/view_pdf", type="http", auth="user", methods=["GET"], csrf=False)
    def view_pdf(self, id):
        try:
            status, headers, attachment = request.env["ir.http"].sudo().binary_content(
                model="sheet.music",
                id=id,
                field="attachment",
                default_mimetype="application/pdf",
            )
            response = Binary._content_image_get_response(
                status=status,
                headers=headers,
                image_base64=attachment,
                model="sheet.music",
                field="attachment",
                id=id,
            )
            return response
        except Exception:
            return request.not_found()