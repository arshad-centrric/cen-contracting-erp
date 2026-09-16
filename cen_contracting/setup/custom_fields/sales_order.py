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
            }
        ]
    }
