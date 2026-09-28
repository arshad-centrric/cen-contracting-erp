# Sales Invoice - Customizations & Logic

## 1. Custom Fields & Data Mapping
* **Project Details:** Custom fields (`cen_project_name`, `cen_choose_project`, `cen_project_type`) mapped to ensure project continuity from the Sales Order.


## 2. Items Table Layout
* **Description & UOM Always Visible:** `description` and `uom` are shown as columns in the items table (`in_list_view`) via Property Setters in `setup/property_setter/sales_invoice.py`.
* **Column Widths:** Item Code 2, Description 2, Qty 1, UOM 1, Rate 1, Amount 1. The standard Warehouse column (2 units) still appears only when Update Stock is ticked.
