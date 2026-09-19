def get_sales_invoice_fields():
    return {
        "Sales Invoice": [
            {
                "fieldname": "cen_payment_terms",
                "label": "Payment Term",
                "fieldtype": "Data",
                "insert_after": "due_date"
            },
            {
                "fieldname": "cen_lpo_number",
                "label": "Customer Reference / LPO No.",
                "fieldtype": "Data",
                "insert_after": "po_date",
                "no_copy": 0,
                "in_list_view": 0,
                "in_standard_filter": 0
            }
        ]
    }
