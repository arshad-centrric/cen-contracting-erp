import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def set_sales_order_properties():
    # Delivery Date is optional (ERPNext's server-side check is relaxed in overrides/sales_order/optional_delivery_date.py)
    make_property_setter("Sales Order", "delivery_date", "reqd", 0, "Check")
    make_property_setter("Sales Order Item", "delivery_date", "reqd", 0, "Check")

    # Always show Description and UOM in the items table; shrink other columns so all fit in the grid's 10 units
    make_property_setter("Sales Order Item", "description", "in_list_view", 1, "Check")
    make_property_setter("Sales Order Item", "uom", "in_list_view", 1, "Check")
    for fieldname, columns in {"item_code": 2, "delivery_date": 1, "description": 2, "qty": 1, "uom": 1, "rate": 1, "amount": 2}.items():
        make_property_setter("Sales Order Item", fieldname, "columns", columns, "Int")
