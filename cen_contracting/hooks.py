app_name = "cen_contracting"
app_title = "Cen Contracting"
app_publisher = "Centrric Innovations Private Limited"
app_description = "A comprehensive ERPNext add-on for general contracting, featuring advanced project workflows, custom CRM routing, detailed petty cash handling, and HR enhancements."
app_email = "support@centrric.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "cen_contracting",
# 		"logo": "/assets/cen_contracting/logo.png",
# 		"title": "Cen Contracting",
# 		"route": "/cen_contracting",
# 		"has_permission": "cen_contracting.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cen_contracting/css/cen_contracting.css"
# app_include_js = "/assets/cen_contracting/js/cen_contracting.js"

# include js, css files in header of web template
# web_include_css = "/assets/cen_contracting/css/cen_contracting.css"
# web_include_js = "/assets/cen_contracting/js/cen_contracting.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "cen_contracting/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Sales Order": ["public/js/sales_order.js", "public/js/project_filters.js"],
    "Quotation": ["public/js/quotation.js", "public/js/project_filters.js"],
    "Lead": "public/js/lead.js",
    "Opportunity": "public/js/project_filters.js",
    "Project": "public/js/project.js",
    "Sales Invoice": "public/js/project_filters.js",
    "Expense Claim": "public/js/expense_claim.js",
    "Employee Advance": "public/js/employee_advance.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "cen_contracting/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "cen_contracting.utils.jinja_methods",
# 	"filters": "cen_contracting.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "cen_contracting.install.before_install"
# after_install = "cen_contracting.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "cen_contracting.uninstall.before_uninstall"
# after_uninstall = "cen_contracting.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "cen_contracting.utils.before_app_install"
# after_app_install = "cen_contracting.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "cen_contracting.utils.before_app_uninstall"
# after_app_uninstall = "cen_contracting.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "cen_contracting.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cen_contracting.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Opportunity": {
		"validate": "cen_contracting.overrides.opportunity.project_sync.sync_projects_on_validate"
	},
	"Quotation": {
		"before_insert": "cen_contracting.overrides.quotation.version_control.increment_version_number",
		"validate": "cen_contracting.overrides.opportunity.project_sync.sync_projects_on_validate"
	},
	"Sales Order": {
		"validate": "cen_contracting.overrides.opportunity.project_sync.sync_projects_on_validate"
	},
	"Purchase Invoice": {
		"on_submit": "cen_contracting.overrides.purchase_invoice.purchase_invoice_overrides.sync_project_costing",
		"on_cancel": "cen_contracting.overrides.purchase_invoice.purchase_invoice_overrides.sync_project_costing"
	},
	"Project": {
		"on_update": "cen_contracting.overrides.project.supervisor_assignment.sync_project_supervisor_assignment"
	},
	"Employee Advance": {
		"validate": "cen_contracting.overrides.employee_advance.advance_type_mapping.validate",
		"on_change": "cen_contracting.overrides.employee_advance.auto_recovery.on_change"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"cen_contracting.tasks.all"
# 	],
# 	"daily": [
# 		"cen_contracting.tasks.daily"
# 	],
# 	"hourly": [
# 		"cen_contracting.tasks.hourly"
# 	],
# 	"weekly": [
# 		"cen_contracting.tasks.weekly"
# 	],
# 	"monthly": [
# 		"cen_contracting.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "cen_contracting.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "cen_contracting.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cen_contracting.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "cen_contracting.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["cen_contracting.utils.before_request"]
# after_request = ["cen_contracting.utils.after_request"]

# Job Events
# ----------
# before_job = ["cen_contracting.utils.before_job"]
# after_job = ["cen_contracting.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"cen_contracting.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

after_migrate = [
    "cen_contracting.setup.custom_fields.create_custom_fields",
    "cen_contracting.setup.property_setter.quotation.set_quotation_properties",
    "cen_contracting.setup.property_setter.opportunity.set_opportunity_properties",
    "cen_contracting.setup.property_setter.project.set_project_properties",
    "cen_contracting.setup.roles.supervisor.setup_supervisor_role_and_workspace",
    "cen_contracting.setup.roles.accountant.setup_accountant_role",
    "cen_contracting.setup.roles.admin.setup_admin_role",
    "cen_contracting.setup.property_setter.employee_advance.set_employee_advance_properties"
]

override_doctype_class = {
    "Expense Claim": "cen_contracting.overrides.petty_cash.expense_claim.CustomExpenseClaim"
}
