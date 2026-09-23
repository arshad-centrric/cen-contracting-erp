import frappe
from frappe import _
from frappe.utils import add_months, get_first_day, getdate

from hrms.hr.doctype.employee_advance.employee_advance import create_return_through_additional_salary

from cen_contracting.cen_contracting.doctype.employee_advance_settings.employee_advance_settings import (
    get_advance_type_mapping,
)

# Employee Advance.status is set to "Paid" via set_status(update=True) -> self.db_set("status", ...),
# called from set_total_advance_paid() (a Payment Entry / Advance Payment Ledger Entry side effect).
# db_set() never runs validate/on_update, only run_method("on_change") - so this must be an
# on_change hook, not validate/on_update. db_set() is also called separately for paid_amount,
# return_amount, status and pending_amount within the same update, so on_change fires multiple
# times per payment - the idempotency guard below is required, not optional.

ELIGIBLE_ADVANCE_TYPES = ("Salary Advance", "Loan Advance")


def on_change(doc, method=None):
    if doc.status != "Paid":
        return
    if doc.cen_advance_type not in ELIGIBLE_ADVANCE_TYPES:
        return
    if not doc.repay_unclaimed_amount_from_salary:
        return
    if frappe.db.exists(
        "Additional Salary", {"ref_doctype": "Employee Advance", "ref_docname": doc.name}
    ):
        return

    try:
        _create_recovery_additional_salary(doc)
    except Exception:
        frappe.log_error(
            title=_("Auto-recovery Additional Salary failed for Employee Advance {0}").format(doc.name),
            message=frappe.get_traceback(),
            reference_doctype="Employee Advance",
            reference_name=doc.name,
        )
        try:
            doc.add_comment(
                "Comment",
                _(
                    "Automatic Additional Salary creation for salary recovery failed. "
                    "Please check the Error Log and create the deduction manually if required."
                ),
            )
        except Exception:
            pass


def _create_recovery_additional_salary(doc):
    mapping = get_advance_type_mapping(doc.company, doc.cen_advance_type)
    if not mapping or not mapping.get("salary_component"):
        frappe.throw(
            _(
                "No Salary Component mapping found for Company {0} and Advance Type {1}. "
                "Please configure it in Employee Advance Settings."
            ).format(doc.company, doc.cen_advance_type)
        )

    additional_salary = create_return_through_additional_salary(doc)
    additional_salary.salary_component = mapping.get("salary_component")
    additional_salary.type = "Deduction"

    if doc.cen_advance_type == "Salary Advance":
        additional_salary.is_recurring = 0
        additional_salary.payroll_date = get_first_day(add_months(getdate(), 1))
    else:  # Loan Advance
        additional_salary.is_recurring = 1
        additional_salary.from_date = doc.cen_loan_start_date
        additional_salary.to_date = doc.cen_loan_end_date
        # create_return_through_additional_salary() defaults amount to the full paid_amount
        # (a lump sum) - the recurring deduction must be the monthly installment instead.
        additional_salary.amount = doc.cen_monthly_deduction

    additional_salary.insert(ignore_permissions=True)
    additional_salary.submit()
