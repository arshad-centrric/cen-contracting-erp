import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_employee_advance_properties():
    # Advance Account is always system-derived from Employee Advance Settings once filled
    make_property_setter("Employee Advance", "advance_account", "read_only_depends_on", "eval:doc.advance_account", "Code")

    # Repay Unclaimed Amount from Salary is always editable: forced to 1 server-side for
    # Salary/Loan Advance, but left to the user for Petty Cash/Expense (manual recovery only,
    # via HRMS's native "Deduction from Salary" button - see overrides/employee_advance/*.py)
