# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form


class NoDueForm(Document):
	def on_submit(self):
		if self.workflow_state == "Submitted":
			for i in self.no_due_clearance:
				frappe.errprint(i.due_status)
				if i.due_status == "Yes":
					frappe.throw("All Due status should be closed to submit the document")

	def on_update(self):
		if self.workflow_state == 'Pending for HOD':
			no_due_alert = frappe.get_doc("Employee",{"name":self.employee},["*"])
			no_due_alert.no_due_alert = 1
			no_due_alert.save(ignore_permissions=True)
			for i in self.no_due_clearance:
				dept = frappe.get_value('Employee',{'user_id':i.hod_name},['department'])
				emp_name = frappe.get_value('Employee',{'user_id':i.hod_name},['name'])
				emp = frappe.get_value('Employee',{'user_id':i.hod_name},['employee_name'])
				if not frappe.db.exists("No Due",{"employee":self.employee,"hod_id":i.hod_name}):
					doc = frappe.new_doc('No Due')
					doc.employee = self.employee
					doc.hod_id = i.hod_name
					doc.hod_name = emp_name 
					doc.hod = emp
					doc.hod_department = dept
					doc.save(ignore_permissions=True)
					no_due_name = frappe.get_value("No Due",{"hod_id":i.hod_name},["name"])

		if self.workflow_state == 'Submitted':
			no_due_clearance = frappe.get_doc("Employee",{"name":self.employee})
			no_due_clearance.no_due_clearance = 1
			no_due_clearance.save(ignore_permissions=True)
			