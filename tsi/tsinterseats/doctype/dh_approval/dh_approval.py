# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class DHApproval(Document):
    
    def validate(self):
        if self.docstatus == 1:  # Check if the document is submitted
            # Fetch Holiday List
            holiday_list_name = "Holiday - TSI"
            hl = frappe.get_doc("Holiday List", holiday_list_name)
            
            if not hl:
                frappe.throw(_("Holiday List '{0}' not found").format(holiday_list_name))

           
