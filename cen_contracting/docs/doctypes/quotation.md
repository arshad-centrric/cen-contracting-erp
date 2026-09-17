# Quotation - Customizations & Logic

## 1. Custom Fields & Data Mapping
* **Company & Customer Details:** Handled via standard ERPNext fields (`company`, `party_name`, `customer_address`).
* **Attention To:** Handled via standard `contact_person` field. Will be formatted as "Attention To: [Name]" on the print format.
* **Customer Reference / LPO:** Custom field `cen_lpo_number` created (Data field).
* **Payment Terms:** Standard `payment_terms_template` is used for tabular schedules. Custom field `cen_payment_terms` is available for free-text conditions.
* **Project Syncing:** Custom fields (`cen_project_name`, `cen_choose_project`, `cen_project_type`) migrated and active. UI filtering managed by `project_filters.js`.


## 2. Validation & Pricing Logic
* **Validity Date Bypass:** The standard mandatory requirement for `valid_till` (Quotation Expiry) has been disabled via a backend Property Setter (`setup/property_setter/quotation.py`) to allow open-ended quotations.
* **SQM Pricing Strategy:** No custom code is required for SQM pricing. The requirement for quotations to be primarily entered on a per SQM basis will be handled natively by configuring the Default Sales UOM to "Sqm" on the respective Item Masters.
