# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime
from datetime import timedelta

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [_('Date') + ":Date:140", _('Employee') + ":Link/Employee:140", _('Employee Name') + ":Data:140"]
	items = frappe.db.sql("""SELECT name FROM `tabFood Menu` ORDER BY serial_no ASC""", as_dict=True)
	for item in items:
		columns.append(_(item.name) + ":Int:80")
	columns.append(_('Total') + ":Int:80")  
	return columns

def get_data(filters):
	data = []
	from_date = datetime.strptime(filters.get('from_date'), '%Y-%m-%d').date()
	to_date = datetime.strptime(filters.get('to_date'), '%Y-%m-%d').date()
	employee = filters.get('employee')
	current_date = from_date
	while current_date <= to_date:
		query = """
			SELECT
				`tabCanteen Coupons`.date,
				`tabCanteen Coupons`.employee,
				`tabCanteen Coupons`.employee_name,
				`tabFood Items`.item,
				SUM(`tabFood Items`.status) AS count
			FROM
				`tabCanteen Coupons`
			LEFT JOIN
				`tabFood Items` ON `tabCanteen Coupons`.name = `tabFood Items`.parent
			WHERE
				`tabCanteen Coupons`.date = %s
		"""
		params = [current_date]

		if employee:
			query += " AND `tabCanteen Coupons`.employee = %s"
			params.append(employee)

		query += """
			GROUP BY
				`tabCanteen Coupons`.date,
				`tabCanteen Coupons`.employee,
				`tabCanteen Coupons`.employee_name,
				`tabFood Items`.item
		"""

		c = frappe.db.sql(query, tuple(params), as_dict=True)
		employee_data = {}
		for row in c:
			employee_id = row['employee']
			employee_name = row['employee_name']
			item = row['item']
			count = row['count']

			if employee_id not in employee_data:
				employee_data[employee_id] = {
					'employee_name': employee_name,
					'items': {item: count},
					'total': 0
				}
			else:
				if item not in employee_data[employee_id]['items']:
					employee_data[employee_id]['items'][item] = count
				else:
					employee_data[employee_id]['items'][item] += count

			employee_data[employee_id]['total'] += count

		items = frappe.db.sql("""SELECT name FROM `tabFood Menu` ORDER BY serial_no ASC""", as_dict=True)

		for employee_id, emp_data in employee_data.items():
			row = [current_date, employee_id, emp_data['employee_name']]
			for item in items:
				row.append(emp_data['items'].get(item.name, 0))
			row.append(emp_data['total'])
			data.append(row)
		current_date += timedelta(days=1)

	return data