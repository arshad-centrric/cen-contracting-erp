# Copyright (c) 2026, Centrric Innovations Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

# Advance Type -> (child doctype, table fieldname on Employee Advance Settings)
ADVANCE_TYPE_MAP = {
	"Petty Cash/Expense": ("Petty Cash Mapping Item", "petty_cash_mapping"),
	"Salary Advance": ("Salary Advance Mapping Item", "salary_advance_mapping"),
	"Loan Advance": ("Loan Advance Mapping Item", "loan_advance_mapping"),
}


class EmployeeAdvanceSettings(Document):
	def validate(self):
		for _child_doctype, table_fieldname in ADVANCE_TYPE_MAP.values():
			self.validate_duplicate_company(table_fieldname)

	def validate_duplicate_company(self, table_fieldname):
		seen = set()
		for row in self.get(table_fieldname):
			if row.company in seen:
				frappe.throw(
					_("Row {0}: Duplicate mapping for Company {1} in {2}").format(
						row.idx, row.company, self.meta.get_field(table_fieldname).label
					)
				)
			seen.add(row.company)


@frappe.whitelist()
def get_advance_type_mapping(company, advance_type):
	"""Return {salary_component, advance_account} for the given Company and Advance Type, or None."""
	config = ADVANCE_TYPE_MAP.get(advance_type)
	if not config:
		return None

	child_doctype, _table_fieldname = config
	return frappe.db.get_value(
		child_doctype,
		{"parent": "Employee Advance Settings", "company": company},
		["salary_component", "advance_account"],
		as_dict=True,
	)
