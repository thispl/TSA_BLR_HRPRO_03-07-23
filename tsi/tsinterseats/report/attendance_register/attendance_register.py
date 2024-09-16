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
from datetime import date, timedelta, datetime,time


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns += [
		_("Employee ID") + ":Data/:150",
		_("Employee Name") + ":Data/:200",
		_("Department") + ":Data/:150",
	]
	dates = get_dates(filters)
	for date in dates:
		date = datetime.strptime(date,'%Y-%m-%d')
		day = datetime.date(date).strftime('%d')
		month = datetime.date(date).strftime('%b')
		columns.append(_(day) + ":Data/:70")
	columns.append(_("Total Days") + ":Data/:100")
	columns.append(_("Present Days") + ":Data/:100")
	columns.append(_('BH') +':Data/:100')
	columns.append(_("DH") + ":Data/:100")
	columns.append(_("PH")+ ':Data/:100')
	columns.append(_("FH")+ ':Data/:100')
	columns.append(_("WH")+ ':Data/:100')
	columns.append(_("CL")+ ':Data/:100')
	columns.append(_("EL")+ ':Data/:100')
	columns.append(_("ESI")+ ':Data/:100')
	columns.append(_("SA")+ ':Data/:100')
	columns.append(_("Loss Of Pay")+ ':Data/:100')
	columns.append(_("Total Paid Days")+ ':Data/:100')
	columns.append(_("Remarks")+ ':Data/:100')
	return columns

def get_data(filters):
	data = []
	row = []
	employees = get_employees(filters)
	tdcnt =0 
	tpds = 0
	twh=0
	tbh=0
	tdh=0
	tph=0
	tfh=0
	tcl=0
	tel=0
	tesi=0
	tlop=0
	ttpd=0
	tsat=0
	for e in employees:
		row=[]
		row += [e.name,e.employee_name,e.department]
		dates=get_dates(filters)
		cnt = 0
		pd=0
		wh=0
		bh=0
		dh=0
		ph=0
		fh=0
		cl=0
		el=0
		esi=0
		sa=0
		lop=0
		tpd=0

		for date in dates:
			if frappe.db.exists("Attendance",{'attendance_date':date,'employee':e.name,'docstatus':('!=','2')}):
				att = frappe.db.get_value("Attendance",{'attendance_date':date,'employee':e.name},['shift_status'])
				if att:
					row.append(att)
					if att =="P":
						pd += 1
						# cell.font = Font(bold=True,size=14)
					elif att == "P/N":
						pd +=1
						sa +=1
					elif att == "P/AB":
						pd +=0.5
					elif att == "DH/P":
						pd +=1
					elif att == "DH/PN":
						pd +=1
					elif att == "DH/PP":
						pd +=0.5
					elif att == "CL":
						cl +=1
					elif att == "PP/CL":
						cl +=0.5
						pd +=0.5
					elif att == "EL":
						el +=1
					elif att == "P/EL":
						el +=0.5
						pd +=0.5
					elif att == "ESI":
						esi +=1
					elif att == "LOP":
						lop +=1

				else:
					row.append('-')
			else:
				hh = check_holiday(date,e.name)
				row.append(hh)
				if hh == "WH":
					wh+=1
				elif hh == "BH":
					bh +=1
				elif hh == "DH":
					dh +=1
				elif hh == "PH":
					ph +=1
				elif hh == "FH":
					fh +=1
			cnt += 1
		row.append(cnt)
		row.append(pd)
		row.append(bh)
		row.append(dh)
		row.append(ph)
		row.append(fh)
		row.append(wh)
		row.append(cl)
		row.append(el)
		row.append(esi)
		tsa = sa*60
		row.append(tsa)
		row.append(lop)
		tpd=pd+bh+dh+ph+fh+wh+cl+el
		row.append(tpd)
		row.append("")
		data.append(row)
		tdcnt +=cnt
		tpds +=pd
		tbh +=bh
		tdh +=dh
		tph +=ph
		tfh +=fh
		twh +=wh
		tcl +=cl
		tel +=el
		tesi +=esi
		tsat +=tsa
		tlop +=lop
		ttpd +=tpd

	row1 = ['','','']
	dates = get_dates(filters)
	for date in dates:
		row1.extend([''])

	row1.append(tdcnt)
	row1.append(tpds)
	row1.append(tbh)
	row1.append(tdh)
	row1.append(tph)
	row1.append(tfh)
	row1.append(twh)
	row1.append(tcl)
	row1.append(tel)
	row1.append(tesi)
	row1.append(tsat)
	row1.append(tlop)
	row1.append(ttpd)
	row1.append([''])
	data.append(row1)
	return data

def get_dates(filters):
	no_of_days = date_diff(add_days(filters['end_date'], 1), filters['start_date'])
	dates = [add_days(filters['start_date'], i) for i in range(0, no_of_days)]
	return dates

def check_holiday(date,e):
	holiday_list = frappe.db.get_value('Employee',{'name':e},'holiday_list')
	holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off, `tabHoliday`.others from `tabHoliday List` 
	left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
	doj= frappe.db.get_value("Employee",{'name':e},"date_of_joining")
	status = ''
	if holiday :
		if doj < holiday[0].holiday_date:
			if holiday[0].weekly_off == 1:
				status = "WH"     
			else:
				if holiday[0].others == "DH":
					status = "DH"
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
	frappe.errprint(filters)
	left_employees = []
	if filters.employee:
		conditions += "and employee = '%s' " % (filters.employee)
	if filters.department:
		conditions += "and department = '%s' "%(filters.department)
	if filters.employee_catagory:
		conditions += "and employee_catagory = '%s' " %(filters.employee_catagory)
	employees = frappe.db.sql("""select * from `tabEmployee` where status = 'Active' %s order by name ASC""" % (conditions), as_dict=True)
	left_employees = frappe.db.sql("""select * from `tabEmployee` where status = 'Left' and relieving_date >= '%s'  %s order by name ASC""" %(filters.from_date,conditions),as_dict=True)
	# employees.extend(left_employees)
	return employees