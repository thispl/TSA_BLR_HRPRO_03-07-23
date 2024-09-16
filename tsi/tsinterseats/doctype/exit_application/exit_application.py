# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ExitApplication(Document):
	pass

@frappe.whitelist()
def exit_out_time(employee,date):
    value=frappe.db.get_value("Attendance",{"employee":employee,"attendance_date":date},['out_time'])
    return value

@frappe.whitelist()
def exit_in_time(employee,date):
    value=frappe.db.get_value("Attendance",{"employee":employee,"attendance_date":date},['in_time'])
    return value