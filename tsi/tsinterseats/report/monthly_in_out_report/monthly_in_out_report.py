# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from functools import total_ordering
from itertools import count
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta,datetime, time
import datetime as dt


def execute(filters=None):
	columns1 = get_columns1(filters)
	data = get_data(filters)
	return columns1, data

def get_columns1(filters):
	columns1 = []
	columns1 += [
		_("Employee ID") + ":Data/:150",
		_("Employee Name") + ":Data/:200",
		_("Department") + ":Data/:150",
		_("Designation") + ":Data/:150",
		_("DOJ") + ":Date/:100",
		_("Date") + ":Data/:150",
	]
	dates = get_dates(filters.from_date,filters.to_date)
	for date in dates:
		date = datetime.strptime(date,'%Y-%m-%d')
		day = datetime.date(date).strftime('%d')
		month = datetime.date(date).strftime('%b')
		columns1.append(_(day + '/' + month) + ":Data/:70")
	columns1.append(_("Present") + ":Data/:100")
	columns1.append(_('Half Day') +':Data/:100')
	columns1.append(_('On Duty') + ':Data/:100')
	columns1.append(_('Permission') + ':Data/:100')
	columns1.append(_("Absent") + ":Data/:100")
	columns1.append(_('Weekoff')+ ':Data/:100')
	columns1.append(_('Holiday')+ ':Data/:100')
	columns1.append(_('Paid Leave')+ ':Data/:150')
	columns1.append(_('LOP')+ ':Data/:100')
	columns1.append(_('COFF')+ ':Data/:100')
	columns1.append(_('OT')+ ':Data/:100')
	columns1.append(_('Actual Late')+ ':Data/:100')
	columns1.append(_('Late Deduct')+ ':Data/:150')
	columns1.append(_('Permission Hours')+ ':Data/:150')
	columns1.append(_('Night Shift')+ ':Data/:150')
	columns1.append(_('Casual Leave')+ ':Data/:150')
	columns1.append(_('Earned Leave')+ ':Data/:150')
	columns1.append(_('ESI Leave')+ ':Data/:150')
	columns1.append(_('Festival Holiday')+ ':Data/:150')
	columns1.append(_('NPD')+ ':Data/:150')
	columns1.append(_('Payment Days')+ ':Data/:150')
	return columns1

