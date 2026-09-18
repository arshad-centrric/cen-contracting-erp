def get_expense_claim_fields():
    return {
        "Expense Claim": [
            {
                "fieldname": "cen_vat_account",
                "label": "VAT Account",
                "fieldtype": "Link",
                "options": "Account",
                "insert_after": "payable_account"
            }
        ],
        "Expense Claim Detail": [
            {
                "fieldname": "cen_vendor_name",
                "label": "Vendor Name",
                "fieldtype": "Data",
                "insert_after": "description"
            },
            {
                "fieldname": "cen_vendor_vat_number",
                "label": "Vendor VAT Number",
                "fieldtype": "Data",
                "insert_after": "cen_vendor_name"
            },
            {
                "fieldname": "cen_vehicle_details",
                "label": "Vehicle Details",
                "fieldtype": "Data",
                "insert_after": "cen_vendor_vat_number"
            },
            {
                "fieldname": "cen_base_amount",
                "label": "Base Amount (Excl. VAT)",
                "fieldtype": "Currency",
                "options": "currency",
                "insert_after": "amount",
                "in_list_view": 1
            },
            {
                "fieldname": "cen_vat_amount",
                "label": "VAT Amount",
                "fieldtype": "Currency",
                "options": "currency",
                "insert_after": "cen_base_amount",
                "in_list_view": 1
            }
        ]
    }
