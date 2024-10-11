from datetime import date, datetime

from odoo.tests import BaseCase
from odoo.tools.date_utils import start_of

from odoo.addons.biz_unit_test.utils.tools import get_messages
from odoo.addons.biz_unit_test.utils.decorator import blueprint as blp
from odoo.addons.biz_unit_test.schemas.employee_schema import EmployeeCreateSchema, EmployeeContractSchema
from odoo.addons.biz_unit_test.schemas.time_off_schema import TimeOffCreateSchema


class BaseTestHelper(BaseCase):
    def assertEqual(self, first, second, msg=None, title=None):
        err_msg, msg = get_messages(title=title, message=msg)
        try:
            super(BaseTestHelper, self).assertEqual(first, second, err_msg)
        except AssertionError as error:
            print(error)
        print(msg)

    def assertTrue(self, expr, msg=None, title=None):
        err_msg, msg = get_messages(title=title, message=msg)
        try:
            super(BaseTestHelper, self).assertTrue(expr, err_msg)
        except AssertionError as error:
            print(error)
        print(msg)

    @classmethod
    @blp.argument(EmployeeCreateSchema())
    def create_employee(cls, fname, lname, name, working_date=None, working_time=None):
        """
        Create a dummy employee for testing purposes

        :param str fname: First Name
        :param str lname: Last Name
        :param str name: Full Name
        :param date working_date: Employee's Start Working Date
        :param int working_time: Employee's Working Time
        :return: Employee Object
        """
        employee = cls.env["hr.employee"].create([{
            "fname": fname,
            "lname": lname,
            "name": name,
            "working_date": start_of(date.today(), "year") if not working_date else working_date,
            "resource_calendar_id": working_time if working_time else working_time,
        }])
        return employee

    @classmethod
    def create_working_time(cls, vals):
        if "attendance_ids" in vals:
            temp = vals.pop("attendance_ids")
            vals["attendance_ids"] = [
                (
                    0, 0,
                    {**val, 'work_entry_type_id': cls.env.ref("hr_work_entry.work_entry_type_attendance").id},
                ) for val in temp]
        working_time = cls.env["resource.calendar"].create(vals)
        return working_time

    @classmethod
    def create_working_time_8_5_normal(cls):
        vals = {
            "name": "8AM-5PM (8:00-12:00, 13:00-17:00)",
            "company_id": False,
            "full_time_required_hours": 40,
            "hours_per_day": 8,
            "tz": "Asia/Phnom_Penh",
            "attendance_ids": [
                {
                    "name": "Monday Morning",
                    "dayofweek": "0",
                    "hour_from": 8.0,
                    "hour_to": 12.0,
                    "break_from": 0.0,
                    "break_to": 0.0,
                    "day_period": "morning",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Monday Afternoon",
                    "dayofweek": "0",
                    "hour_from": 13.0,
                    "hour_to": 17.0,
                    "break_from": 0.0,
                    "break_to": 0.0,
                    "day_period": "afternoon",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Tuesday Morning",
                    "dayofweek": "1",
                    "hour_from": 8.0,
                    "hour_to": 12.0,
                    "break_from": 0.0,
                    "break_to": 0.0,
                    "day_period": "morning",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Tuesday Afternoon",
                    "dayofweek": "1",
                    "hour_from": 13.0,
                    "hour_to": 17.0,
                    "break_from": 0.0,
                    "break_to": 0.0,
                    "day_period": "afternoon",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Wednesday Morning",
                    "dayofweek": "2",
                    "hour_from": 8.0,
                    "hour_to": 12.0,
                    "break_from": 0.0,
                    "break_to": 0.0,
                    "day_period": "morning",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Wednesday Afternoon",
                    "dayofweek": "2",
                    "hour_from": 13.0,
                    "hour_to": 17.0,
                    "break_from": 0.0,
                    "break_to": 0.0,
                    "day_period": "afternoon",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Thursday Morning",
                    "dayofweek": "3",
                    "hour_from": 8.0,
                    "hour_to": 12.0,
                    "break_from": 0.0,
                    "break_to": 0.0,
                    "day_period": "morning",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Thursday Afternoon",
                    "dayofweek": "3",
                    "hour_from": 13.0,
                    "hour_to": 17.0,
                    "break_from": 0.0,
                    "break_to": 0.0,
                    "day_period": "afternoon",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Friday Morning",
                    "dayofweek": "4",
                    "hour_from": 8.0,
                    "hour_to": 12.0,
                    "break_from": 0.0,
                    "break_to": 0.0,
                    "day_period": "morning",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Friday Afternoon",
                    "dayofweek": "4",
                    "hour_from": 13.0,
                    "hour_to": 17.0,
                    "break_from": 0.0,
                    "break_to": 0.0,
                    "day_period": "afternoon",
                    "work_entry_type_id": 1
                }
            ]
        }
        working_time = cls.create_working_time(vals)
        return working_time

    @classmethod
    def create_working_time_8_5_full_time(cls):
        vals = {
            "name": "8AM-5PM (8:00-17:00)",
            "company_id": False,
            "full_time_required_hours": 40,
            "hours_per_day": 8,
            "tz": "Asia/Phnom_Penh",
            "attendance_ids": [
                {
                    "name": "Monday",
                    "dayofweek": "0",
                    "hour_from": 8.0,
                    "hour_to": 17.0,
                    "break_from": 12.0,
                    "break_to": 13.0,
                    "day_period": "full_day",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Tuesday",
                    "dayofweek": "1",
                    "hour_from": 8.0,
                    "hour_to": 17.0,
                    "break_from": 12.0,
                    "break_to": 13.0,
                    "day_period": "full_day",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Wednesday",
                    "dayofweek": "2",
                    "hour_from": 8.0,
                    "hour_to": 17.0,
                    "break_from": 12.0,
                    "break_to": 13.0,
                    "day_period": "full_day",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Thursday",
                    "dayofweek": "3",
                    "hour_from": 8.0,
                    "hour_to": 17.0,
                    "break_from": 12.0,
                    "break_to": 13.0,
                    "day_period": "full_day",
                    "work_entry_type_id": 1
                },
                {
                    "name": "Friday",
                    "dayofweek": "4",
                    "hour_from": 8.0,
                    "hour_to": 17.0,
                    "break_from": 12.0,
                    "break_to": 13.0,
                    "day_period": "full_day",
                    "work_entry_type_id": 1
                }
            ]
        }
        working_time = cls.create_working_time(vals)
        return working_time

    @classmethod
    @blp.argument(EmployeeContractSchema())
    def create_contract(cls, name, employee_id, date_start, structure_type_id, resource_calendar_id, wage):
        """
        Create Dummy Contract for an Employee with Default Salary Structure Type

        :param str name: Contract Name
        :param int employee_id: Employee ID
        :param date date_start: Start Date of Contract
        :param int structure_type_id: Salary Structure Type ID
        :param int resource_calendar_id: Employee's Working Time
        :param float wage: Employee's Salary
        :return: HrContract
        """
        contract = cls.env["hr.contract"].create([{
            "name": name,
            "employee_id": employee_id,
            "date_start": date_start,
            "structure_type_id": structure_type_id,
            "resource_calendar_id": resource_calendar_id,
            "resident_type_new": "resident",
            "wage": wage,
            "state": "open",
        }])
        return contract

    @classmethod
    def create_unpaid_time_off_type(cls):
        unpaid_leave = cls.env["hr.leave.type"].create([{
            "name": "Unpaid",
            "check_leave_unpaid": True,
            "allocation_type": "no",
            "request_unit": "hour",
            "work_entry_type_id": cls.env.ref("hr_work_entry_contract.work_entry_type_unpaid_leave").id,
        }])
        return unpaid_leave

    @classmethod
    @blp.argument(TimeOffCreateSchema())
    def create_time_off(
            cls,
            name,
            employee_id,
            holiday_status_id,
            request_date_from,
            request_date_to,
            request_hour_from,
            request_hour_to,
            date_from,
            date_to,
            request_unit_half=False,
            request_unit_hours=False,
            request_date_from_period='am',
    ):
        """
        Helper function for create time off

        :param str name: Reason
        :param int employee_id: Employee
        :param int holiday_status_id: TimeOff Type
        :param date request_date_from: Date From
        :param date request_date_to: Date To
        :param str request_hour_from: Hour From
        :param str request_hour_to: Hour To
        :param datetime date_from: DateTime From
        :param datetime date_to: DateTime To
        :param bool request_unit_half: half day
        :param bool request_unit_hours: request in hour
        :param str request_date_from_period: period of leave request has taken
        :return: LeaveRequest
        """
        time_off = cls.env["hr.leave"].create([{
            "name": name,
            "employee_id": employee_id,
            "holiday_status_id": holiday_status_id,
            "request_date_from": request_date_from,
            "request_date_to": request_date_to,
            "date_from": date_from,
            "date_to": date_to,
            "request_unit_half": request_unit_half,
            "request_unit_hours": request_unit_hours,
            "state": "validate",
        }])
        return time_off
