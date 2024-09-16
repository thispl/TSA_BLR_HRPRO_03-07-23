# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt

import fractions
from frappe.model.document import Document
import frappe
import datetime
from datetime import datetime, timedelta

from datetime import date, datetime,time
from frappe.utils import add_days,today
import datetime as dt
# import pandas as pd
from frappe.utils import (
    add_days,
    add_to_date,
    cint,
    flt,
    get_datetime,
    get_link_to_form,
    get_time,
    getdate,
    time_diff,
    time_diff_in_hours,
    time_diff_in_seconds,
)

class OvertimeRequest(Document):
    pass

# @frappe.whitelist()
# def get_att_bio_checkin(emp,ot_date):
#     datalist = []
#     data = {}
#     if frappe.db.exists('Attendance',{'employee':emp,'attendance_date':ot_date}):
#         attendance = frappe.get_all('Attendance',{'employee':emp,'attendance_date':ot_date},['*'])
#         for att in attendance:
#             if att.in_time and att.out_time:
#                 from_time = att.in_time
#                 to_time = att.out_time
#                 start_time = frappe.get_value('Shift Type',{'name':att.shift},['start_time'])
#                 end_time = frappe.get_value('Shift Type',{'name':att.shift},['end_time'])
#                 if att.shift == "N":
#                     shift_duration = (end_time - start_time) + timedelta(days=1)
#                 elif att.shift in ["I", "II", "G"]:
#                     shift_duration = (end_time - start_time)
#                 shift = att.shift
#                 total_wh = att.total_working_hours 
#                 if total_wh > shift_duration:
#                     ot = total_wh - shift_duration
#                     frappe.errprint(ot)
#                     frappe.errprint("Hi")
#                     try:
#                         time_diff = datetime.strptime(str(ot), '%H:%M:%S')
#                         frappe.errprint(time_diff)
#                     except:
#                         time_diff = datetime.strptime(str("23:59:59"), '%H:%M:%S')
#                         frappe.errprint(time_diff)
#                     ot_hours = time(0,0,0)
#                     if time_diff.hour == 0 :
#                         if time_diff.minute >= 30 and time_diff.minute <= 59:
#                             ot_hours = time(time_diff.hour,30,0)
#                     elif time_diff.hour >= 1 :
#                         if time_diff.minute <= 29:
#                             ot_hours = time(time_diff.hour,0,0)
#                         elif time_diff.minute >= 30 and time_diff.minute <= 59:
#                             ot_hours = time(time_diff.hour,30,0)
#                     data.update({
#                         'bio_in':from_time,
#                         'bio_out':to_time,
#                         'total_wh':total_wh,
#                         'shift':shift,
#                         'ot_hours':ot_hours
#                     })
#                     datalist.append(data.copy())
#                 else:
#                     frappe.msgprint("No OT Hours")
                    
#                     data.update({
#                         'bio_in':from_time,
#                         'bio_out':to_time,
#                         'total_wh':total_wh,
#                         'shift':shift,
#                         'ot_hours':''
#                     })
#                     datalist.append(data.copy())
#             else:
#                 data.update({
#                     'bio_in':'',
#                     'bio_out':'',
#                     'total_wh':'',
#                     'shift':'',
#                     'ot_hours':''
#                 })
#                 datalist.append(data.copy())
#                 frappe.msgprint('Overtime Cannot be applied without Biometric In time and Out time')
#     else:
#         data.update({
#             'bio_in':'',
#             'bio_out':'',
#             'total_wh':'',
#             'shift':'',
#             'ot_hours':''
#         })
#         datalist.append(data.copy())
#         frappe.msgprint('Overtime Cannot be applied without Attendance')
#     return datalist    

