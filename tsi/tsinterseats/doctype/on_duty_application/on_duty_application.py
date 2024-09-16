from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime, timedelta

class OnDutyApplication(Document):
	def validate(self):
		if frappe.db.exists("On Duty Application", {'employee': self.employee, 'od_date': self.od_date, 'docstatus':1}):
			frappe.throw(_("On Duty Application Already Found for this Employee and Date"))
	def on_submit(self):
		# Check if the submitted OnDuty application has a shift type, date, and session
		if self.shift and self.od_date and self.session:
			try:
				start_time = datetime.strptime(self.from_time, "%H:%M:%S.%f")
			except ValueError:
				start_time = datetime.strptime(self.from_time, "%H:%M")

			try:
				end_time = datetime.strptime(self.to_time, "%H:%M:%S.%f")
			except ValueError:
				end_time = datetime.strptime(self.to_time, "%H:%M")

			time_difference = end_time - start_time

			# Calculate the time difference in seconds
			total_seconds = time_difference.total_seconds()

			# Calculate hours, minutes, and seconds from total seconds
			hours, remainder = divmod(total_seconds, 3600)
			minutes, seconds = divmod(remainder, 60)

			# Format the total working hours as 'HH:MM:SS'
			formatted_total_hours = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

			# Check if an attendance record already exists for the same date and employee
			attendance = frappe.db.exists("Attendance", {
				"employee": self.employee,
				"attendance_date": self.od_date
			})
			if attendance:
				attendance_doc = frappe.get_doc("Attendance", attendance)
				if self.session == 'Flexible':
					attendance_doc.on_duty_application = self.name
					attendance_doc.session_from_time = self.flexible_time
					attendance_doc.session_to_time = self.flexible_to_time

					try:
						start_time_flex = datetime.strptime(self.flexible_time, "%H:%M:%S")
					except ValueError:
						start_time_flex = datetime.strptime(self.flexible_time, "%H:%M")

					try:
						end_time_flex = datetime.strptime(self.flexible_to_time, "%H:%M:%S")
					except ValueError:
						end_time_flex = datetime.strptime(self.flexible_to_time, "%H:%M")

					time_difference = end_time_flex - start_time_flex

					# Additional processing for flexible session if needed


					# Calculate the time difference in seconds
					total_seconds = time_difference.total_seconds()

					# Calculate hours, minutes, and seconds from total seconds
					hours, remainder = divmod(total_seconds, 3600)
					minutes, seconds = divmod(remainder, 60)

					# Format the total working hours as 'HH:MM:SS'
					formatted_total_hours = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

					attendance_doc.total_working_hours = formatted_total_hours
					attendance_doc.save(ignore_permissions=True)
				else:
					if self.session == "Full day":
						attendance_doc.status = "Present"
						attendance_doc.shift_status = "P(OD)"
					if self.session == "First Half":
						if attendance_doc.status == "Half Day":
							attendance_doc.status = "Present"
							attendance_doc.shift_status = "OD/P"
						else:
							attendance_doc.status = "Half Day"
							attendance_doc.shift_status = "HD(OD)"
					if self.session == "Second Half":
						if attendance_doc.status == "Half Day":
							attendance_doc.status = "Present"
							attendance_doc.shift_status = "P/OD"
						else:
							attendance_doc.status = "Half Day"
							attendance_doc.shift_status = "HD(OD)"
					attendance_doc.on_duty_application = self.name
					attendance_doc.session_from_time = self.from_time
					attendance_doc.session_to_time = self.to_time
					attendance_doc.shift = self.shift
					attendance_doc.total_working_hours = formatted_total_hours
					attendance_doc.save(ignore_permissions=True)
			else:
				attendance_doc = frappe.new_doc("Attendance")
				attendance_doc.employee = self.employee
				attendance_doc.attendance_date = self.od_date
				if self.session == 'Flexible':
					attendance_doc.on_duty_application = self.name
					attendance_doc.session_from_time = self.flexible_time
					attendance_doc.session_to_time = self.flexible_to_time
					# attendance_doc.shift = self.shift or ''
					start_time = datetime.strptime(self.flexible_time, "%H:%M:%S")
					end_time = datetime.strptime(self.flexible_to_time, "%H:%M:%S")
					time_difference = end_time - start_time

					# Calculate the time difference in seconds
					total_seconds = time_difference.total_seconds()

					# Calculate hours, minutes, and seconds from total seconds
					hours, remainder = divmod(total_seconds, 3600)
					minutes, seconds = divmod(remainder, 60)

					# Format the total working hours as 'HH:MM:SS'
					formatted_total_hours = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

					attendance_doc.total_working_hours = formatted_total_hours
					attendance_doc.save(ignore_permissions=True)
				else:
					if self.session == "Full day":
						attendance_doc.status = "Present"
						attendance_doc.shift_status = "P(OD)"
					if self.session == "First Half":
						attendance_doc.status = "Half Day"
						attendance_doc.shift_status = "HD(OD)"
					if self.session == "Second Half":
						attendance_doc.status = "Half Day"
						attendance_doc.shift_status = "HD(OD)"
					attendance_doc.on_duty_application = self.name
					attendance_doc.session_from_time = self.from_time
					attendance_doc.session_to_time = self.to_time
					attendance_doc.shift = self.shift
					attendance_doc.total_working_hours = formatted_total_hours
					attendance_doc.save(ignore_permissions=True)
				# attendance_doc.insert()
		elif self.session !="Flexible":
			frappe.msgprint(_("Please provide shift type, date, and session for the OnDuty application."))

	# def on_cancel(self):
	# # # 	clear_field = frappe.db.sql("""UPDATE `tabAttendance` SET on_duty_application = '', session_from_time = '', session_to_time = '', shift = '', total_working_hours = '' WHERE on_duty_application = self.name""")
	# # # 	status_field = frappe.db.sql("""UPDATE `tabAttendance` SET status = 'Absent' WHERE on_duty_application = self.name AND status = 'Present""")

	# 	att = frappe.get_doc('Attendance',{'on_duty_application': self.name})

	# 	frappe.db.set_value('Attendance', att.name, 'on_duty_application','')
	# 	frappe.db.set_value('Attendance', att.name, 'session_from_time','00:00:00')
	# 	frappe.db.set_value('Attendance', att.name, 'session_to_time','00:00:00')
	# 	frappe.db.set_value('Attendance', att.name, 'shift','') 
	# 	frappe.db.set_value('Attendance', att.name, 'total_working_hours','00:00:00')
		
	# 	if self.session == "Full day":
	# 		frappe.db.set_value('Attendance', att.name,'status','Absent')
	# 		frappe.db.set_value('Attendance', att.name,'shift_status','AB')

	# 	if self.session == "First Half" or "Second Half":
	# 		frappe.db.set_value('Attendance', att.name,'status','Half Day')
	# 		frappe.db.set_value('Attendance', att.name,'shift_status','HD')
		

@frappe.whitelist()
def get_shift_time(name):
    # Fetch the "Start Time" and "End Time" values based on the selected "Shift Type"
    shift_doc = frappe.get_doc("Shift Type", name)
    if shift_doc:
        # Calculate hours and minutes from timedelta objects
        start_hours, start_minutes = divmod(shift_doc.start_time.seconds // 60, 60)
        end_hours, end_minutes = divmod(shift_doc.end_time.seconds // 60, 60)

        # Convert hours and minutes to strings and format the time data
        start_time = '{:02}:{:02}'.format(start_hours, start_minutes)
        end_time = '{:02}:{:02}'.format(end_hours, end_minutes)

        return {
            "start_time": start_time,
            "end_time": end_time
        }
    else:
        return {}
   