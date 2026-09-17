import frappe
frappe.init(site="classy-dubai-site.local")
frappe.connect()
ps = frappe.get_all("Property Setter", filters={"doc_type": "Project", "property": "insert_after"}, fields=["field_name", "value"])
print(ps)
