import frappe
from frappe import _
from datetime import datetime, timedelta

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        _('Date') + ":Date:140",
        _('Visitor Name') + ":Link/Employee:140",
        _('Requester Name') + ":Data:140",
        _('Company Name') + ":Data:140",
        _('Purpose Of Visit') + ":Data:140",
    ]
    
    items = frappe.db.sql("""SELECT name FROM `tabFood Menu` ORDER BY serial_no ASC""", as_dict=True)
    for item in items:
        columns.append(_(item.name) + ":Int:80")
    
    columns.append(_('Total') + ":Int:80")
    return columns

def get_data(filters):
    count=0
    item=0
    data = []
    from_date = datetime.strptime(filters.get('from_date'), '%Y-%m-%d').date()
    to_date = datetime.strptime(filters.get('to_date'), '%Y-%m-%d').date()
    name1 = filters.get('name1')
    current_date = from_date

    while current_date <= to_date:
        query = """
            SELECT
                `tabVisitor Pass`.visiting_date,
                `tabVisitor Pass`.name1,
                `tabVisitor Pass`.employee,
                `tabVisitor Pass`.company_name AS company,
                `tabVisitor Pass`.purpose_of_visit,
                `tabFood Items`.item,
                SUM(`tabFood Items`.status) AS count
            FROM
                `tabVisitor Pass`
            LEFT JOIN
                `tabFood Items` ON `tabVisitor Pass`.name = `tabFood Items`.parent
            WHERE
                `tabVisitor Pass`.visiting_date = %s
        """
        params = [current_date]

        if name1:
            query += " AND `tabVisitor Pass`.name1 = %s"
            params.append(name1)

        query += """
            GROUP BY
                `tabVisitor Pass`.visiting_date,
                `tabVisitor Pass`.name1,
                `tabVisitor Pass`.employee,
                `tabVisitor Pass`.company_name,
                `tabVisitor Pass`.purpose_of_visit,
                `tabFood Items`.item
        """

        c = frappe.db.sql(query, tuple(params), as_dict=True)
        employee_data = {}
        
        for row in c:
            employee_id = row['name1']
            employee_name = row['employee']
            company = row['company']
            visit = row['purpose_of_visit']
            item = row['item'] or 0
            count = row['count'] or 0

            if employee_id not in employee_data:
                employee_data[employee_id] = {
                    'employee': employee_name,
                    'company': company,
                    'purpose_of_visit': visit,
                    'items': {item: count},
                    'total': 0
                }
            else:
                if item not in employee_data[employee_id]['items']:
                    employee_data[employee_id]['items'][item] = count or 0
                else:
                    employee_data[employee_id]['items'][item] += count or 0

            employee_data[employee_id]['total'] += count or 0

        items = frappe.db.sql("""SELECT name FROM `tabFood Menu` ORDER BY serial_no ASC""", as_dict=True)

        for employee_id, emp_data in employee_data.items():
            row = [current_date, employee_id, emp_data['employee'], emp_data['company'], emp_data['purpose_of_visit']]
            for item in items:
                row.append(emp_data['items'].get(item.name, 0))
            row.append(emp_data['total'])
            data.append(row)
        current_date += timedelta(days=1)

    return data