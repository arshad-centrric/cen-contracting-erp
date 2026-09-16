import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields as make_custom_fields

from .opportunity import get_opportunity_fields
from .quotation import get_quotation_fields
from .sales_order import get_sales_order_fields
from .sales_invoice import get_sales_invoice_fields
from .customer import get_customer_fields

def create_custom_fields():
    custom_fields = {}
    
    custom_fields.update(get_opportunity_fields())
    custom_fields.update(get_quotation_fields())
    custom_fields.update(get_sales_order_fields())
    custom_fields.update(get_sales_invoice_fields())
    custom_fields.update(get_customer_fields())
    
    make_custom_fields(custom_fields)