def get_data(filters):
	data = []
	dates = get_dates(filters.from_date, filters.to_date)
	row = ["", "", "", "", "", "Day"]
	for date in dates:
		date = datetime.strptime(date, '%Y-%m-%d')
		day = datetime.date(date).strftime('%a')
		row.append(day)
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	row.append("")
	data.append(row)
	employees = get_employees(filters)
	for emp in employees:
		dates = get_dates(filters.from_date, filters.to_date)
		row1 = [emp.name, emp.employee_name, emp.designation, emp.department, emp.date_of_joining, "Status"]
		row2 = ["", "", "", "", "", "Shift"]
		row3 = ["", "", "", "", "", "In Time"]
		row4 = ["", "", "", "", "", "Out Time"]
		row5 = ["", "", "", "", "", "Late"]
		row6 = ["", "", "", "", "", "Early"]
		row7 = ["", "", "", "", "", "TWH"]
		row8 = ["", "", "", "", "", "OT"]
		total_present = 0
		total_half_day = 0
		total_absent = 0
		total_holiday = 0
		total_weekoff = 0
		total_ot = 0
		total_od1 = 0
		total_lop = 0
		total_paid_leave = 0
		total_combo_off = 0
		n_shift = 0
		total_cl = 0
		total_sl = 0
		esi = 0
		total_esi = 0
		total_el = 0
		total_fh = 0
		total_dh = 0
		tw_days = 0
		for date in dates:
			if frappe.db.exists("Attendance", {'attendance_date': date, 'employee': emp.name, 'docstatus': ('!=', '2')}):
				att = frappe.get_doc("Attendance",{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')})
				shift_status = att.shift_status
				shift = att.shift
				in_time = att.in_time
				od_app = att.on_duty_application
				out_time = att.out_time
				working_hours = att.working_hours
				status = att.status
				leave_type = att.leave_type
				if status == "On Leave" and leave_type!='':
					if leave_type == "Casual Leave":
						row1.append("CL")
						total_paid_leave +=1
						total_cl += 1
					elif leave_type == "Sick Leave":
						row1.append("SL")
						total_paid_leave +=1
						total_sl += 1
					elif leave_type == "Compensatory Off":
						row1.append("CO")
						total_paid_leave +=1
					elif leave_type == "ESI Leave":
						row1.append("ESI")
						total_paid_leave +=1
						total_esi += 1
					elif leave_type == "Earned Leave":
						row1.append("EL")
						total_paid_leave +=1
						total_el += 1
					elif leave_type == "Leave Without Pay":
						row1.append("LWP")
						total_lop += 1
					elif leave_type == "Maternity Leave":
						row1.append("ML")
						total_paid_leave +=1
						tw_days+=1
				elif status == "On Leave" and leave_type=='':	
					row1.append("AB")
					total_absent +=1
				else:
					if shift_status:
						row1.append(shift_status)
						if shift_status =="P":
							total_present += 1
						elif shift_status == "P/PH":
							total_present +=1
						elif shift_status == "HD/PH":
							total_present +=0.5
							total_holiday +=0.5
						elif shift_status == "HD/NPD":
							total_present +=0.5
							total_holiday +=0.5
							total_dh += 0.5
						elif shift_status == "P/BH":
							total_present +=1
						elif shift_status == "HD/BH":
							total_present +=0.5
							total_holiday +=0.5
						elif shift_status == "P/FH":
							total_present +=1
						elif shift_status == "HD/FH":
							total_present +=0.5
							total_holiday +=0.5
						elif shift_status == "P/N":
							total_present +=1
							n_shift +=1
						elif shift_status == "P/AB":
							total_present +=0.5
							total_half_day +=0.5
							total_absent +=0.5
						elif shift_status == "AB/P":
							total_present +=0.5
							total_half_day +=0.5
							total_absent +=0.5
						elif shift_status == "P/NPD":
							total_present +=1
							total_dh += 1
						elif shift_status == "PN/NPD":
							total_present +=1
							total_dh += 1
						elif shift_status == "NPD/PN":
							total_present +=1
							n_shift +=1
							total_dh += 1
						elif shift_status == "NPD/PP":
							total_present +=0.5
							total_dh += 0.5
						elif shift_status == "NPD":
							total_holiday += 1
						elif shift_status == "CL":
							total_paid_leave +=1
							total_cl += 1
						elif shift_status == "SL":
							total_paid_leave +=1
							total_sl += 1
						elif shift_status == "NPD/CL":
							total_paid_leave +=0.5
							total_cl += 0.5
							total_present +=0.5
							total_dh += 0.5
						elif shift_status == "NPD/SL":
							total_paid_leave +=0.5
							total_sl += 0.5
							total_present +=0.5
							total_dh += 0.5
						elif shift_status == "EL":
							total_paid_leave += 1
							total_el += 1
						elif shift_status == "PP/EL":
							total_paid_leave +=0.5
							total_present +=0.5
							total_el += 0.5
						elif shift_status == "PP/CL":
							total_paid_leave +=0.5
							total_present +=0.5
							total_half_day +=0.5
							total_cl += 0.5	
						elif shift_status == "PP/SL":
							total_paid_leave +=0.5
							total_present +=0.5
							total_half_day +=0.5
							total_sl += 0.5	
						elif shift_status == "ESI":
							esi +=1
							total_esi += 1
						elif shift_status == "LOP":
							total_lop +=1
						elif shift_status == "PP/LOP":
							total_lop +=0.5
							total_present +=0.5
						elif shift_status == "LOP/PP":
							total_lop +=0.5
							total_present +=0.5
						elif shift_status == "AB":
							total_absent +=1
						elif shift_status == "HD/WW":
							total_present +=0.5
							total_weekoff +=0.5
						elif shift_status == "P/WW":
							total_present +=1
						elif shift_status == "WW":
							total_weekoff +=1
					else:
						row1.append('-')
				if shift:
					row2.append(shift)
				else:
					row2.append('-')
				if in_time is not None:
					in_tim = in_time.strftime('%H:%M')

				else:
					if att.on_duty_application:
						in_tim=att.session_from_time
					else:
						in_tim = '-'
				if out_time is not None:
					out_tim = out_time.strftime('%H:%M')
				else:
					if att.on_duty_application:
						out_tim=att.session_to_time
					else:
						out_tim = ''
				row3.append(in_tim)
				row4.append(out_tim)

				late_time = 0
				if shift and in_time:
					if att.late_entry_application:
						row5.append(att.late_entry_application)
					else:
						shift_time = frappe.get_value("Shift Type",{'name':att.shift},["start_time"])
						get_time = datetime.strptime(str(shift_time),'%H:%M:%S').strftime('%H:%M:%S')
						shift_start_time = dt.datetime.strptime(str(get_time),"%H:%M:%S")
						start_time = dt.datetime.combine(att.attendance_date,shift_start_time.time())
						if in_time > start_time:
							late_time = in_time - start_time
						else:
							late_time = "-"
						row5.append(str(late_time))
				else:
					late_time = "-"
					row5.append(str(late_time))
				
				early_out = 0
				if shift and out_time:
					if att.early_exit_application:
						row6.append(att.early_exit_application)

					else:
						shift_time = frappe.get_value("Shift Type", {'name': shift}, ["end_time"])
						get_time = datetime.strptime(str(shift_time), '%H:%M:%S').strftime('%H:%M:%S')
						shift_end_time = dt.datetime.strptime(str(get_time), "%H:%M:%S")
						end_time = dt.datetime.combine(att.attendance_date, shift_end_time.time())
						if out_time < end_time:
							early_out = end_time - out_time
						else:
							early_out = "-"
						row6.append(str(early_out))
				else:
					early_out = "-"
					row6.append(str(early_out))

				row7.append(working_hours)
				
				if att.get('shift_status') == "P/WW" or att.get('shift_status') == "P/PH" or att.get('shift_status') == "P/NPD" or att.get('shift_status') == "P/FH" or att.get('shift_status') == "P/BH":
					# ot_hours=(att.get(overtime_hours))
					if att.get('shift_status') == "P/FH":
						row8.append(att.get('overtime_hours', '-'))
						total_ot +=att.get('overtime_hours')
						total_fh += 1
					elif att.get('shift_status') == "P/NPD":
						row8.append(att.get('overtime_hours', '-'))
						total_ot += att.get('overtime_hours')
						total_dh += 1
					else:
						row8.append(att.get('overtime_hours', '-'))
						total_ot += att.get('overtime_hours')
				elif att.get('shift_status') == "AB":
					row8.append(att.get('overtime_hours', '-'))
					total_ot += 0
				else:
					row8.append(att.get('overtime_hours', '-'))
					total_ot += att.get('overtime_hours')
				
			else:
				hh = check_holiday(date, emp.name)
				if hh:
					frappe.errprint(hh)
					row1.append(hh)
					row2.append('-')
					row3.append('-')
					row4.append('-')
					row5.append('-')
					row6.append('-')
					row7.append('-')
					row8.append('-')
				else:
					row1.append('-')
					row2.append('-')
					row3.append('-')
					row4.append('-')
					row5.append('-')
					row6.append('-')
					row7.append('-')
					row8.append('-')
				if hh == "WH":
					total_weekoff += 1
				elif hh == "BH":
					total_holiday += 1
				elif hh == "NPD":
					total_holiday += 1
				elif hh == "PH":
					total_holiday += 1
				elif hh == "FH":
					total_holiday += 1
		
		total_od = frappe.db.sql("""select * from `tabOn Duty Application` where docstatus = 1 and od_date between '%s' and '%s' and employee = '%s'"""%(filters.from_date, filters.to_date, emp.name), as_dict=True)
		for od in total_od:
			if od.session == "Full day":
				total_od1 +=1
			elif od.session == "Second Half" or od.session == "First Half":
				total_od1 += 0.5
				total_present+=0.5
			elif od.session == "Flexible":
				total_od1 +=1

		total_combo_off = frappe.db.sql("""select count(name) as coff from `tabLeave Application` where docstatus = 1 and from_date between '%s' and '%s' and employee = '%s' and leave_type = 'Compensatory Off' """%(filters.from_date, filters.to_date, emp.name), as_dict=True)
		row1.append(total_present)
		frappe.errprint(total_present)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_half_day)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_od1)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append('-')
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_absent)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_weekoff)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_holiday)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_paid_leave)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_lop)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_combo_off[0]['coff'])
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_ot)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append('-')
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append('-')
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append('-')
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(n_shift)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_cl)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_el)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_esi)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_fh)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		row1.append(total_dh)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		tw_days += (total_present + total_weekoff + total_holiday +total_od1 +total_cl+total_sl+total_el+total_combo_off[0]['coff'])
		row1.append(tw_days)
		row2.append('-')
		row3.append('-')
		row4.append('-')
		row5.append('-')
		row6.append('-')
		row7.append('-')
		row8.append('-')
		data.append(row1)
		data.append(row2)
		data.append(row3)
		data.append(row4)
		data.append(row5)
		data.append(row6)
		data.append(row7)
		data.append(row8)
	return data

