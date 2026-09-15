# cen_contracting Developer Guide

## Architecture Overview
This app utilizes a strictly decoupled, **DocType-centric directory structure**. This prevents merge conflicts, ensures domain logic is isolated, and makes finding code intuitive.

* **`cen_contracting/setup/`**: Contains Python-based database schema updates (custom fields) and installation scripts.
* **`cen_contracting/public/js/`**: Contains all Client-Side UI scripts named after their respective DocTypes.
* **`cen_contracting/overrides/`**: The core directory for all backend business logic.
  * **Structure:** `overrides/[doctype_name]/[feature_name].py`
  * **Example:** `overrides/quotation/pricing_logic.py`

## Strict Development Rules

1. **NO EXPORTED FIXTURES FOR CUSTOM FIELDS:** 
   Do not use standard Frappe export fixtures for custom fields. All new custom fields must be defined programmatically as a dictionary inside `cen_contracting/setup/custom_fields.py` and mapped to `after_migrate` in `hooks.py`. This ensures clean version control.

2. **PREFIX CONVENTION:** 
   Every custom field created for this app must strictly use the `cen_` prefix (e.g., `cen_project_type`).

3. **CLIENT SCRIPTS:** 
   Do not write JavaScript inside the standard ERPNext "Client Script" DocType GUI. All UI overrides must be written in `public/js/` and mapped in `hooks.py` using the `doctype_js` dictionary.

4. **ADDING NEW LOGIC:** 
   When developing a new feature for a specific document, create a descriptive Python file inside that document's folder in `overrides/` (e.g., `overrides/sales_invoice/retention_reminder.py`). Map any document hooks (like `on_submit` or `validate`) in `hooks.py` pointing specifically to these functions.

Important note : Instead of folder name : custom_logic use the name : overrides. 

