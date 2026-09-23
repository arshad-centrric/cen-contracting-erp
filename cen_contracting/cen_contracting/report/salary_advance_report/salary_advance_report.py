import frappe


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 140},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 160},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
        {"label": "Purpose", "fieldname": "purpose", "fieldtype": "Data", "width": 220},
        {"label": "Advance Amount", "fieldname": "advance_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Paid Amount", "fieldname": "paid_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Returned Amount", "fieldname": "return_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Balance", "fieldname": "balance", "fieldtype": "Currency", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 130},
    ]


def get_conditions(filters):
    conditions = ["cen_advance_type = 'Salary Advance'", "company = %(company)s"]
    values = {"company": filters.get("company")}

    if filters.get("employee"):
        conditions.append("employee = %(employee)s")
        values["employee"] = filters.get("employee")

    if filters.get("from_date"):
        conditions.append("posting_date >= %(from_date)s")
        values["from_date"] = filters.get("from_date")

    if filters.get("to_date"):
        conditions.append("posting_date <= %(to_date)s")
        values["to_date"] = filters.get("to_date")

    if filters.get("status"):
        conditions.append("status = %(status)s")
        values["status"] = filters.get("status")
    else:
        conditions.append("docstatus != 2")

    return " AND ".join(conditions), values


def get_data(filters):
    conditions, values = get_conditions(filters)
    query = f"""
        SELECT
            employee,
            employee_name,
            posting_date,
            purpose,
            advance_amount,
            paid_amount,
            return_amount,
            GREATEST(paid_amount - return_amount, 0) as balance,
            status
        FROM `tabEmployee Advance`
        WHERE {conditions}
        ORDER BY posting_date DESC
    """
    return frappe.db.sql(query, values, as_dict=1)
