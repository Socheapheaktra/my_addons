from enum import Enum

from odoo.tools import config


class FirebaseEnum(Enum):
    SERVICE_ACCOUNT_PATH = config.get("google_application_credentials", "")
    SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
    PROJECT_ID = config.get("firebase_project_id", "")
    URL = config.get("firebase_notification_url", "") % {
        "project_id": PROJECT_ID
    }
