# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import math
import frappe
import json
import requests
# import pandas as pd
import openpyxl
from six import BytesIO
from frappe.utils import gzip_decompress,cstr

@frappe.whitelist()
def get_data_pf():
	data = []
	name = frappe.db.get_value('Prepared Report', {'report_name': 'PF Report', 'status': 'Completed'}, 'name')
	attached_file_name = frappe.db.get_value(
		"File",
		{"attached_to_doctype": 'Prepared Report',
			"attached_to_name": name},
		"name",
	)
	attached_file = frappe.get_doc("File", attached_file_name)
	compressed_content = attached_file.get_content()
	uncompressed_content = gzip_decompress(compressed_content)
	dos = json.loads(uncompressed_content.decode("utf-8"))
	result = ""
	for do in dos['result']:
		result +=  str(do['employee']) + " #~#" + str(do['employee_name']) + " #~#" + str(do['department']) + " #~#" + str(do['bank_account_number']) + " #~#" + str(round(do['gross_pay'])) + " #~#" + str(round(do['pf'])) + "\n" 
	frappe.response["result"] = result
	frappe.response["type"] = "txt"
	frappe.response["doctype"] = "PF Text File"
	return data