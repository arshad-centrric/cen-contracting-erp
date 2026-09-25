# Copyright (c) 2026, Centrric Innovations Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PrintRoutingSettings(Document):
	def validate(self):
		seen = set()
		for row in self.mappings:
			if row.document_type in seen:
				frappe.throw(
					_("Row {0}: Duplicate mapping for {1}").format(row.idx, frappe.bold(row.document_type))
				)
			seen.add(row.document_type)

			if not frappe.get_meta(row.document_type).has_field("letter_head"):
				frappe.throw(
					_("Row {0}: {1} has no Letter Head field, so a default Letter Head can't be applied to it").format(
						row.idx, frappe.bold(row.document_type)
					)
				)
