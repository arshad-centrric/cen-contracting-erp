import json

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
        # "report": 1 required for the Salary Advance Report / Loan Report (cen_contracting) -
        # frappe.has_permission(ref_doctype, "report") is checked separately from "read".
        # Write+create so the Supervisor can raise their own Salary Advance/Loan request.
        {"parent": "Employee Advance", "read": 1, "write": 1, "create": 1, "report": 1},
        # Read-only: needed to pass the Company filter value on the same two reports above.
        {"parent": "Company", "read": 1},
        # Attendance - full access. Supervisors mark attendance for every employee on
        # their site, not just their own team - not scoped/restricted.
        {"parent": "Attendance", "read": 1, "write": 1, "create": 1},
        # Bulk attendance marking page - read only, this is what the workspace shortcut
        # below points to.
        {"parent": "Employee Attendance Tool", "read": 1},
        # Raise requests only - not approve/process (no write/submit).
        {"parent": "Material Request", "read": 1, "create": 1},
        # View available project-related stock.
        {"parent": "Item", "read": 1},
        {"parent": "Warehouse", "read": 1},
        # Link-field dependencies on Project/Task, currently blocking those forms.
        {"parent": "Project Template", "read": 1},
        {"parent": "Department", "read": 1},
        {"parent": "Cost Center", "read": 1},
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

    # 3. Create/update Workspace
    workspace_name = "Supervisor Desk"
    sections = [
        ("Project", [
            {"label": "Project", "type": "DocType", "link_to": "Project", "icon": "folder-plus"},
            {"label": "Task", "type": "DocType", "link_to": "Task", "icon": "check-square"},
            {"label": "Timesheet", "type": "DocType", "link_to": "Timesheet", "icon": "clock"},
        ]),
        ("Attendance & Advance", [
            {"label": "Employee Attendance Tool", "type": "DocType", "link_to": "Employee Attendance Tool", "icon": "clock"},
            {"label": "Employee Advance", "type": "DocType", "link_to": "Employee Advance", "icon": "credit-card"},
            {"label": "Expense Claim", "type": "DocType", "link_to": "Expense Claim", "icon": "credit-card"},
        ]),
        ("Inventory", [
            {"label": "Material Request", "type": "DocType", "link_to": "Material Request", "icon": "package"},
            {"label": "Item", "type": "DocType", "link_to": "Item", "icon": "package"},
            {"label": "Warehouse", "type": "DocType", "link_to": "Warehouse", "icon": "package"},
        ]),
        ("Reports", [
            {"label": "Salary Advance Report", "type": "Report", "link_to": "Salary Advance Report", "icon": "table"},
            {"label": "Loan Report", "type": "Report", "link_to": "Loan Report", "icon": "table"},
        ]),
    ]

    all_shortcuts = []
    content_blocks = []
    for section_key, section_shortcuts in sections:
        block_id_base = "wsSuper" + section_key.replace(" ", "").replace("&", "")
        content_blocks.append(
            {"id": block_id_base + "Head", "type": "header", "data": {"text": section_key, "level": 2}}
        )
        for i, s in enumerate(section_shortcuts):
            content_blocks.append(
                {"id": f"{block_id_base}{i}", "type": "shortcut", "data": {"shortcut_name": s["label"], "col": 3}}
            )
        all_shortcuts += section_shortcuts

    if frappe.db.exists("Workspace", workspace_name):
        workspace = frappe.get_doc("Workspace", workspace_name)
    else:
        workspace = frappe.new_doc("Workspace")
        workspace.name = workspace_name
        workspace.label = workspace_name
        workspace.title = workspace_name
        workspace.icon = "clipboard"
        workspace.is_standard = 0
        workspace.public = 1
        workspace.roles = []
        workspace.append("roles", {"role": role_name})

    workspace.module = None
    workspace.content = json.dumps(content_blocks)
    workspace.shortcuts = []
    for s in all_shortcuts:
        workspace.append("shortcuts", s)
    workspace.save(ignore_permissions=True)

    # 4. Pin the workspace to the Home/Desktop screen (creates its Workspace Sidebar +
    # Desktop Icon) so a user with only this role sees it immediately after login.
    # Same call the desk UI itself makes to do this; idempotent (no-ops if both already exist).
    add_workspace_to_desktop(workspace_name)
