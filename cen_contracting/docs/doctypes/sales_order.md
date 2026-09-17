# Sales Order - Customizations & Logic

## 1. Custom Fields & Data Mapping
* **Project Details:** Custom fields (`cen_project_name`, `cen_choose_project`, `cen_project_type`) mapped to ensure continuity from Quotation. UI filtering managed by `project_filters.js`.

## 2. Validation Logic
* **Backend Sync:** Standard `project` field automatically synchronized with `cen_choose_project` upon validation via the backend hook (`overrides/opportunity/project_sync.py`).

