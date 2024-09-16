// Copyright (c) 2023, Abdulla P I and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Wise Meal Count Report"] = {
	"filters": [
		{
			fieldname: 'from_date',
			label: __('From Date'),
			fieldtype: 'Date',
			// default: frappe.datetime.add_months(frappe.datetime.nowdate(), -1),
			reqd: 1,
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
			fieldname: 'to_date',
			label: __('To Date'),
			fieldtype: 'Date',
			// default: frappe.datetime.nowdate(),
			reqd: 1,
		},
		{
			fieldname: 'employee',
			label: __('Employee Name'),
			fieldtype: 'Link',
			options: 'Employee',
		}
	]
};
