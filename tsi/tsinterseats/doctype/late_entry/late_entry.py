# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
from urllib.request import ftpwrapper
from frappe.model.document import Document
from frappe.utils import get_first_day, get_last_day, format_datetime,get_url_to_form,today
from frappe.utils import time_diff

class LateEntry(Document):
	def on_update(self):
		data = []
		total = 0
		month_start = get_first_day(today())
		month_end = get_last_day(today())
		late_permission = frappe.db.get_all('Late Entry',{'employee':self.employee,"permission_date": ('between',(month_start,month_end))},['*'])
		for late in late_permission:
			total_per_time = frappe.db.get_value('Late Entry',late.name,['late'])
			data.append(int(total_per_time))
		early_permission = frappe.db.get_all('Early Out',{'employee':self.employee,"permission_date": ('between',(month_start,month_end))},['*'])
		for early in early_permission:
			total_time = frappe.db.get_value('Early Out',early.name,['out'])
			data.append(int(total_time))
			
		total = sum(map(int, [i for i in data if i]))
		if total > 60:
			frappe.throw("Permission Time exceeded 60 minutes")
		if len(data) > 2:
			frappe.throw("Only two Permissions are allowed in a month.Kindly apply for Half Day Leave")

	def on_submit(self):
		frappe.db.set_value("Attendance",{"name":self.attendance},'late_entry',1)
		frappe.db.set_value("Attendance",{"name":self.attendance},'late_entry_application',self.name)
	def on_cancel(self):
		frappe.db.set_value("Attendance",{"name":self.attendance},'late_entry',0)
		frappe.db.set_value("Attendance",{"name":self.attendance},'late_entry_application','')


@frappe.whitelist()
def time_difference(in_time_value,corrected_in_time):   
    value = time_diff(in_time_value,corrected_in_time)
    val = value.total_seconds() / 60
    return val

@frappe.whitelist()
def calculate_overall_late_time(employee,late):
    data = []
    total = 0
    avaliable_time=0
    month_start = get_first_day(today())
    month_end = get_last_day(today())
    late_permission = frappe.db.get_all('Late Entry',{'employee':employee,"permission_date": ('between',(month_start,month_end))},['*'])
    for late in late_permission:
        total_per_time = frappe.db.get_value('Late Entry',late.name,['late'])
        data.append(int(total_per_time))
    early_permission = frappe.db.get_all('Early Out',{'employee':employee,"permission_date": ('between',(month_start,month_end))},['*'])
    for early in early_permission:
        total_time = frappe.db.get_value('Early Out',early.name,['out'])
        data.append(int(total_time))
        
    total = sum(map(int, [i for i in data if i]))
    total_hours = total
    avaliable_time=60-total
    return total_hours,avaliable_time


@frappe.whitelist()
def in_time(attendance_name):
    value=frappe.db.get_value("Attendance",{"name":attendance_name},['in_time'])
    return value

@frappe.whitelist()
def date_validation(date):
    dayss = today() <date
    return dayss