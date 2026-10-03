import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_quotation_properties():
    make_property_setter("Quotation", "valid_till", "reqd", "0", "Check")

    # Always show Description and UOM in the items table; shrink other columns so all fit in the grid's 10 units
    make_property_setter("Quotation Item", "description", "in_list_view", 1, "Check")
    make_property_setter("Quotation Item", "uom", "in_list_view", 1, "Check")
    for fieldname, columns in {"item_code": 2, "description": 3, "qty": 1, "uom": 1, "rate": 1, "amount": 2}.items():
        make_property_setter("Quotation Item", fieldname, "columns", columns, "Int")
