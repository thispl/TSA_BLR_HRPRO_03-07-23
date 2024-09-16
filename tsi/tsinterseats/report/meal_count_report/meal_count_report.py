# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt
import frappe
from frappe import _
import datetime
from datetime import date, datetime, timedelta


def execute(filters=None):
    columns, data = [] ,[]
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    column = [_('Date') + ":Date:140",]

    items = frappe.db.sql(""" select name,serial_no from `tabFood Menu` order by serial_no asc""",as_dict =1)
    
    for i in items:
        column.extend([_(i.name) + ":Data:140",])

    return column

def get_data(filters):
    if filters.checkbox==1:
        data = []
        total=0
        frm = datetime.strptime(filters.from_date, '%Y-%m-%d').date()
        to = datetime.strptime(filters.to_date, '%Y-%m-%d').date()
        
        delta = to - frm
            
        items = frappe.db.sql(""" select name,serial_no from `tabFood Menu` order by serial_no asc""",as_dict =1)
        
        for i in range(delta.days + 1):
            day = frm + timedelta(days=i)
            d = frappe.db.sql(""" select  sum(`tabFood Items`.status) as count,`tabFood Items`.item from `tabVisitor Pass` 
                left join `tabFood Items` on `tabVisitor Pass`.name = `tabFood Items`.parent
                where  `tabVisitor Pass`.posting_date = '%s'  group by  `tabFood Items`.item """ %(day), as_dict =1)
            
            row = [day]
            status = []
            for s in items:
                count1 = 0
                for j in d:
                    if s.name == j.item:
                        count1 = j.count
                status.append(count1)
            
            row.extend(status)
        
            data.append(row)
        return data 
    else:
        data = []
        total=0
        frm = datetime.strptime(filters.from_date, '%Y-%m-%d').date()
        to = datetime.strptime(filters.to_date, '%Y-%m-%d').date()
        
        delta = to - frm
            
        items = frappe.db.sql(""" select name,serial_no from `tabFood Menu` order by serial_no asc""",as_dict =1)
        
        for i in range(delta.days + 1):
            day = frm + timedelta(days=i)
            c = frappe.db.sql(""" select  sum(`tabFood Items`.status) as count,`tabFood Items`.item from `tabCanteen Coupons` 
                left join `tabFood Items` on `tabCanteen Coupons`.name = `tabFood Items`.parent
                where  `tabCanteen Coupons`.date = '%s'  group by  `tabFood Items`.item """ %(day), as_dict =1)
            
            d = frappe.db.sql(""" select  sum(`tabFood Items`.status) as count,`tabFood Items`.item from `tabVisitor Pass` 
                left join `tabFood Items` on `tabVisitor Pass`.name = `tabFood Items`.parent
                where  `tabVisitor Pass`.posting_date = '%s'  group by  `tabFood Items`.item """ %(day), as_dict =1)
            
            row = [day]
            status = []
            for s in items:
                count = 0
                count1=0
                count2=0
                for i in c:
                    if s.name == i.item:
                        count1 = i.count
                for j in d:
                    if s.name == j.item:
                        count2 = j.count
                total=count1+count2
                frappe.errprint(total)
                status.append(total)
            
            row.extend(status)
        
            data.append(row)
        return data 

def get_dates_between(start_date, end_date):
  
  dates = []
  current_date = start_date
  while current_date <= end_date:
   dates.append(current_date)
  current_date += datetime.timedelta(days=1)

  return dates