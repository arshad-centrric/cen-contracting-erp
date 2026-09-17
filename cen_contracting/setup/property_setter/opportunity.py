import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_opportunity_properties():
    # Make contact fields mandatory for Opportunity
    make_property_setter("Opportunity", "contact_person", "reqd", 1, "Check")
    make_property_setter("Opportunity", "contact_mobile", "reqd", 1, "Check")

