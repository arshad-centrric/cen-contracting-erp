import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_quotation_properties():
    make_property_setter("Quotation", "valid_till", "reqd", "0", "Check")

