# Opportunity - Customizations & Logic

## 1. Custom Fields & Data Mapping
* **Project Tracking:** Custom fields (`cen_project_name`, `cen_choose_project`, `cen_project_type`) created to track projects decoupled from standard Frappe project records.
* **Party Details:** Custom fields (`cen_party_name_details`, `cen_party_organization`) added. These fields automatically fetch and display the actual Lead or Customer name/company based on the selected `party_name`, handled via `project_filters.js`.

## 2. Validation & UI Logic
* **Mandatory Contacts:** `contact_person` and `contact_mobile` are strictly enforced as mandatory on the frontend UI level via `public/js/project_filters.js`.
* **Project Syncing:** The `cen_choose_project` field acts as the primary UI selector and automatically syncs with the hidden standard `project` field via a backend Python `validate` hook (`overrides/opportunity/project_sync.py`) and frontend JS to ensure standard reports continue to work.

