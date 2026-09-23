import json

import frappe
from frappe.desk.doctype.desktop_icon.desktop_icon import add_workspace_to_desktop


def setup_admin_role():
    role_name = "Classy Admin"

    # 1. Create Role
    if not frappe.db.exists("Role", role_name):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name,
            "desk_access": 1
        }).insert(ignore_permissions=True)

    # 2. Document Permissions - full control (read/write/create/delete, plus
    # submit/cancel/amend on submittable doctypes) across every module this role
    # is meant to oversee. "report": 1 everywhere full access is granted, since the
    # role's stated purpose includes org-wide monitoring, not just transacting.
    FULL_NON_SUBMITTABLE = {"read": 1, "write": 1, "create": 1, "delete": 1, "report": 1}
    FULL_SUBMITTABLE = {**FULL_NON_SUBMITTABLE, "submit": 1, "cancel": 1, "amend": 1}
    # Minimum "can manage" bar for HR/payroll setup doctypes - read+write+create+report,
    # deliberately NOT submit/cancel/amend/delete unless explicitly requested.
    HR_MANAGE = {"read": 1, "write": 1, "create": 1, "report": 1}

    perms = [
        # CRM & Sales - full access, including override of the Accountant's Quotation
        # workflow (submit/cancel/amend here is what lets this role approve/reject/cancel
        # a Quotation the Accountant already submitted - see note in the summary about
        # there being no formal multi-state Workflow record for Quotation to "patch").
        {"parent": "Customer", **FULL_NON_SUBMITTABLE},
        {"parent": "Contact", **FULL_NON_SUBMITTABLE},
        {"parent": "Opportunity", **FULL_NON_SUBMITTABLE},
        {"parent": "Quotation", **FULL_SUBMITTABLE},
        {"parent": "Sales Order", **FULL_SUBMITTABLE},
        # Project Management - full access. Project has no Quotation/Sales Order
        # dependency in this app's validation (cen_contracting.overrides.opportunity
        # .project_sync only syncs fields when one exists; it never requires one), so
        # "create directly" already works as soon as `create` is granted here.
        {"parent": "Project", **FULL_NON_SUBMITTABLE},
        {"parent": "Task", **FULL_NON_SUBMITTABLE},
        {"parent": "Timesheet", **FULL_SUBMITTABLE},
        # Accounting & Expenses - full access and override, including the Petty Cash
        # (Expense Claim) approval override the Accountant normally handles.
        {"parent": "Account", **FULL_NON_SUBMITTABLE},
        {"parent": "Sales Invoice", **FULL_SUBMITTABLE},
        {"parent": "Payment Entry", **FULL_SUBMITTABLE},
        {"parent": "Purchase Invoice", **FULL_SUBMITTABLE},
        {"parent": "Journal Entry", **FULL_SUBMITTABLE},
        {"parent": "Expense Claim", **FULL_SUBMITTABLE},
        # Inventory - master data and stock control.
        {"parent": "Item", **FULL_NON_SUBMITTABLE},
        {"parent": "UOM", **FULL_NON_SUBMITTABLE},
        {"parent": "Warehouse", **FULL_NON_SUBMITTABLE},
        # Warehouse Rack (classy_coat_addons) - the standalone doctype backing the
        # Warehouse rack/location custom fields; Item Rack Detail is a child table of
        # Item, so it already inherits Item's permissions above with no separate entry.
        {"parent": "Warehouse Rack", **FULL_NON_SUBMITTABLE},
        {"parent": "Material Request", **FULL_SUBMITTABLE},
        {"parent": "Stock Entry", **FULL_SUBMITTABLE},
        # Stock Ledger Entry is a system-generated ledger (written internally by the
        # stock reposting engine on submit of Stock Entry/Sales Invoice/etc.), the same
        # way GL Entry is for accounting - read/report only, deliberately NOT full CRUD,
        # matching the precedent set for GL Entry on the Classy Accountant role.
        {"parent": "Stock Ledger Entry", "read": 1, "report": 1},
        # GL Entry - view-only, needed for Accounting oversight and so the General Ledger
        # report shortcut on Admin Desk actually works (frappe.has_permission(ref_doctype,
        # "report") is checked independently of the report's own role list).
        {"parent": "GL Entry", "read": 1, "report": 1},
        # Human Resources - configuration & monitoring.
        {"parent": "Employee", **FULL_NON_SUBMITTABLE},
        {"parent": "Department", **FULL_NON_SUBMITTABLE},
        {"parent": "Designation", **FULL_NON_SUBMITTABLE},
        {"parent": "Attendance", **FULL_SUBMITTABLE},
        {"parent": "Leave Application", **FULL_SUBMITTABLE},
        {"parent": "Overtime Slip", **FULL_SUBMITTABLE},
        {"parent": "Salary Slip", **FULL_SUBMITTABLE},
        # Payroll/HR setup doctypes - "at least read+write+create", per explicit request,
        # upgraded from the read+report-only dependent-doctype default below (or added
        # fresh where there was no grant at all before).
        {"parent": "Salary Component", **HR_MANAGE},
        {"parent": "Salary Structure", **HR_MANAGE},
        {"parent": "Salary Structure Assignment", **HR_MANAGE},
        {"parent": "Payroll Entry", **HR_MANAGE},
        {"parent": "Additional Salary", **HR_MANAGE},
        {"parent": "Employee Advance", **HR_MANAGE},
        {"parent": "Employee Attendance Tool", **HR_MANAGE},
        {"parent": "Employee Checkin", **HR_MANAGE},
        {"parent": "Shift Type", **HR_MANAGE},
        {"parent": "Overtime Type", **HR_MANAGE},
        {"parent": "Payroll Settings", **HR_MANAGE},
        # Employee Advance Settings (cen_contracting) - the Loan/Advance Settings singleton.
        {"parent": "Employee Advance Settings", **HR_MANAGE},
        # User - "to manage employee access". NOTE: this includes delete=1 on User as
        # explicitly requested; deleting a User is effectively irreversible (breaks
        # every record that user owns/is linked from) and is normally a System Manager
        # -only action. Confirm this is really wanted before relying on it in practice.
        {"parent": "User", **FULL_NON_SUBMITTABLE},
    ]

    # Dependent reference/master doctypes: every Link field on the doctypes above
    # (including their child tables) is permission-checked independently -
    # frappe.database.query.py throws "Insufficient Permission for {doctype}" the
    # moment a Link field points at a doctype the role can't read, even with full
    # access to the parent document (see the Classy Accountant role's history for how
    # this surfaces). Unlike Classy Accountant, this role has NO "restricted viewing in
    # other modules" requirement - it explicitly reaches into Buying, Manufacturing/
    # Stock, and Payroll already via the primary doctypes above - so every dependency
    # found is granted read + report here rather than excluded by module.
    dependent_read_only = [
        "Account Category", "Activity Type", "Address",
        "Appraisal Template", "Asset", "Asset Category", "Asset Repair",
        "Attendance Request", "Auto Repeat", "BOM", "Bank Account", "Batch",
        "Blanket Order", "Branch", "Brand", "Company", "Cost Center", "Country",
        "Coupon Code", "Currency", "Customer Group", "Customs Tariff Number",
        "Delivery Note", "Delivery Trip", "Email Account",
        "Employee Grade", "Employee Health Insurance", "Employment Type",
        "Expense Claim Type", "Finance Book", "Gender", "Google Contacts",
        "Holiday List", "Incoterm", "Industry Type", "Issue", "Item Attribute",
        "Item Group", "Item Tax Template", "Job Applicant", "Job Card",
        "Journal Entry Template", "Language", "Lead", "Leave Block List",
        "Leave Type", "Letter Head", "Location", "Lower Deduction Certificate",
        "Loyalty Program", "Manufacturer", "Market Segment",
        "Mode of Payment", "Module Profile",
        "Opportunity Type", "POS Closing Entry", "POS Invoice",
        "POS Profile", "Payment Order", "Payment Request", "Payment Term",
        "Payment Terms Template", "Payroll Period",
        "Pick List", "Price List", "Pricing Rule",
        "Print Heading", "Process Deferred Accounting", "Product Bundle",
        "Production Plan", "Project Template", "Project Type", "Prospect",
        "Purchase Order", "Purchase Receipt", "Purchase Taxes and Charges Template",
        "Putaway Rule", "Quality Inspection", "Quality Inspection Template",
        "Role", "Role Profile",
        "Salary Withholding", "Sales Partner", "Sales Person", "Sales Stage",
        "Sales Taxes and Charges Template", "Salutation",
        "Serial and Batch Bundle", "Shipping Rule", "Skill",
        "Stock Entry Type", "Subcontracting Inward Order", "Subcontracting Order",
        "Subscription", "Supplier", "Supplier Group", "Supplier Quotation",
        "Task Type", "Tax Category", "Tax Withholding Category",
        "Tax Withholding Group", "Terms and Conditions", "Territory",
        "UOM Category", "UTM Campaign", "UTM Medium", "UTM Source",
        "User Type", "Vehicle Log", "Warehouse Type", "Work Order", "Workspace",
    ]
    perms += [{"parent": dt, "read": 1, "report": 1} for dt in dependent_read_only]

    for p in perms:
        existing = frappe.db.exists("Custom DocPerm", {"parent": p["parent"], "role": role_name})
        docperm = frappe.get_doc("Custom DocPerm", existing) if existing else frappe.new_doc("Custom DocPerm")
        docperm.parent = p["parent"]
        docperm.role = role_name
        docperm.read = p.get("read", 0)
        docperm.write = p.get("write", 0)
        docperm.create = p.get("create", 0)
        docperm.submit = p.get("submit", 0)
        docperm.cancel = p.get("cancel", 0)
        docperm.amend = p.get("amend", 0)
        docperm.delete = p.get("delete", 0)
        docperm.report = p.get("report", 0)
        docperm.save(ignore_permissions=True) if existing else docperm.insert(ignore_permissions=True)

    for p in perms:
        frappe.clear_cache(doctype=p["parent"])

    # 3. Grant visibility on standard reports that are role-restricted, same pattern as
    # Classy Accountant. Report.save() refuses to run on standard reports outside
    # developer mode (or bench migrate), so insert directly into the "Has Role" child
    # table instead of loading/saving the parent Report document.
    restricted_reports = [
        "Sales Register", "Accounts Receivable", "General Ledger", "Project Profitability",
        "Purchase Register", "Stock Ledger", "Stock Balance", "Item-wise Price List Rate",
        "Employee Leave Balance", "Salary Register", "Customer Lifecycle Billing",
    ]
    for report_name in restricted_reports:
        if not frappe.db.exists("Report", report_name):
            continue
        already_has_role = frappe.db.exists(
            "Has Role", {"parent": report_name, "parenttype": "Report", "role": role_name}
        )
        if not already_has_role:
            frappe.get_doc({
                "doctype": "Has Role",
                "parent": report_name,
                "parenttype": "Report",
                "parentfield": "roles",
                "role": role_name,
            }).insert(ignore_permissions=True)

    # 4. Create/update Workspace (desk landing icon for this role). Sectioned by module,
    # every label is the bare doctype/report name - each shortcut just opens that
    # doctype's list view (or the report), regardless of the verb a label might imply.
    workspace_name = "Admin Desk"
    sections = [
        ("CRM", [
            {"label": "Customer", "type": "DocType", "link_to": "Customer", "icon": "users"},
            {"label": "Lead", "type": "DocType", "link_to": "Lead", "icon": "users"},
            {"label": "Opportunity", "type": "DocType", "link_to": "Opportunity", "icon": "target"},
        ]),
        ("Sales", [
            {"label": "Quotation", "type": "DocType", "link_to": "Quotation", "icon": "file-text"},
            {"label": "Sales Order", "type": "DocType", "link_to": "Sales Order", "icon": "shopping-cart"},
        ]),
        ("Project", [
            {"label": "Project", "type": "DocType", "link_to": "Project", "icon": "folder-plus"},
            {"label": "Task", "type": "DocType", "link_to": "Task", "icon": "check-square"},
            {"label": "Timesheet", "type": "DocType", "link_to": "Timesheet", "icon": "clock"},
        ]),
        ("Inventory", [
            {"label": "Item", "type": "DocType", "link_to": "Item", "icon": "package"},
            {"label": "Warehouse", "type": "DocType", "link_to": "Warehouse", "icon": "package"},
            {"label": "Warehouse Rack", "type": "DocType", "link_to": "Warehouse Rack", "icon": "package"},
            {"label": "Material Request", "type": "DocType", "link_to": "Material Request", "icon": "package"},
            {"label": "Stock Entry", "type": "DocType", "link_to": "Stock Entry", "icon": "package"},
        ]),
        ("Accounting", [
            {"label": "Sales Invoice", "type": "DocType", "link_to": "Sales Invoice", "icon": "credit-card"},
            {"label": "Purchase Invoice", "type": "DocType", "link_to": "Purchase Invoice", "icon": "credit-card"},
            {"label": "Payment Entry", "type": "DocType", "link_to": "Payment Entry", "icon": "dollar-sign"},
            {"label": "Journal Entry", "type": "DocType", "link_to": "Journal Entry", "icon": "book-open"},
            {"label": "Expense Claim", "type": "DocType", "link_to": "Expense Claim", "icon": "check-circle"},
        ]),
        ("HR", [
            {"label": "Employee", "type": "DocType", "link_to": "Employee", "icon": "users"},
            {"label": "Department", "type": "DocType", "link_to": "Department", "icon": "users"},
            {"label": "User", "type": "DocType", "link_to": "User", "icon": "user"},
            {"label": "Employee Advance", "type": "DocType", "link_to": "Employee Advance", "icon": "credit-card"},
        ]),
        ("Reports", [
            {"label": "General Ledger", "type": "Report", "link_to": "General Ledger", "icon": "table"},
            {"label": "Accounts Receivable", "type": "Report", "link_to": "Accounts Receivable", "icon": "table"},
            {"label": "Stock Balance", "type": "Report", "link_to": "Stock Balance", "icon": "table"},
            {"label": "Salary Advance Report", "type": "Report", "link_to": "Salary Advance Report", "icon": "table"},
            {"label": "Loan Report", "type": "Report", "link_to": "Loan Report", "icon": "table"},
            {"label": "Customer Lifecycle Billing", "type": "Report", "link_to": "Customer Lifecycle Billing", "icon": "table"},
        ]),
    ]

    all_shortcuts = []
    content_blocks = []
    for section_key, section_shortcuts in sections:
        block_id_base = "wsAdmin" + section_key.replace(" ", "")
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
        workspace.icon = "setting"
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

    # 5. Pin the workspace to the Home/Desktop screen (creates its Workspace Sidebar +
    # Desktop Icon), same call the desk UI itself makes; idempotent.
    add_workspace_to_desktop(workspace_name)

    # 6. "HR Setup" - child workspace nested under Admin Desk (native parent_page
    # nesting: Workspace.get_public_items() matches child.parent_page == parent.title
    # and child.public == parent.public - see frappe/desk/doctype/workspace/workspace.py).
    # No separate Desktop Icon/Workspace Sidebar entry for the child - it's discovered
    # dynamically via that match and appears nested under Admin Desk in the sidebar.
    hr_setup_name = "HR Setup"
    hr_sections = [
        ("Payroll", [
            {"label": "Salary Component", "type": "DocType", "link_to": "Salary Component", "icon": "dollar-sign"},
            {"label": "Salary Structure", "type": "DocType", "link_to": "Salary Structure", "icon": "dollar-sign"},
            {"label": "Salary Structure Assignment", "type": "DocType", "link_to": "Salary Structure Assignment", "icon": "dollar-sign"},
            {"label": "Payroll Entry", "type": "DocType", "link_to": "Payroll Entry", "icon": "dollar-sign"},
            {"label": "Salary Slip", "type": "DocType", "link_to": "Salary Slip", "icon": "dollar-sign"},
            {"label": "Additional Salary", "type": "DocType", "link_to": "Additional Salary", "icon": "dollar-sign"},
        ]),
        ("Advance, Loan & Expense", [
            {"label": "Employee Advance", "type": "DocType", "link_to": "Employee Advance", "icon": "credit-card"},
            {"label": "Expense Claim", "type": "DocType", "link_to": "Expense Claim", "icon": "check-circle"},
        ]),
        ("Shift & Attendance", [
            {"label": "Employee Attendance Tool", "type": "DocType", "link_to": "Employee Attendance Tool", "icon": "clock"},
            {"label": "Employee Checkin", "type": "DocType", "link_to": "Employee Checkin", "icon": "clock"},
            {"label": "Shift Type", "type": "DocType", "link_to": "Shift Type", "icon": "clock"},
            {"label": "Overtime Type", "type": "DocType", "link_to": "Overtime Type", "icon": "clock"},
            {"label": "Overtime Slip", "type": "DocType", "link_to": "Overtime Slip", "icon": "clock"},
        ]),
        ("Settings", [
            {"label": "Payroll Settings", "type": "DocType", "link_to": "Payroll Settings", "icon": "setting"},
            {"label": "Employee Advance Settings", "type": "DocType", "link_to": "Employee Advance Settings", "icon": "setting"},
        ]),
    ]

    hr_all_shortcuts = []
    hr_content_blocks = []
    for section_key, section_shortcuts in hr_sections:
        block_id_base = "wsHrSetup" + section_key.replace(" ", "").replace(",", "")
        hr_content_blocks.append(
            {"id": block_id_base + "Head", "type": "header", "data": {"text": section_key, "level": 2}}
        )
        for i, s in enumerate(section_shortcuts):
            hr_content_blocks.append(
                {"id": f"{block_id_base}{i}", "type": "shortcut", "data": {"shortcut_name": s["label"], "col": 3}}
            )
        hr_all_shortcuts += section_shortcuts

    if frappe.db.exists("Workspace", hr_setup_name):
        hr_workspace = frappe.get_doc("Workspace", hr_setup_name)
    else:
        hr_workspace = frappe.new_doc("Workspace")
        hr_workspace.name = hr_setup_name
        hr_workspace.label = hr_setup_name
        hr_workspace.title = hr_setup_name
        hr_workspace.icon = "setting"
        hr_workspace.is_standard = 0
        hr_workspace.public = 1
        hr_workspace.roles = []
        hr_workspace.append("roles", {"role": role_name})

    hr_workspace.parent_page = workspace_name
    # Explicitly blank: a truthy module here makes on_update() try to export this
    # non-standard workspace to a real app module folder and throw "Module not found".
    hr_workspace.module = None
    hr_workspace.content = json.dumps(hr_content_blocks)
    hr_workspace.shortcuts = []
    for s in hr_all_shortcuts:
        hr_workspace.append("shortcuts", s)
    hr_workspace.save(ignore_permissions=True)

    frappe.clear_cache()
