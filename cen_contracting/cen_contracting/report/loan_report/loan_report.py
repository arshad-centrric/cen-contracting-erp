import frappe
from frappe.utils import flt


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
        {"label": "Advance Amount", "fieldname": "advance_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Loan Term (Months)", "fieldname": "cen_loan_term_months", "fieldtype": "Int", "width": 130},
        {"label": "Monthly Deduction", "fieldname": "cen_monthly_deduction", "fieldtype": "Currency", "width": 140},
        {"label": "Loan Start Date", "fieldname": "cen_loan_start_date", "fieldtype": "Date", "width": 120},
        {"label": "Loan End Date", "fieldname": "cen_loan_end_date", "fieldtype": "Date", "width": 120},
        {"label": "Returned Amount", "fieldname": "return_amount", "fieldtype": "Currency", "width": 130},
        {"label": "Balance Remaining", "fieldname": "balance_remaining", "fieldtype": "Currency", "width": 140},
        {"label": "Loan Status", "fieldname": "loan_status", "fieldtype": "Data", "width": 140},
    ]


def get_conditions(filters):
    conditions = ["cen_advance_type = 'Loan Advance'", "company = %(company)s"]
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

    return " AND ".join(conditions), values


def get_loan_status(row):
    if row.docstatus == 2:
        return "Cancelled"
    if row.status in ("Draft", "Unpaid"):
        return "Pending Disbursement"
    if flt(row.return_amount) >= flt(row.advance_amount):
        return "Closed"
    return "Active"


def get_data(filters):
    conditions, values = get_conditions(filters)
    query = f"""
        SELECT
            employee,
            employee_name,
            posting_date,
            advance_amount,
            cen_loan_term_months,
            cen_monthly_deduction,
            cen_loan_start_date,
            cen_loan_end_date,
            return_amount,
            docstatus,
            status
        FROM `tabEmployee Advance`
        WHERE {conditions}
        ORDER BY posting_date DESC
    """
    rows = frappe.db.sql(query, values, as_dict=1)

    loan_status_filter = filters.get("loan_status")
    data = []
    for row in rows:
        row["loan_status"] = get_loan_status(row)
        row["balance_remaining"] = max(flt(row.advance_amount) - flt(row.return_amount), 0)
        if loan_status_filter and row["loan_status"] != loan_status_filter:
            continue
        data.append(row)

    return data
