// Copyright (c) 2023, Abdulla P I and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly In Out Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default":frappe.datetime.month_start()
			on_change: function () {
				var from_date = frappe.query_report.get_filter_value('from_date')
				frappe.call({
					method: "tsi.tsinterseats.report.monthly_in_out_report.monthly_in_out_report.get_to_date",
					args: {
						from_date: from_date
					},
					callback(r) {
						frappe.query_report.set_filter_value('to_date', r.message);
						frappe.query_report.refresh();
					}
				})
			}
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default":frappe.datetime.month_end()
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
		{
			"fieldname": "employee_catagory",
			"label": __("Employee Catagory"),
			"fieldtype": "Link",
			"options": "Employee Catagory",
			"default":""
		},
		
	]
};
