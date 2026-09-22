import frappe

def sync_project_costing(doc, method=None):
    """
    Absolute recalculation override for Project costing.
    Hooks into Purchase Invoice on_submit and on_cancel to prevent incremental caching drift.
    """
    # Get all unique projects tagged in the item table of this invoice
    projects = set([item.project for item in doc.items if item.project])
    
    for project in projects:
        try:
            # Load the full project doc to access standard calculation methods
            project_doc = frappe.get_doc("Project", project)
            
            # This triggers an absolute SQL query summation of all Purchase Invoice Items
            # and automatically calls calculate_gross_margin() internally.
            project_doc.update_purchase_costing()
            
            # Update the database
            project_doc.db_update()
        except Exception as e:
            frappe.log_error(title=f"Failed to sync project costing for {project}", message=str(e))
