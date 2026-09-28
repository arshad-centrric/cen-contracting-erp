# Sales Order - Customizations & Logic

## 1. Custom Fields & Data Mapping
* **Project Details:** Custom fields (`cen_project_name`, `cen_choose_project`, `cen_project_type`) mapped to ensure continuity from Quotation. UI filtering managed by `project_filters.js`.

## 2. Validation Logic
* **Backend Sync:** Standard `project` field automatically synchronized with `cen_choose_project` upon validation via the backend hook (`overrides/opportunity/project_sync.py`).


## 3. Optional Delivery Date
* **Not Mandatory:** `delivery_date` on Sales Order and Sales Order Item is optional, so orders can be saved and submitted without a delivery date.
* **Backend:** ERPNext's `validate_delivery_date` throws "Please enter Delivery Date" on every Sales type order. It is relaxed by the `OptionalDeliveryDateMixin` class (`overrides/sales_order/optional_delivery_date.py`), mapped via `extend_doctype_class` in `hooks.py`. When no date is entered the check is skipped; once a date is entered ERPNext's standard behaviour still applies (dates copied between the order and its items, and a date before the order date is rejected).
* **Frontend:** ERPNext's form script marks the item Delivery Date column mandatory; `public/js/sales_order.js` overrides `toggle_delivery_date` in the `setup` event to keep it optional.
* **Property Setter:** `reqd = 0` on both fields in `setup/property_setter/sales_order.py`, so the fields stay optional even if another app makes them mandatory.

## 4. Items Table Layout
* **Description & UOM Always Visible:** `description` and `uom` are shown as columns in the items table (`in_list_view`) via Property Setters in `setup/property_setter/sales_order.py`.
* **Column Widths:** Item Code 2, Delivery Date 1, Description 2, Qty 1, UOM 1, Rate 1, Amount 2 (the grid holds 10 units; Frappe widens columns automatically when space is free).
