# Copyright (c) 2023, Abdulla P I and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

class ProcessCoupons(Document):
    pass

@frappe.whitelist()
def fetch_active_employees(from_date, to_date):
    start_date = datetime.strptime(from_date, '%Y-%m-%d')
    end_date = datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1)  # Include the end date

    while start_date < end_date:
        process_date = start_date.strftime('%Y-%m-%d')
        employees = frappe.get_all(
            'Employee',
            filters={'status': 'Active'},
            fields=['name', 'employee_name', 'designation', 'department']
        )
        
        for emp in employees:
            fm = frappe.get_all('Food Menu', ["*"])  # Get all Food Menu items

            # Check if Canteen Coupons exist for the employee on the specific date
            if not frappe.db.exists('Canteen Coupons', {'employee': emp.name, 'date': process_date}):
                # Create a new Canteen Coupons document for the employee on the specified date
                cc = frappe.new_doc('Canteen Coupons')
                cc.employee = emp.name
                cc.employee_name = emp.employee_name
                cc.department = emp.department
                cc.designation = emp.designation
                cc.date = process_date
                items_to_add = []  # Initialize an empty list for items

                # Add all Food Menu items to the items_to_add list
                for f in fm:
                    items_to_add.append({
                        'item': f.name,
                        'status': 0  # Set status to 0 initially
                    })

                # Set the child table field 'items' with the items_to_add list
                cc.set('items', items_to_add)
                cc.save(ignore_permissions=True)

            else:
                # Get existing Canteen Coupons document for the employee on the specified date
                cc = frappe.get_doc('Canteen Coupons', {'employee': emp.name, 'date': process_date})

                # If the document has no items, add Food Menu items to the 'items' child table
                if not cc.get('items'):
                    items_to_add = []  # Initialize an empty list for items

                    # Add all Food Menu items to the items_to_add list
                    for f in fm:
                        items_to_add.append({
                            'item': f.name,
                            'status': 0  # Set status to 0 initially
                        })

                    # Extend the 'items' child table with the items_to_add list
                    cc.extend('items', items_to_add)
                    cc.save(ignore_permissions=True)

            # Check attendance for the employee on the specified date
            if frappe.db.exists('Attendance', {'employee': emp.name, 'attendance_date': process_date,
                                   'status': ['in', ('Present', 'Half Day')]}):
                att = frappe.get_value("Attendance",
                                    {'employee': emp.name, 'attendance_date': process_date,
                                        'status': ['in', ('Present', 'Half Day')]}, ["in_time", "out_time","on_duty_application","session_from_time","session_to_time"])

                # Check if attendance has valid in_time and out_time
                if att and att[0] and att[1] and not att[2]:
                    in_time = att[0].strftime('%H:%M:%S')
                    out_time = att[1].strftime('%H:%M:%S')
                    time_in = datetime.strptime(in_time, '%H:%M:%S').time()
                    time_out = datetime.strptime(out_time, '%H:%M:%S').time()

                    # Check if Food Menu items fall within the attendance time range
                    for item in cc.get('items'):
                        food_menu = frappe.get_doc('Food Menu', item.get('item'))
                        from_time = str(food_menu.from_time)
                        st = datetime.strptime(from_time, '%H:%M:%S').time()

                        if time_in <= st <= time_out:
                            item.status = 1  # Update status field for existing items in 'Canteen Coupons' items child table
                
                # Check if there's a specific session attendance with valid from_time and to_time
                if att and att[3] and att[4] and att[2]:
                    in_time = str(att[3])
                    out_time = str(att[4])
                    time_in = datetime.strptime(in_time, '%H:%M:%S').time()
                    time_out = datetime.strptime(out_time, '%H:%M:%S').time()

                    # Check if Food Menu items fall within the session time range
                    for item in cc.get('items'):
                        food_menu = frappe.get_doc('Food Menu', item.get('item'))
                        from_time = str(food_menu.from_time)
                        st = datetime.strptime(from_time, '%H:%M:%S').time()

                        if time_in <= st <= time_out:
                            item.status = 1  # Update status field for existing items in 'Canteen Coupons' items child table

            # Save the 'Canteen Coupons' document after processing
            cc.save(ignore_permissions=True)

        start_date += timedelta(days=1)  # Move to the next day in the date range

    return True  # Return True after processing all dates and employees
