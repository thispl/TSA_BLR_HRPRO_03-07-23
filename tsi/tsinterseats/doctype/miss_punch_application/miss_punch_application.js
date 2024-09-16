// Copyright (c) 2023, Abdulla P I and contributors
// For license information, please see license.txt

frappe.ui.form.on('Miss Punch Application', {
	date:function(frm) {
		if (frm.doc.__islocal){
			frappe.call({
				'method':'frappe.client.get_value',
				'args':{
					'doctype':'Attendance',
					'filters':{
						'employee':frm.doc.employee,
						'attendance_date':frm.doc.date
					},
					'fieldname':['in_time','out_time','shift','total_working_hours']
				},
				callback(r){
					if(r.message){
						// console.log(r.message)
						frm.set_value('in_punch',r.message.in_time)
						frm.set_value('out_punch',r.message.out_time)
						frm.set_value('shift',r.message.shift)
					}
				}
			})
		}
		// const employee = frm.doc.employee;
		// const missPunchDate = frm.doc.date;
		// if (employee && missPunchDate) {
			// const year = new Date(missPunchDate).getFullYear();
			// const month = new Date(missPunchDate).getMonth() + 1;
			// const lastDay = new Date(year, month, 0).getDate();
			// const startDate = `01-${month.toString().padStart(2, '0')}-${year}`;
			// const endDate = `${lastDay.toString().padStart(2, '0')}-${month.toString().padStart(2, '0')}-${year}`;
			// console.log(startDate)
			// console.log(endDate)
			// frappe.call({
				// method: 'frappe.client.get_value',
				// args: {
				// 	doctype: 'Miss Punch Application',
				// 	filters: {
				// 		employee: employee,
				// 		date: ['>=', startDate],
				// 		date: ['<=', endDate],
				// 		docstatus : 1
				// 	},
				// 	fieldname: ['name']
				// },
				// callback: function(response) {
				// 	console.log(response)
				// 	const existingMissPunches = response.message;

				// 	if (existingMissPunches && existingMissPunches.name ) {
				// 		frappe.msgprint(__("Employee already has a Miss Punch application for this year."));
				// 		frappe.validated = false;
				// 		frm.disable_save();
				// 	} else {
				// 		frappe.validated = true;
				// 		// console.log('hi')
				// 		frm.enable_save();
				// 	}
				// }
		
	// });
		}
		
	// }
});

	