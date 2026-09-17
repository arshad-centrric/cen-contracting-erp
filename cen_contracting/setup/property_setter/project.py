import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_project_properties():
    # Make standard fields mandatory
    make_property_setter("Project", "customer", "reqd", 1, "Check")
    make_property_setter("Project", "expected_start_date", "reqd", 1, "Check")
    
    # Update Status options
    make_property_setter("Project", "status", "options", "Open\nOngoing\nHold\nCompleted\nCancelled", "Text")
