import frappe

def execute(filters=None):
    columns = get_columns()
    raw_data = get_data(filters)
    data = format_data_for_wireframe(raw_data)
    
    return columns, data

def get_columns():
    return [
        {"fieldname": "customer", "label": "Customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"fieldname": "quotation", "label": "Quotation", "fieldtype": "Link", "options": "Quotation", "width": 130},
        {"fieldname": "project", "label": "Project", "fieldtype": "Link", "options": "Project", "width": 130},
        {"fieldname": "sales_order", "label": "Sales Order", "fieldtype": "Link", "options": "Sales Order", "width": 130},
        {"fieldname": "invoice", "label": "Invoice", "fieldtype": "Link", "options": "Sales Invoice", "width": 130},
        {"fieldname": "amount", "label": "Amount", "fieldtype": "Currency", "width": 120},
        {"fieldname": "received_amount", "label": "Received", "fieldtype": "Currency", "width": 120},
        {"fieldname": "balance", "label": "Balance", "fieldtype": "Currency", "width": 120},
        {"fieldname": "so_amount", "label": "SO Total Amount", "fieldtype": "Currency", "width": 130},
        {"fieldname": "so_received", "label": "SO Total Received", "fieldtype": "Currency", "width": 130},
        {"fieldname": "so_balance", "label": "SO Total Balance", "fieldtype": "Currency", "width": 130}
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    # Query linking Invoice -> Order -> Quotation
    query = f"""
        SELECT 
            si.customer,
            so_item.prevdoc_docname AS quotation,
            si.project,
            si_item.sales_order,
            si.name AS invoice,
            si.grand_total AS amount,
            (si.grand_total - si.outstanding_amount) AS received_amount,
            si.outstanding_amount AS balance,
            so.base_grand_total AS so_amount
        FROM 
            `tabSales Invoice` si
        LEFT JOIN 
            `tabSales Invoice Item` si_item ON si_item.parent = si.name
        LEFT JOIN 
            `tabSales Order Item` so_item ON so_item.parent = si_item.sales_order
        LEFT JOIN
            `tabSales Order` so ON so.name = si_item.sales_order
        WHERE 
            si.docstatus = 1 {conditions}
        GROUP BY 
            si.name, si.customer, si.project, si_item.sales_order, so_item.prevdoc_docname, so.base_grand_total
        ORDER BY 
            si.customer, si_item.sales_order, si.posting_date ASC
    """
    
    return frappe.db.sql(query, filters, as_dict=1)

def get_conditions(filters):
    filters = filters or {}
    conditions = ""
    if filters.get("customer"):
        conditions += " AND si.customer = %(customer)s"
    if filters.get("quotation"):
        conditions += " AND so_item.prevdoc_docname = %(quotation)s"
    if filters.get("sales_order"):
        conditions += " AND si_item.sales_order = %(sales_order)s"
    if filters.get("invoice"):
        conditions += " AND si.name = %(invoice)s"
    return conditions

def format_data_for_wireframe(raw_data):
    # Pass 1: Calculate sums per Sales Order
    so_totals = {}
    for row in raw_data:
        if row.sales_order:
            if row.sales_order not in so_totals:
                so_totals[row.sales_order] = {"received": 0, "balance": 0}
            so_totals[row.sales_order]["received"] += (row.received_amount or 0)
            so_totals[row.sales_order]["balance"] += (row.balance or 0)

    # Pass 2: Format for wireframe
    formatted_data = []
    last_sales_order = None
    
    for row in raw_data:
        # Always set the SO totals for every row, since blanking them out 
        # causes Frappe to render '0.00' for Currency fields.
        if row.sales_order in so_totals:
            row.so_received = so_totals[row.sales_order]["received"]
            row.so_balance = so_totals[row.sales_order]["balance"]
        else:
            row.so_received = 0
            row.so_balance = 0

        if row.sales_order and row.sales_order == last_sales_order:
            # If it's the same order, blank out the text/link fields to avoid visual clutter
            row.customer = ""
            row.quotation = ""
            row.project = ""
            row.sales_order = ""
            # We do NOT blank out so_amount, so_received, so_balance here anymore.
        else:
            # New order, update the tracker
            last_sales_order = row.sales_order
            
        formatted_data.append(row)
        
    return formatted_data