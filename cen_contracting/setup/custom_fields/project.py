def get_project_fields():
    return {
        "Project": [
            {
                "fieldname": "cen_project_details_section",
                "label": "Project Details",
                "fieldtype": "Section Break",
                "insert_after": "department"
            },
            {
                "fieldname": "cen_customer_category",
                "label": "Customer Category",
                "fieldtype": "Data",
                "fetch_from": "customer.cen_customer_category",
                "insert_after": "cen_project_details_section"
            },
            {
                "fieldname": "cen_site_location",
                "label": "Site / Location",
                "fieldtype": "Data",
                "insert_after": "cen_customer_category"
            },
            {
                "fieldname": "cen_project_supervisor",
                "label": "Project Supervisor",
                "fieldtype": "Link",
                "options": "User",
                "insert_after": "cen_site_location",
                "reqd": 1
            }
        ]
    }

