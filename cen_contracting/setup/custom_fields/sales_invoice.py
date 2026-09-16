def get_sales_invoice_fields():
    return {
        "Sales Invoice": [
            {
                "fieldname": "cen_payment_terms",
                "label": "Payment Term",
                "fieldtype": "Data",
                "insert_after": "due_date"
            }
        ]
    }
