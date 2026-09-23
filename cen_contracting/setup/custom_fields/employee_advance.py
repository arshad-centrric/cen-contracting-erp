def get_employee_advance_fields():
    return {
        "Employee Advance": [
            {
                "fieldname": "cen_advance_type",
                "label": "Advance Type",
                "fieldtype": "Select",
                "options": "Petty Cash/Expense\nSalary Advance\nLoan Advance",
                "reqd": 1,
                "in_list_view": 1,
                "in_standard_filter": 1,
                "insert_after": "section_break_8"
            },
            {
                "fieldname": "cen_loan_details_section",
                "label": "Loan Details",
                "fieldtype": "Section Break",
                "insert_after": "repay_unclaimed_amount_from_salary",
                "depends_on": "eval:doc.cen_advance_type==\"Loan Advance\""
            },
            {
                "fieldname": "cen_loan_term_months",
                "label": "Loan Term (Months)",
                "fieldtype": "Int",
                "insert_after": "cen_loan_details_section",
                "mandatory_depends_on": "eval:doc.cen_advance_type==\"Loan Advance\""
            },
            {
                "fieldname": "cen_monthly_deduction",
                "label": "Monthly Deduction",
                "fieldtype": "Currency",
                "options": "currency",
                "insert_after": "cen_loan_term_months"
            },
            {
                "fieldname": "cen_loan_details_column_break",
                "fieldtype": "Column Break",
                "insert_after": "cen_monthly_deduction"
            },
            {
                "fieldname": "cen_loan_start_date",
                "label": "Loan Start Date",
                "fieldtype": "Date",
                "insert_after": "cen_loan_details_column_break",
                "mandatory_depends_on": "eval:doc.cen_advance_type==\"Loan Advance\""
            },
            {
                "fieldname": "cen_loan_end_date",
                "label": "Loan End Date",
                "fieldtype": "Date",
                "insert_after": "cen_loan_start_date",
                "read_only": 1
            }
        ]
    }
