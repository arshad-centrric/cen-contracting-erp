import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_quotation_properties():
    make_property_setter({
        'doctype_or_field': 'DocField',
        'doc_type': 'Quotation',
        'field_name': 'valid_till',
        'property': 'reqd',
        'value': '0',
        'property_type': 'Check'
    }, is_system_generated=False)

