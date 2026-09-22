import json

import frappe
from frappe.desk.doctype.desktop_icon.desktop_icon import add_workspace_to_desktop


def setup_accountant_role():
    role_name = "Classy Accountant"

    # 1. Create Role
    if not frappe.db.exists("Role", role_name):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name,
            "desk_access": 1
        }).insert(ignore_permissions=True)

    # 2. Document Permissions
    perms = [
        # CRM - read-only
        {"parent": "Customer", "read": 1},
        {"parent": "Customer Group", "read": 1},
        {"parent": "Contact", "read": 1},
        {"parent": "Opportunity", "read": 1},
        # Sales & Quotations - full workflow (Quotation also supports amend for revisions)
        {"parent": "Quotation", "read": 1, "write": 1, "create": 1, "submit": 1, "amend": 1},
        {"parent": "Sales Order", "read": 1, "write": 1, "create": 1, "submit": 1},
        # Billing & Accounting - full access including cancel/amend. "report": 1 on Sales
        # Invoice is required for the Sales Register / Accounts Receivable reports below -
        # frappe.has_permission(ref_doctype, "report") is checked separately from "read".
        {"parent": "Sales Invoice", "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1, "report": 1},
        {"parent": "Payment Entry", "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1},
        {"parent": "Journal Entry", "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1},
        # Petty Cash & Expenses - review & approve only (no create: requests are raised by
        # the requesting employee/Project Supervisor, the Accountant approves/submits)
        {"parent": "Expense Claim", "read": 1, "write": 1, "submit": 1},
        # Read-only on report ref_doctypes not otherwise covered above, so the Accountant's
        # doctype-permission check passes for General Ledger (GL Entry) and Project
        # Profitability (Timesheet). "report": 1 required (see note above).
        {"parent": "GL Entry", "read": 1, "report": 1},
        {"parent": "Timesheet", "read": 1, "report": 1},
    ]

    # Dependent reference/master doctypes: every Link field on the doctypes above (including
    # their child tables, e.g. Quotation Item, Sales Taxes and Charges) is permission-checked
    # independently - frappe.database.query.py throws "Insufficient Permission for {doctype}"
    # the moment a Link field points at a doctype the role can't read, even with full access
    # to the parent document. Read-only, and scoped to Sales/Billing/Petty-Cash reference data
    # only. Deliberately EXCLUDES Buying (Purchase Order/Invoice, Supplier, Payment
    # Order/Request), Manufacturing/Stock (BOM, Material Request, Stock Entry, Quality
    # Inspection, Pick List, Batch, Serial and Batch Bundle, Delivery Note, Blanket Order,
    # Asset), and Payroll (Salary Slip) doctypes - the original spec calls for "restricted
    # viewing in other modules", so a Link field into one of those will still throw. Add the
    # relevant doctype here (with read: 1) if that turns out to be needed after all.
    #
    # NOTE: a doctype's `read` grant only counts at permlevel 0. Standard roles like "Desk
    # User" often grant `read` on doctypes like Project/Lead/POS Invoice at permlevel 1 only,
    # which does NOT grant baseline read access - checked here with frappe.has_permission()
    # against the real permission engine, not by reading the DocPerm table directly.
    dependent_read_only = [
        "Account", "Activity Type", "Auto Repeat", "Bank Account", "Brand", "Company",
        "Cost Center", "Coupon Code", "Currency", "Delivery Trip", "Department", "Employee",
        "Employee Advance", "Expense Claim Type", "Finance Book", "Fiscal Year", "Incoterm",
        "Industry Type", "Item", "Item Group", "Item Tax Template", "Journal Entry Template",
        "Lead", "Loyalty Program", "Market Segment", "Mode of Payment", "Opportunity Type",
        "POS Invoice", "Project", "Party Type",
        "POS Closing Entry", "POS Profile", "Payment Term", "Payment Terms Template",
        "Price List", "Pricing Rule", "Prospect", "Sales Partner", "Sales Person",
        "Sales Stage", "Sales Taxes and Charges Template", "Shipping Rule", "Subscription",
        "Task", "Tax Category", "Tax Withholding Category", "Tax Withholding Group",
        "Terms and Conditions", "Territory", "UOM", "UTM Campaign", "UTM Medium",
        "UTM Source", "Vehicle Log", "Warehouse",
    ]
    # "Party Type" isn't a schema Link target on any doctype above - the Accounts Receivable
    # report's JS filter (get_party_type_options()) queries it directly to populate a
    # dropdown, so it needs read access independently of GL Entry/Sales Invoice.
    perms += [{"parent": dt, "read": 1} for dt in dependent_read_only]

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
        docperm.report = p.get("report", 0)
        docperm.save(ignore_permissions=True) if existing else docperm.insert(ignore_permissions=True)

    for p in perms:
        frappe.clear_cache(doctype=p["parent"])

    # 3. Grant visibility on standard reports that are role-restricted.
    # These reports already list other roles (Accounts Manager/User, Auditor, HR roles,
    # etc.) - always APPEND, never overwrite, so existing roles keep access.
    # Note: Report.save() refuses to run on standard reports outside developer mode
    # (or bench migrate), so we insert directly into the "Has Role" child table instead
    # of loading and saving the parent Report document.
    restricted_reports = ["Sales Register", "Accounts Receivable", "General Ledger", "Project Profitability"]
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

    # 4. Create Workspace (desk landing icon for this role, so a Classy Accountant user
    # can run their whole workflow - quotations through billing to expense approval -
    # from one place after logging in)
    workspace_name = "Accountant Desk"
    if not frappe.db.exists("Workspace", workspace_name):
        action_shortcuts = [
            {"label": "New Quotation", "type": "DocType", "link_to": "Quotation", "icon": "file-text"},
            {"label": "New Sales Order", "type": "DocType", "link_to": "Sales Order", "icon": "shopping-cart"},
            {"label": "New Sales Invoice", "type": "DocType", "link_to": "Sales Invoice", "icon": "credit-card"},
            {"label": "New Payment Entry", "type": "DocType", "link_to": "Payment Entry", "icon": "dollar-sign"},
            {"label": "New Journal Entry", "type": "DocType", "link_to": "Journal Entry", "icon": "book-open"},
            {"label": "Approve Expense Claims", "type": "DocType", "link_to": "Expense Claim", "icon": "check-circle"},
        ]
        report_shortcuts = [
            {"label": "Sales Register", "type": "Report", "link_to": "Sales Register", "icon": "table"},
            {"label": "Accounts Receivable", "type": "Report", "link_to": "Accounts Receivable", "icon": "table"},
            {"label": "General Ledger", "type": "Report", "link_to": "General Ledger", "icon": "table"},
            {"label": "Project Profitability", "type": "Report", "link_to": "Project Profitability", "icon": "table"},
        ]

        content_blocks = [{"id": "wsAcctHead1", "type": "header", "data": {"text": "Accountant Actions", "level": 2}}]
        content_blocks += [
            {"id": f"wsAcctAct{i}", "type": "shortcut", "data": {"shortcut_name": s["label"], "col": 3}}
            for i, s in enumerate(action_shortcuts)
        ]
        content_blocks.append({"id": "wsAcctHead2", "type": "header", "data": {"text": "Reports", "level": 2}})
        content_blocks += [
            {"id": f"wsAcctRpt{i}", "type": "shortcut", "data": {"shortcut_name": s["label"], "col": 3}}
            for i, s in enumerate(report_shortcuts)
        ]

        frappe.get_doc({
            "doctype": "Workspace",
            "name": workspace_name,
            "label": workspace_name,
            "title": workspace_name,
            "icon": "accounting",
            "is_standard": 0,
            "public": 1,
            "roles": [{"role": role_name}],
            "content": json.dumps(content_blocks),
            "shortcuts": action_shortcuts + report_shortcuts,
        }).insert(ignore_permissions=True)

    # 5. Pin the workspace to the Home/Desktop screen (creates its Workspace Sidebar +
    # Desktop Icon) so a user with only this role sees it immediately after login.
    # Same call the desk UI itself makes to do this; idempotent (no-ops if both already exist).
    add_workspace_to_desktop(workspace_name)

    frappe.clear_cache()
