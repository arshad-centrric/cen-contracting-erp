// Copyright (c) 2026, Centrric Innovations Private Limited and contributors
// For license information, please see license.txt

frappe.query_reports["Loan Report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "loan_status",
			"label": __("Loan Status"),
			"fieldtype": "Select",
			"options": "\nPending Disbursement\nActive\nClosed\nCancelled"
		}
	]
};
