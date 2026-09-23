import frappe
from frappe import _
from frappe.utils import add_months, flt, fmt_money, get_first_day, getdate

from cen_contracting.cen_contracting.doctype.employee_advance_settings.employee_advance_settings import (
    get_advance_type_mapping,
)


def validate(doc, method=None):
    if not doc.cen_advance_type:
        return

    mapping = get_advance_type_mapping(doc.company, doc.cen_advance_type)
    if not mapping:
        frappe.throw(
            _(
                "No Advance Account mapping found for Company {0} and Advance Type {1}. "
                "Please configure it in Employee Advance Settings."
            ).format(frappe.bold(doc.company), frappe.bold(doc.cen_advance_type))
        )

    doc.advance_account = mapping.get("advance_account")

    # Salary/Loan Advance recovery is always automatic - force it on. Petty Cash/Expense is
    # left to the user (client script defaults it unchecked on type change); recovery for that
    # type is manual-only regardless, see overrides/employee_advance/auto_recovery.py.
    if doc.cen_advance_type != "Petty Cash/Expense":
        doc.repay_unclaimed_amount_from_salary = 1

    if doc.cen_advance_type == "Loan Advance":
        set_loan_details(doc)


def set_loan_details(doc):
    # mandatory_depends_on is client-side only; Frappe's own mandatory-field
    # check never evaluates it server-side, so it must be enforced here too.
    if not doc.cen_loan_term_months:
        frappe.throw(_("Loan Term (Months) is mandatory when Advance Type is Loan Advance"))

    if not doc.cen_loan_start_date:
        base_date = doc.posting_date or getdate()
        doc.cen_loan_start_date = get_first_day(add_months(base_date, 1))

    if not doc.cen_monthly_deduction and doc.advance_amount:
        doc.cen_monthly_deduction = flt(doc.advance_amount) / doc.cen_loan_term_months

    doc.cen_loan_end_date = add_months(doc.cen_loan_start_date, doc.cen_loan_term_months)

    validate_loan_reconciliation(doc)


def validate_loan_reconciliation(doc):
    # HRMS's own validate_employee_advance_return() only checks the face-value amount
    # of each Additional Salary row once - it never multiplies by term/occurrences - so
    # nothing native catches term x monthly_deduction silently not matching advance_amount.
    expected_total = flt(doc.cen_loan_term_months) * flt(doc.cen_monthly_deduction)
    # tolerance covers up to 1 currency unit of rounding per month (the last instalment
    # often doesn't divide evenly)
    tolerance = flt(doc.cen_loan_term_months)

    if abs(expected_total - flt(doc.advance_amount)) > tolerance:
        frappe.throw(
            _(
                "Loan Term (Months) x Monthly Deduction ({0} x {1} = {2}) does not reconcile "
                "with Advance Amount ({3}). Please correct Monthly Deduction or Advance Amount."
            ).format(
                doc.cen_loan_term_months,
                fmt_money(doc.cen_monthly_deduction, currency=doc.currency),
                fmt_money(expected_total, currency=doc.currency),
                fmt_money(doc.advance_amount, currency=doc.currency),
            )
        )