def get_dates(from_date,to_date):
	no_of_days = date_diff(add_days(to_date, 1), from_date)
	dates = [add_days(from_date, i) for i in range(0, no_of_days)]
	return dates

def check_holiday(date, emp):
	holiday_list_name = 'Holiday - TSI'

	query = """
		SELECT
			`tabHoliday`.holiday_date,
			`tabHoliday`.weekly_off,
			`tabHoliday`.others
		FROM
			`tabHoliday List`
		LEFT JOIN
			`tabHoliday` ON `tabHoliday`.parent = `tabHoliday List`.name
		WHERE
			`tabHoliday List`.name = %s AND holiday_date = %s
	"""

	holiday = frappe.db.sql(query, (holiday_list_name, date), as_dict=True)

	doj = frappe.db.get_value("Employee", {'name': emp}, "date_of_joining")
	relieving_date = frappe.db.get_value("Employee",{'name': emp}, "relieving_date")
	status = ''

	if holiday:
		if relieving_date:
			if (doj and doj < holiday[0].holiday_date) and (relieving_date and relieving_date > holiday[0].holiday_date):
				if holiday[0].weekly_off == 1:
					status = "WH"
				else:
					if holiday[0].others == "DH":
						status = "NPD"
					elif holiday[0].others == "BH":
						status = "BH"
					elif holiday[0].others == "PH":
						status = "PH"
					elif holiday[0].others == "FH":
						status = "FH"
			else:
				status = '*'
		else:
			if doj and doj < holiday[0].holiday_date:
				if holiday[0].weekly_off == 1:
					status = "WH"
				else:
					if holiday[0].others == "DH":
						status = "NPD"
					elif holiday[0].others == "BH":
						status = "BH"
					elif holiday[0].others == "PH":
						status = "PH"
					elif holiday[0].others == "FH":
						status = "FH"
			else:
				status = '*'
	return status

def get_employees(filters):
	conditions = ''
	left_employees = []
	if filters.employee:
		conditions += "and employee = '%s' " % (filters.employee)
	if filters.employee_catagory:
		conditions += "and employee_catagory = '%s' " %(filters.employee_catagory)
	employees = frappe.db.sql("""select * from `tabEmployee` where status = 'Active' %s order by name ASC""" % (conditions), as_dict=True)
	left_employees = frappe.db.sql("""select * from `tabEmployee` where status = 'Left' and relieving_date >= '%s'  %s order by name ASC""" %(filters.from_date,conditions),as_dict=True)
	employees.extend(left_employees)
	return employees

from frappe.utils import  formatdate,get_last_day, get_first_day, add_days
@frappe.whitelist()
def get_to_date(from_date):
	return get_last_day(from_date)
