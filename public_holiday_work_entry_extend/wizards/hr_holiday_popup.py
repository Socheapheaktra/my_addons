from odoo import models


class HolidayPopup(models.TransientModel):
    _inherit = "hr.holiday.popup"

    def compute_apply(self):
        super(HolidayPopup, self).compute_apply()

        holidays = self.env["hr.holiday.year"].search([("id", "in", self.holiday_year_id.ids)])
        for holiday in holidays:
            calendars = self.env["resource.calendar"].search([("id", "in", holiday.resource_calendar_ids.ids)])
            for calendar in calendars:
                work_entry = self.env.ref("hr_work_entry.work_entry_type_attendance")
                calendar.global_leave_ids.write({"work_entry_type_id": work_entry.id})
