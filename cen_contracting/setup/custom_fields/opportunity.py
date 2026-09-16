def get_opportunity_fields():
    return {
        "Opportunity": [
            {
                "fieldname": "cen_project_type",
                "label": "Project Type",
                "fieldtype": "Select",
                "options": "Existing\nNew",
                "insert_after": "party_name"
            },
            {
                "fieldname": "cen_party_name_details",
                "label": "Full Name",
                "fieldtype": "Data",
                "read_only": 1,
                "insert_after": "party_name"
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
                "fieldname": "cen_party_organization",
                "label": "Organization",
                "fieldtype": "Data",
                "read_only": 1,
                "insert_after": "cen_party_name_details"
            },
            {
                "fieldname": "cen_project_name",
                "label": "Project Name",
                "fieldtype": "Data",
                "depends_on": "eval:doc.cen_project_type == \"New\"",
                "insert_after": "cen_choose_project"
            }
        ]
    }
