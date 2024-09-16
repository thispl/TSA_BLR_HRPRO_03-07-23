// Copyright (c) 2023, Abdulla P I and contributors
// For license information, please see license.txt

frappe.ui.form.on('DH Approval', {
	
	employee(frm){
		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "Attendance",
				filters: {
					"employee": frm.doc.employee,
					"attendance_date":frm.doc.dh_date
				},
				fieldname: ["name","out_time",'in_time','shift','total_working_hours','overtime_hours','extra_hours']
				},
				callback: function(r){
					if(r.message){
						frm.set_value("attendance",r.message.name);
						frm.set_value("shift",r.message.shift);
						frm.set_value("working_time_start",r.message.in_time);
						frm.set_value("working_time_finish",r.message.out_time);
						frm.set_value("working_time_finish",r.message.out_time);
						frm.set_value("total_working_hours",r.message.total_working_hours);
						frm.set_value("overtime_hours",r.message.overtime_hours);
						frm.set_value("extra_hours",r.message.extra_hours);
					}
				}
			});
			
			if(frm.doc.attendance){
				frappe.call({
					method: 'tsi.custom.in_time',
					args: {
						attendance_name: frm.doc.attendance
					},
					callback: function(r) {
						if (r.message) {
							frm.set_value('working_time_start', r.message);
						}
					}
				}); 
				frappe.call({
				   method: 'tsi.custom.out_time',
				   args: {
					   attendance_name: frm.doc.attendance
				   },
				   callback: function(r) {
					   if (r.message) {
						   frm.set_value('working_time_finish', r.message);
						}
					}
			   }); 
			}


			var totalWorkingHours = frm.doc.total_working_hours;
			console.log(type(totalWorkingHours))
			var hours = parseInt(totalWorkingHours.split(":")[0]);
			var minutes = parseInt(totalWorkingHours.split(":")[1]);
			var seconds = parseInt(totalWorkingHours.split(":")[2]);
			var totalWorkingTime = hours + minutes / 60 + seconds / 3600;
			console.log(type(totalWorkingTime))

			// Fixed rate per hour
			var ratePerHour = 62.5;

			// Calculate dhAmount based on totalWorkingTime
			var dhAmount = totalWorkingTime * ratePerHour;

			frm.set_value('dh_allowance', dhAmount);

		}


});
