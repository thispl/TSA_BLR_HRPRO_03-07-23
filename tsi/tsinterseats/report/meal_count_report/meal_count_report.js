// Copyright (c) 2023, Abdulla P I and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Meal Count Report"] = {
	filters: [
	  {
		fieldname: 'from_date',
		label: __('From Date'),
		fieldtype: 'Date',
		default: frappe.datetime.now_date().split('-')[0] + '-' + frappe.datetime.now_date().split('-')[1] + '-01', // Set to the first day of the current month
		reqd: 1,
	  },
	  {
		fieldname: 'to_date',
		label: __('To Date'),
		fieldtype: 'Date',
		default: frappe.datetime.now_date().split('-')[0] + '-' + frappe.datetime.now_date().split('-')[1] + '-' + new Date(frappe.datetime.now_date().split('-')[0], frappe.datetime.now_date().split('-')[1], 0).getDate(), // Set to the last day of the current month
		reqd: 1,
	  },
	  {
		fieldname: 'checkbox',
		label: __('Visitor Count'),
		fieldtype: 'Check',
		default: 0  
	  }
	//   {
	// 	fieldname: 'items',
	// 	label: __('Items'),
	// 	fieldtype: 'Link',
	// 	options: 'Food Menu',
	//   },
	],
};