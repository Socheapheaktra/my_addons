import random
from datetime import time

from odoo.tests import SavepointCase
from odoo.tools.date_utils import start_of, end_of

from odoo.addons.resource.models.resource import float_to_time

from odoo.addons.biz_unit_test.tests.base_test import BaseTestHelper
from odoo.addons.biz_unit_test.utils.date_utils import *


class TestWorkEntry(SavepointCase, BaseTestHelper):
    @classmethod
    def setUpClass(cls):
        super(TestWorkEntry, cls).setUpClass()
        cls.env.cr.execute("DELETE FROM hr_work_entry WHERE TRUE")
        cls.structure_type_id = 7  # This is static for now, later will create a function.
        cls.working_time_normal = cls.create_working_time_8_5_normal()
        cls.working_time_full = cls.create_working_time_8_5_full_time()
        cls.employee = cls.create_employee(
            fname="Test",
            lname="Employee",
            name="Test Employee",
            working_time=cls.working_time_full.id,
        )
        cls.contract = cls.create_contract(
            name=cls.employee.name + "'s Contract",
            employee_id=cls.employee.id,
            date_start=date_to_string(start_of(date.today(), "year")),
            structure_type_id=cls.structure_type_id,
            resource_calendar_id=cls.working_time_normal.id,
            wage=500,
        )
        cls.unpaid_leave_type = cls.create_unpaid_time_off_type()

    def test_00_confirm_setup(self):
        print("Test Confirm Setup")
        self.assertTrue(
            title="Create Working Time Full",
            expr=self.working_time_full,
            msg="Failed to create Working Time Full.",
        )
        self.assertTrue(
            title="Create Working Time Normal",
            expr=self.working_time_normal.exists(),
            msg="Failed to create Working Time Normal.",
        )
        self.assertTrue(
            title="Create Employee",
            expr=self.employee.exists(),
            msg="Failed to create Dummy Employee.",
        )
        self.assertTrue(
            title="Create Employee Contract",
            expr=self.contract.exists(),
            msg="Failed to create Employee Contract",
        )
        self.assertTrue(
            title="Check Employee Contract",
            expr=self.employee.contract_running_id.exists(),
            msg="Employee Contract not exists.",
        )

        print("\n\n")

    def test_01_work_entry_unpaid_on_normal_working_time(self):
        """
        This test is to make sure UnpaidLeave counts correctly on Normal Working Time

        Case: UnpaidLeave Request 1 Full Day
        Expected Result: 2 WorkEntries on same day (morning, afternoon), half day each

        :return: None
        """
        print("Test Work Entry Unpaid On Normal Working Time")

        self.employee.resource_calendar_id = self.working_time_normal.id
        self.contract.resource_calendar_id = self.working_time_normal.id
        self.assertEqual(
            title="Check Employee Working Time Normal.",
            first=self.employee.resource_calendar_id.id,
            second=self.working_time_normal.id,
            msg="Employee Working Time is not normal.",
        )
        self.assertEqual(
            title="Check Contract Working Time Normal",
            first=self.contract.resource_calendar_id.id,
            second=self.working_time_normal.id,
            msg="Contract Working Time is not normal."
        )

        date_start = start_of(value=date.today(), granularity="month")
        date_stop = end_of(value=date.today(), granularity="month")

        working_days = self.employee.resource_calendar_id.attendance_ids.mapped("dayofweek")
        date_ranges = [d for d in date_range(start=date_start, end=date_stop) if str(d.weekday()) in working_days]

        request_date = random.choice(date_ranges)
        work_from = min(self.working_time_normal.attendance_ids.mapped("hour_from"))
        work_to = max(self.working_time_full.attendance_ids.mapped("hour_to"))
        date_from = datetime.combine(request_date, float_to_time(work_from))
        date_to = datetime.combine(request_date, float_to_time(work_to))
        leave_request = self.create_time_off(
            name="Test Leave Request",
            employee_id=self.employee.id,
            holiday_status_id=self.unpaid_leave_type.id,
            request_date_from=request_date,
            request_date_to=request_date,
            date_from=datetime_to_utc(dt=date_from),
            date_to=datetime_to_utc(dt=date_to),
        )
        self.assertTrue(
            title="Create Leave Request",
            expr=leave_request.exists(),
            msg="Failed to create LeaveRequest.",
        )

        # LeaveResource needed to be created before WorkEntry Generation to Generate Time Off WorkEntries
        leave_request.sudo()._create_resource_leave()

        work_entries = self.employee \
            .contract_running_id \
            .with_context(force_work_entry_generation=True) \
            ._generate_work_entries(date_start, date_stop)
        self.assertTrue(
            title="Generate Work Entries",
            expr=work_entries.exists(),
            msg="Failed to generate WorkEntries.",
        )

        unpaid_work_entries = work_entries.filtered(lambda l: l.leave_id.id in leave_request.ids)
        self.assertTrue(
            title="Check Unpaid WorkEntries.",
            expr=unpaid_work_entries.exists(),
            msg="Failed to generate Unpaid Work Entries"
        )

        unpaid_work_entries_count = sum(unpaid_work_entries.mapped("num_day"))
        unpaid_leave_count = sum(leave_request.mapped("number_of_days"))
        self.assertEqual(
            title="Compare Unpaid Work Entries with Unpaid Leave Requests.",
            first=unpaid_work_entries_count,
            second=unpaid_leave_count,
            msg=f"Work Entries({unpaid_work_entries_count}) not equals to Leave Request({unpaid_leave_count})."
        )

        print("\n\n")

    def test_02_work_entry_unpaid_on_full_day_working_time(self):
        """
        This test is to make sure UnpaidLeave counts correctly on Full Day Working Time

        Case UnpaidLeave Request 1 Full Day
        Expected Result: 2 WorkEntries on same day (morning, afternoon), half day each

        Bug Report: WorkEntry Unpaid 2 (morning, afternoon), both counted as 1 day which total 2 days in 1 request

        :return: None
        """
        print("Test WorkEntry Unpaid on Full Day Working Time")

        self.employee.resource_calendar_id = self.working_time_full.id
        self.contract.resource_calendar_id = self.working_time_full.id

        self.assertEqual(
            title="Check Full Time Calendar.",
            first=self.employee.resource_calendar_id.id,
            second=self.working_time_full.id,
            msg="Employee Working Time is not Full Day."
        )
        self.assertEqual(
            title="Check Full Time Calendar in Contract.",
            first=self.contract.resource_calendar_id.id,
            second=self.working_time_full.id,
            msg="Working Time in Contract is not Full Day."
        )

        date_start = start_of(value=date.today(), granularity="month")
        date_stop = end_of(value=date.today(), granularity="month")

        working_days = self.employee.resource_calendar_id.attendance_ids.mapped("dayofweek")
        date_ranges = [d for d in date_range(start=date_start, end=date_stop) if str(d.weekday()) in working_days]

        request_date = random.choice(date_ranges)
        work_from = min(self.working_time_normal.attendance_ids.mapped("hour_from"))
        work_to = max(self.working_time_full.attendance_ids.mapped("hour_to"))
        date_from = datetime.combine(request_date, float_to_time(work_from))
        date_to = datetime.combine(request_date, float_to_time(work_to))
        leave_request = self.create_time_off(
            name="Test Leave Request",
            employee_id=self.employee.id,
            holiday_status_id=self.unpaid_leave_type.id,
            request_date_from=request_date,
            request_date_to=request_date,
            date_from=datetime_to_utc(dt=date_from),
            date_to=datetime_to_utc(dt=date_to),
        )
        self.assertTrue(
            title="Create Leave Request",
            expr=leave_request.exists(),
            msg="Failed to create LeaveRequest.",
        )

        # LeaveResource needed to be created before WorkEntry Generation to Generate Time Off WorkEntries
        leave_request.sudo()._create_resource_leave()

        work_entries = self.employee \
            .contract_running_id \
            .with_context(force_work_entry_generation=True) \
            ._generate_work_entries(date_start, date_stop)
        self.assertTrue(
            title="Generate Work Entries",
            expr=work_entries.exists(),
            msg="Failed to generate WorkEntries.",
        )

        unpaid_work_entries = work_entries.filtered(lambda l: l.leave_id.id in leave_request.ids)
        self.assertTrue(
            title="Check Unpaid WorkEntries.",
            expr=unpaid_work_entries.exists(),
            msg="Failed to generate Unpaid Work Entries"
        )

        unpaid_work_entries_count = sum(unpaid_work_entries.mapped("num_day"))
        unpaid_leave_count = sum(leave_request.mapped("number_of_days"))
        self.assertEqual(
            title="Compare Unpaid Work Entries with Unpaid Leave Requests.",
            first=unpaid_work_entries_count,
            second=unpaid_leave_count,
            msg=f"Work Entries({unpaid_work_entries_count}) not equals to Leave Request({unpaid_leave_count})."
        )

        print("\n\n")

    def test_03_work_entry_unpaid_hour_on_normal_working_time(self):
        print("Test Work Entry Unpaid Hour On Normal Working Time")

        self.employee.resource_calendar_id = self.working_time_normal.id
        self.contract.resource_calendar_id = self.working_time_normal.id
        self.assertEqual(
            title="Check Employee Working Time Normal.",
            first=self.employee.resource_calendar_id.id,
            second=self.working_time_normal.id,
            msg="Employee Working Time is not normal.",
        )

        date_start = start_of(value=date.today(), granularity="month")
        date_stop = end_of(value=date.today(), granularity="month")

        working_days = self.employee.resource_calendar_id.attendance_ids.mapped("dayofweek")
        date_ranges = [d for d in date_range(start=date_start, end=date_stop) if str(d.weekday()) in working_days]

        request_date = random.choice(date_ranges)
        hour_from = time(hour=8, minute=0, second=0)
        hour_to = time(hour=10, minute=0, second=0)
        date_from = datetime.combine(date=request_date, time=hour_from)
        date_to = datetime.combine(date=request_date, time=hour_to)
        leave_request = self.create_time_off(
            name="Test Leave Request",
            employee_id=self.employee.id,
            holiday_status_id=self.unpaid_leave_type.id,
            request_date_from=request_date,
            request_date_to=request_date,
            request_hour_from="8",
            request_hour_to="10",
            date_from=datetime_to_utc(dt=date_from),
            date_to=datetime_to_utc(dt=date_to),
        )
        self.assertTrue(
            title=f"Create Leave Request Hours({leave_request.number_of_days})",
            expr=leave_request.exists(),
            msg="Failed to create LeaveRequest.",
        )

        # LeaveResource needed to be created before WorkEntry Generation to Generate Time Off WorkEntries
        leave_request.sudo()._create_resource_leave()

        work_entries = self.employee \
            .contract_running_id \
            .with_context(force_work_entry_generation=True) \
            ._generate_work_entries(date_start, date_stop)
        self.assertTrue(
            title="Generate Work Entries",
            expr=work_entries.exists(),
            msg="Failed to generate WorkEntries.",
        )

        unpaid_work_entries = work_entries.filtered(lambda l: l.leave_id.id in leave_request.ids)
        self.assertTrue(
            title="Generate WorkEntries.",
            expr=unpaid_work_entries.exists(),
            msg="Failed to generate Work Entries"
        )

        unpaid_work_entries_count = sum(unpaid_work_entries.mapped("num_day"))
        unpaid_leave_count = sum(leave_request.mapped("number_of_days"))
        self.assertEqual(
            title=f"Compare Work Entries({unpaid_work_entries_count}) with Leave ({unpaid_leave_count}).",
            first=unpaid_work_entries_count,
            second=unpaid_leave_count,
            msg=f"Work Entries({unpaid_work_entries_count}) not equals to Leave Request({unpaid_leave_count})."
        )

        print("\n\n")

    def test_04_work_entry_unpaid_hour_on_full_day_working_time(self):
        print("Test Work Entry Unpaid Hour On Full Day Working Time")

        self.employee.resource_calendar_id = self.working_time_full.id
        self.contract.resource_calendar_id = self.working_time_full.id
        self.assertEqual(
            title="Check Employee Working Time Full",
            first=self.employee.resource_calendar_id.id,
            second=self.working_time_full.id,
            msg="Employee Working Time is not Full",
        )

        date_start = start_of(value=date.today(), granularity="month")
        date_stop = end_of(value=date.today(), granularity="month")

        working_days = self.employee.resource_calendar_id.attendance_ids.mapped("dayofweek")
        date_ranges = [d for d in date_range(start=date_start, end=date_stop) if str(d.weekday()) in working_days]

        request_date = random.choice(date_ranges)
        hour_from = time(hour=14, minute=0, second=0)
        hour_to = time(hour=17, minute=0, second=0)
        date_from = datetime.combine(date=request_date, time=hour_from)
        date_to = datetime.combine(date=request_date, time=hour_to)
        leave_request = self.create_time_off(
            name="Test Leave Request",
            employee_id=self.employee.id,
            holiday_status_id=self.unpaid_leave_type.id,
            request_date_from=request_date,
            request_date_to=request_date,
            request_hour_from="14",
            request_hour_to="17",
            date_from=datetime_to_utc(dt=date_from),
            date_to=datetime_to_utc(dt=date_to),
        )
        self.assertTrue(
            title=f"Create Leave Request Hours({leave_request.number_of_days})",
            expr=leave_request.exists(),
            msg="Failed to create LeaveRequest.",
        )

        # LeaveResource needed to be created before WorkEntry Generation to Generate Time Off WorkEntries
        leave_resource = leave_request.sudo()._create_resource_leave()
        print(leave_resource)

        work_entries = self.employee \
            .contract_running_id \
            .with_context(force_work_entry_generation=True) \
            ._generate_work_entries(date_start, date_stop)
        self.assertTrue(
            title="Generate Work Entries",
            expr=work_entries.exists(),
            msg="Failed to generate WorkEntries.",
        )

        unpaid_work_entries = work_entries.filtered(lambda l: l.leave_id.id in leave_request.ids)
        self.assertTrue(
            title="Generate WorkEntries.",
            expr=unpaid_work_entries.exists(),
            msg="Failed to generate Work Entries"
        )

        unpaid_work_entries_count = sum(unpaid_work_entries.mapped("num_day"))
        unpaid_leave_count = sum(leave_request.mapped("number_of_days"))
        self.assertEqual(
            title=f"Compare Work Entries({unpaid_work_entries_count}) with Leave ({unpaid_leave_count}).",
            first=unpaid_work_entries_count,
            second=unpaid_leave_count,
            msg=f"Work Entries({unpaid_work_entries_count}) not equals to Leave Request({unpaid_leave_count})."
        )

        print("\n\n")

    def test_05_work_entry_unpaid_half_day_on_normal_working_time(self):
        print("Test Work Entry Unpaid Half Day On Normal Working Time")

        self.employee.resource_calendar_id = self.working_time_normal.id
        self.contract.resource_calendar_id = self.working_time_normal.id
        self.assertEqual(
            title="Check Employee Working Time Normal",
            first=self.employee.resource_calendar_id.id,
            second=self.working_time_normal.id,
            msg="Employee Working Time is not normal",
        )
        self.assertEqual(
            title="Check Contract Working Time Normal",
            first=self.contract.resource_calendar_id.id,
            second=self.working_time_normal.id,
            msg="Contract Working Time is not normal"
        )

        date_start = start_of(value=date.today(), granularity="month")
        date_stop = end_of(value=date.today(), granularity="month")

        working_days = self.employee.resource_calendar_id.attendance_ids.mapped("dayofweek")
        date_ranges = [d for d in date_range(start=date_start, end=date_stop) if str(d.weekday()) in working_days]

        request_date = random.choice(date_ranges)
        work_from = min(self.working_time_normal.attendance_ids.mapped("hour_from"))
        work_to = min(self.working_time_full.attendance_ids.mapped("hour_to"))
        date_from = datetime.combine(request_date, float_to_time(work_from))
        date_to = datetime.combine(request_date, float_to_time(work_to))
        leave_request = self.create_time_off(
            name="Test Leave Request",
            employee_id=self.employee.id,
            holiday_status_id=self.unpaid_leave_type.id,
            request_date_from=request_date,
            request_date_to=request_date,
            request_date_from_period="am",
            date_from=datetime_to_utc(dt=date_from),
            date_to=datetime_to_utc(dt=date_to),
        )
        self.assertTrue(
            title=f"Create Leave Request ({leave_request.number_of_days})",
            expr=leave_request.exists(),
            msg="Failed to create LeaveRequest.",
        )

        # LeaveResource needed to be created before WorkEntry Generation to Generate Time Off WorkEntries
        leave_request.sudo()._create_resource_leave()

        work_entries = self.employee \
            .contract_running_id \
            .with_context(force_work_entry_generation=True) \
            ._generate_work_entries(date_start, date_stop)
        self.assertTrue(
            title="Generate Work Entries",
            expr=work_entries.exists(),
            msg="Failed to generate WorkEntries.",
        )

        unpaid_work_entries = work_entries.filtered(lambda l: l.leave_id.id in leave_request.ids)
        self.assertTrue(
            title="Check Unpaid WorkEntries.",
            expr=unpaid_work_entries.exists(),
            msg="Failed to generate Unpaid Work Entries"
        )

        unpaid_work_entries_count = sum(unpaid_work_entries.mapped("num_day"))
        unpaid_leave_count = sum(leave_request.mapped("number_of_days"))
        self.assertEqual(
            title=f"Compare Work Entries({unpaid_work_entries_count}) with Leave Requests({unpaid_leave_count})",
            first=unpaid_work_entries_count,
            second=unpaid_leave_count,
            msg=f"Work Entries({unpaid_work_entries_count}) not equals to Leave Request({unpaid_leave_count})."
        )

        print("\n\n")

    def test_06_work_entry_unpaid_half_day_on_full_day_working_time(self):
        pass
