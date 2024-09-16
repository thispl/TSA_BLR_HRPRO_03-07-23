# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VisitorPass(Document):
	pass

@frappe.whitelist()
def get_condition():
    condn = frappe.db.sql("""select * from `tabFood Menu` order by `order` """,as_dict=True)
    return condn