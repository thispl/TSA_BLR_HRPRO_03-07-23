import frappe

@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
	if frappe.db.exists('Employee',{'biometric_pin':args['employee'],'status':'Active'}):
		if not frappe.db.exists('Employee Checkin',{'biometric_pin':args['employee'],'time':args['time']}):
			ec = frappe.new_doc('Employee Checkin')
			ec.employee = frappe.get_value('Employee',{'biometric_pin':args['employee'],'status':'Active'})
			ec.time = args['time']
			ec.device_id = args['device_id']
			ec.biometric_pin = args['employee']
			if args['device_id'] == 'IN':
				ec.log_type = 'IN'
			else:
				ec.log_type = 'OUT'
			ec.save(ignore_permissions=True)
			frappe.db.commit()
			return "Checkin Marked"
		else:
			return "Checkin Marked"
	else:
		if not frappe.db.exists('Unregistered Employee Checkin',{'biometric_pin':args['employee'],'biometric_time':args['time']}):
			ec = frappe.new_doc('Unregistered Employee Checkin')
			ec.biometric_pin = args['employee'].upper()
			ec.biometric_time = args['time']
			ec.locationdevice_id = args['device_id']
			if args['device_id'] == 'IN':
				ec.log_type = 'IN'
			else: 
				ec.log_type = 'OUT'
			ec.save(ignore_permissions=True)
			frappe.db.commit()
			return "Checkin Marked" 
		else:
			return "Checkin Marked"