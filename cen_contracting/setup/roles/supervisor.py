import frappe
from frappe.desk.doctype.desktop_icon.desktop_icon import add_workspace_to_desktop

def setup_supervisor_role_and_workspace():
    role_name = "Project Supervisor"

    # 1. Create Role
    if not frappe.db.exists("Role", role_name):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name,
            "desk_access": 1
        }).insert(ignore_permissions=True)

    # 2. Assign Permissions
    perms = [
        {"parent": "Project", "read": 1, "write": 1, "create": 1},
        {"parent": "Task", "read": 1, "write": 1, "create": 1},
        {"parent": "Timesheet", "read": 1, "write": 1, "create": 1, "submit": 1},
        {"parent": "Expense Claim", "read": 1, "write": 1, "create": 1, "submit": 1},
        {"parent": "Employee", "read": 1},
        {"parent": "Customer", "read": 1},
    ]

    for p in perms:
        existing = frappe.db.exists("Custom DocPerm", {"parent": p["parent"], "role": role_name})
        docperm = frappe.get_doc("Custom DocPerm", existing) if existing else frappe.new_doc("Custom DocPerm")
        docperm.parent = p["parent"]
        docperm.role = role_name
        docperm.read = p.get("read", 0)
        docperm.write = p.get("write", 0)
        docperm.create = p.get("create", 0)
        docperm.submit = p.get("submit", 0)
        docperm.report = p.get("report", 0)
        docperm.save(ignore_permissions=True) if existing else docperm.insert(ignore_permissions=True)

    # Update perms (Clear cache so new permissions take effect immediately)
    for p in perms:
        frappe.clear_cache(doctype=p["parent"])

    # 3. Create Workspace
    workspace_name = "Supervisor Desk"
    if not frappe.db.exists("Workspace", workspace_name):
        frappe.get_doc({
            "doctype": "Workspace",
            "name": workspace_name,
            "label": workspace_name,
            "title": workspace_name,
            "icon": "clipboard",
            "is_standard": 0,
            "public": 1,
            "roles": [{"role": role_name}],
            "content": '[{"id": "VymR211wYc", "type": "header", "data": {"text": "Supervisor Actions", "level": 2}}, {"id": "N7xG9Z3qB1", "type": "shortcut", "data": {"shortcut_name": "Create New Project", "col": 3}}, {"id": "L8vH4M2kA9", "type": "shortcut", "data": {"shortcut_name": "Assign Task", "col": 3}}, {"id": "P5jC7X9wD4", "type": "shortcut", "data": {"shortcut_name": "Submit Timesheet", "col": 3}}, {"id": "R2tN6F8qV3", "type": "shortcut", "data": {"shortcut_name": "Claim Petty Cash", "col": 3}}]',
            "shortcuts": [
                {"type": "DocType", "link_to": "Project", "label": "Create New Project", "icon": "folder-plus"},
                {"type": "DocType", "link_to": "Task", "label": "Assign Task", "icon": "check-square"},
                {"type": "DocType", "link_to": "Timesheet", "label": "Submit Timesheet", "icon": "clock"},
                {"type": "DocType", "link_to": "Expense Claim", "label": "Claim Petty Cash", "icon": "credit-card"}
            ]
        }).insert(ignore_permissions=True)

    # 4. Pin the workspace to the Home/Desktop screen (creates its Workspace Sidebar +
    # Desktop Icon) so a user with only this role sees it immediately after login.
    # Same call the desk UI itself makes to do this; idempotent (no-ops if both already exist).
    add_workspace_to_desktop(workspace_name)
