def get_quotation_fields():
    return {
        "Quotation": [
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
                "insert_after": "valid_till"
            },
            {
                "fieldname": "cen_lpo_number",
                "label": "Customer Reference / LPO No.",
                "fieldtype": "Data",
                "insert_after": "transaction_date"
            },
            {
                "fieldname": "cen_version_number",
                "label": "Version Number",
                "fieldtype": "Int",
                "default": "1",
                "read_only": 1,
                "insert_after": "naming_series"
            },
            {
                "fieldname": "cen_revision_reason",
                "label": "Reason for Revision",
                "fieldtype": "Small Text",
                "depends_on": "eval:doc.amended_from",
                "insert_after": "amended_from"
            },
            {
                "fieldname": "cen_customer_category",
                "label": "Customer Category",
                "fieldtype": "Data",
                "insert_after": "customer_name",
                "read_only": 1,
                "fetch_from": "party_name.cen_customer_category",
                "depends_on": "eval:doc.quotation_to == 'Customer'"
            },
            {
                "fieldname": "cen_work_description",
                "label": "Description of Work",
                "fieldtype": "Text",
                "insert_after": "has_unit_price_items"
            }
        ]
    }
