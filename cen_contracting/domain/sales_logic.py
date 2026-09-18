import frappe

def increment_version_number(doc, method):
    if doc.amended_from:
        previous_version = frappe.db.get_value("Quotation", doc.amended_from, "cen_version_number")
        doc.cen_version_number = (int(previous_version) + 1) if previous_version else 2
    else:
        doc.cen_version_number = 1

