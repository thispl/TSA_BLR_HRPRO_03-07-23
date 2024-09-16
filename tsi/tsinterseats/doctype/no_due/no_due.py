# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form


class NoDue(Document):
	def on_Submitted(self):
		doc = frappe.get_doc('No Due Child',{'parent':self.employee_name,'hod_name':self.hod_id},['hod_name','due_status','description'])
		doc.due_status = self.due_status
		doc.description = self.description
		# doc.department = self.department
		doc.save(ignore_permissions=True)
		frappe.db.set_value('Employee',self.employee,'no_due_clearance',1)
		
