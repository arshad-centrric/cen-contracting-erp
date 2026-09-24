import frappe


def set_dynamic_letter_head(doc, method=None):
	if not doc.meta.has_field("letter_head"):
		return

	# Runs on every insert site-wide, so read the cached single rather than hitting the DB.
	mapped = next(
		(
			row.default_letter_head
			for row in frappe.get_cached_doc("Print Routing Settings").mappings
			if row.document_type == doc.doctype
		),
		None,
	)
	if not mapped:
		return

	# New documents arrive pre-filled with the default Letter Head (the global default, or the
	# Company's default via ERPNext's form), so those don't count as a manual selection.
	if doc.letter_head and doc.letter_head not in get_auto_filled_letter_heads(doc):
		return

	doc.letter_head = mapped


def get_auto_filled_letter_heads(doc):
	letter_heads = {frappe.db.get_default("letter_head")}
	if doc.get("company"):
		letter_heads.add(frappe.get_cached_value("Company", doc.company, "default_letter_head"))
	return letter_heads
