from odoo.addons.biz_unit_test.utils.consts import Colors, AssertStatus
from odoo.addons.biz_unit_test.schemas.helper_schema import AssertMessageSchema
from odoo.addons.biz_unit_test.utils.decorator import blueprint as blp


@blp.argument(AssertMessageSchema())
def set_message(title, status, msg):
    bold = Colors.BOLD
    header = Colors.HEADER
    color = Colors.FAIL if status == AssertStatus.FAIL else Colors.OKGREEN
    if status == AssertStatus.FAIL:
        message = f"{header}{bold}{title}: {color}{status}{Colors.ENDC}\n{msg}"
    else:
        message = f"{header}{bold}{title}: {color}{status}{Colors.ENDC}"
    return message


def get_messages(title, message):
    err_msg = set_message(title=title, status=AssertStatus.FAIL, msg=message)
    msg = set_message(title=title, status=AssertStatus.PASS, msg=message)

    return err_msg, msg
