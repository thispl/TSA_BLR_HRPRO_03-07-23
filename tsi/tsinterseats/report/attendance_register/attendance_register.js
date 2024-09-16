// Copyright (c) 2023, Abdulla P I and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance Register"] = {
	"filters": [
		{
			"fieldname": "start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"reqd": 1,
			on_change: function () {
				var from_date = frappe.query_report.get_filter_value('start_date')
				frappe.call({
					method: "tsi.tsinterseats.report.monthly_in_out_report.monthly_in_out_report.get_to_date",
					args: {
						from_date: from_date
					},
					callback(r) {
						console.log(r.message)
						frappe.query_report.set_filter_value('end_date', r.message);
						frappe.query_report.refresh();
					}
				})
			}
		},
		{
			"fieldname": "end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"fieldname": "employee_catagory",
			"label": __("Employee Catagory"),
			"fieldtype": "Link",
			"options": "Employee Catagory",
			"default":""
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
	],
};
