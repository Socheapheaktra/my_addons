from google.auth.transport import requests
from google.oauth2 import service_account

from odoo.addons.notification_helper.utils.consts import FirebaseEnum


def _get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        filename=FirebaseEnum.SERVICE_ACCOUNT_PATH.value,
        scopes=FirebaseEnum.SCOPES.value,
    )
    request = requests.Request()
    credentials.refresh(request)
    token = credentials.token
    return token
