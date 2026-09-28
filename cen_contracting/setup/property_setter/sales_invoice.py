import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_sales_invoice_properties():
    # Always show Description and UOM in the items table; shrink other columns so all fit in the grid's 10 units
    # (Warehouse keeps its default 2 units and only shows when Update Stock is ticked)
    make_property_setter("Sales Invoice Item", "description", "in_list_view", 1, "Check")
    make_property_setter("Sales Invoice Item", "uom", "in_list_view", 1, "Check")
    for fieldname, columns in {"item_code": 2, "description": 2, "qty": 1, "uom": 1, "rate": 1, "amount": 1}.items():
        make_property_setter("Sales Invoice Item", fieldname, "columns", columns, "Int")
