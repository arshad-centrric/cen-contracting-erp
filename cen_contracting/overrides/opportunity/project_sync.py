import frappe

def sync_projects_on_validate(doc, method=None):
    # Ensure custom cen_choose_project and standard project fields are always in sync
    custom_proj = doc.get("cen_choose_project")
    std_proj = doc.get("project")
    
    if custom_proj and not std_proj:
        doc.project = custom_proj
    elif std_proj and not custom_proj:
        doc.cen_choose_project = std_proj
    elif custom_proj and std_proj and custom_proj != std_proj:
        # If they somehow differ, assume custom is correct since it's the UI element
        doc.project = custom_proj

