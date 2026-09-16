def get_customer_fields():
    return {
        "Customer": [
            {
                "fieldname": "cen_customer_category",
                "label": "Customer Category",
                "fieldtype": "Select",
                "options": "VIP\nCORE\nSTANDARD",
                "default": "STANDARD",
                "allow_in_quick_entry": 1,
                "insert_after": "customer_group"
            }
        ]
    }

