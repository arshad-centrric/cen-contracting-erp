def get_sales_order_fields():
    return {
        "Sales Order": [
            {
                "fieldname": "cen_project_type",
                "label": "Project Type",
                "fieldtype": "Select",
                "options": "Existing\nNew",
                "insert_after": "customer_name"
            },
            {
                "fieldname": "cen_choose_project",
                "label": "Choose Project",
                "fieldtype": "Link",
                "options": "Project",
                "depends_on": "eval:doc.cen_project_type == \"Existing\"",
                "insert_after": "cen_project_type"
            },
            {
                "fieldname": "cen_project_name",
                "label": "Project Name",
                "fieldtype": "Data",
                "depends_on": "eval:doc.cen_project_type == \"New\"",
                "insert_after": "cen_choose_project"
            },
            {
                "fieldname": "cen_payment_terms",
                "label": "Payment Term",
                "fieldtype": "Data",
                "insert_after": "delivery_date"
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
