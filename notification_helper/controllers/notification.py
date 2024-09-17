import json

from odoo.http import Controller, route, Response

from odoo.addons.notification_helper.utils.functions import _get_access_token


class NotificationController(Controller):
    @route("/api/app-hr/v1/fcm-token", auth="none", type="http", methods=["GET"], csrf=False)
    def get_fcm_token(self):
        token = _get_access_token()

        data = {
            "access_token": token,
        }
        response = Response(json.dumps(data), status=200, content_type="application/json")
        return response
