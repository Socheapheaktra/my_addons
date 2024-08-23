import io
import yt_dlp

from contextlib import redirect_stdout

from odoo.http import Controller, route, request, Response
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
        except Exception as error:
            print(error)
            return request.not_found()

    @route("/sheet_music/<int:id>/download", type="http", auth="user", methods=["GET"], csrf=False)
    def download_music(self, id):

        sheet_music = request.env["sheet.music"].browse(id)
        video_url = sheet_music.youtube_link

        ctx = {
            "outtmpl": "-",
            "logtostderr": True,
        }

        buffer = io.BytesIO()
        with redirect_stdout(buffer), yt_dlp.YoutubeDL(ctx) as foo:
            foo.download([video_url])

        file_path = io.BytesIO(buffer.getvalue())

        file_length = len(file_path.getvalue())

        response = Response(
            file_path.getvalue(),
            status=200,
            content_type="video/mp4",
            headers=[
                ("Content-Disposition", f"attachment; filename={sheet_music.name}.mp4"),
            ]
        )
        return response
