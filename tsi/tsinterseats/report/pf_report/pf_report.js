frappe.query_reports["PF Report"] = {
	"filters": [
		{
			"fieldname": "start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			// "default": [frappe.datetime.add_months(frappe.datetime.get_today())],
			"reqd": 1
		},
		{
			"fieldname": "end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			// "default": [frappe.datetime.add_months(frappe.datetime.get_today())],
			"reqd": 1
		},
	]
};