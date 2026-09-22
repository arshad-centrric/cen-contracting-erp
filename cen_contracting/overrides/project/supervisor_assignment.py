import frappe
from frappe.desk.form.assign_to import _add as assign_to
from frappe.desk.form.assign_to import _remove as unassign


def sync_project_supervisor_assignment(doc, method=None):
    supervisor = doc.get("cen_project_supervisor")

    previous = doc.get_doc_before_save()
    previous_supervisor = previous.get("cen_project_supervisor") if previous else None

    if previous_supervisor and previous_supervisor != supervisor:
        unassign(doc.doctype, doc.name, previous_supervisor, ignore_permissions=True)

    if not supervisor:
        return

    # Also covers projects that already had a supervisor before this feature existed,
    # or whose ToDo was closed/cancelled some other way - not just a field change.
    already_assigned = frappe.db.exists(
        "ToDo",
        {
            "reference_type": doc.doctype,
            "reference_name": doc.name,
            "allocated_to": supervisor,
            "status": "Open",
        },
    )
    if already_assigned:
        return

    assign_to(
        {
            "assign_to": [supervisor],
            "doctype": doc.doctype,
            "name": doc.name,
            "description": frappe._("Assigned as Project Supervisor"),
        },
        ignore_permissions=True,
    )
