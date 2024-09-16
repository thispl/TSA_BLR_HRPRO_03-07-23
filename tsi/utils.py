import frappe
from frappe.model.document import Document
from frappe.utils import time_diff
from datetime import datetime
from datetime import timedelta
import pdfkit

from frappe import throw,_
from frappe.utils import (
    add_days,
    add_months,
    cint,
    date_diff,
    flt,
    get_first_day,
    get_last_day,
    get_link_to_form,
    getdate,
    rounded,
    today,
)
from frappe.utils import get_first_day, get_last_day, format_datetime,get_url_to_form,today
from frappe.utils.data import ceil, get_time, get_year_start
import json
import datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from datetime import date, timedelta,time
from frappe.utils import get_url_to_form
import math
import dateutil.relativedelta
from datetime import timedelta, datetime
from frappe.utils import cstr, add_days, date_diff,format_datetime




# @frappe.whitelist()
# def delete_attendance_records():
#     # Assuming 'attendance_date' and 'employee_id' are the field names in the `tabAttendance` table
#     frappe.db.sql("""
#         DELETE FROM `tabAttendance`
#         WHERE 
#             (
#                 (
#                     (MONTH(attendance_date) = 1 OR MONTH(attendance_date) = 2)
#                     AND DAYOFWEEK(attendance_date) = 1
#                     AND status = 'Absent'
#                 )
#             )
#     """)
#     frappe.db.commit()  # Commit the transaction after deletion
#     return "Records deleted successfully"

import frappe
from frappe import _

@frappe.whitelist()
def attendance_correction():
    # Fetch the 'on_duty_application' for the given criteria
    att = frappe.db.get_value(
        "Attendance",
        {"status": "Absent", "attendance_date": "2024-04-18"},  # Ensure correct date format
        ["name"]
    )
    for i in att:
        setatt=frappe.db.get_value(
        "Attendance",
        {"name": i},  # Ensure correct date format
        ["shift_status"])
        if setatt:
            frappe.db.sql(
                """UPDATE `tabAttendance` 
                SET shift_status = 'P(OD)' 
                WHERE name = i
                AND attendance_date = '2024-04-18'
                AND status = 'Absent'""",
                as_dict=True
            )
            frappe.db.commit()

