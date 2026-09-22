# Purchase Invoice Customizations

This document outlines the custom business logic applied to the standard `Purchase Invoice` DocType within the `cen_contracting` app.

## Project Costing Synchronization (`on_submit`, `on_cancel`)
**Location:** `cen_contracting.overrides.purchase_invoice.purchase_invoice_overrides.sync_project_costing`

### Description
Standard ERPNext uses an incremental caching mechanism (adding `current_purchase_cost + new_value`) to update Project costs when an invoice is submitted. This mechanism was prone to caching drift and double-counting (e.g., adding the total sum to the existing sum instead of setting it).

To ensure 100% accurate cost accounting matching the General Ledger, we override this behavior. When a Purchase Invoice is submitted or cancelled, this hook:
1. Identifies all unique `Project`s referenced in the invoice items.
2. Triggers `project_doc.update_purchase_costing()`, which runs an absolute recalculation by summing all `docstatus=1` invoice items directly from the SQL database.
3. Automatically recalculates and updates the `gross_margin` and `per_gross_margin` based on the new absolutely correct purchase cost.

### Important Note
A previous unauthorized modification to core ERPNext (`erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py`) that attempted to force Gross Margin updates has been successfully reverted, and its responsibility migrated to this decoupled hook to comply with our architecture guidelines.
