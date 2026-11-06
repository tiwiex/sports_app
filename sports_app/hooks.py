app_name = "sports_app"
app_title = "Sports App"
app_publisher = "Idelta Technologies"
app_description = "Sports Academy Application"
app_email = "tiwiex@yahoo.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "sports_app",
# 		"logo": "/assets/sports_app/logo.png",
# 		"title": "Sports App",
# 		"route": "/sports_app",
# 		"has_permission": "sports_app.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sports_app/css/sports_app.css"
# app_include_js = "/assets/sports_app/js/sports_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/sports_app/css/sports_app.css"
# web_include_js = "/assets/sports_app/js/sports_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sports_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sports_app/public/icons.svg"

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

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sports_app.utils.jinja_methods",
# 	"filters": "sports_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sports_app.install.before_install"
# after_install = "sports_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sports_app.uninstall.before_uninstall"
# after_uninstall = "sports_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sports_app.utils.before_app_install"
# after_app_install = "sports_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sports_app.utils.before_app_uninstall"
# after_app_uninstall = "sports_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sports_app.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sports_app.tasks.all"
# 	],
# 	"daily": [
# 		"sports_app.tasks.daily"
# 	],
# 	"hourly": [
# 		"sports_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sports_app.tasks.weekly"
# 	],
# 	"monthly": [
# 		"sports_app.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "sports_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sports_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sports_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sports_app.utils.before_request"]
# after_request = ["sports_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["sports_app.utils.before_job"]
# after_job = ["sports_app.utils.after_job"]

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
# 	"sports_app.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


# Sports contributes views to the optional Boost host; it owns no copied shell.
boost_console_providers = ["sports_app.console.get_provider"]
after_install = ["sports_app.console.setup_console", "sports_app.payment_setup.setup_payment_support"]
after_migrate = ["sports_app.console.setup_console", "sports_app.payment_setup.setup_payment_support"]
on_login = "sports_app.console.set_console_login_redirect"

before_install = "sports_app.console.setup_roles"
before_migrate = "sports_app.console.setup_roles"

# Academy configuration links to ERPNext company and currency masters.
required_apps = ["erpnext"]

# Protect Sports-linked ERPNext receipt provenance without changing ERPNext core.
doc_events = {
	"Sales Invoice": {
		"validate": "sports_app.enrollment_invoices.validate_enrollment_invoice",
		"before_submit": "sports_app.enrollment_invoices.validate_finance_submission",
		"on_submit": "sports_app.enrollment_invoices.record_invoice_payment",
		"before_update_after_submit": "sports_app.enrollment_invoices.validate_enrollment_invoice",
	},
	"Payment Entry": {
		"validate": "sports_app.enrollment_payments.validate_sports_payment",
		"before_submit": "sports_app.enrollment_payments.validate_sports_payment",
	},
}

# App-owned invoice review action; core accounting stays in ERPNext.
doctype_js = {
	"Sales Invoice": "public/js/enrollment_invoice.js",
	"Sports Player": "public/js/player_id_change.js",
}

# Add the app-owned finance shortcut to Boost invoice menus.
from sports_app.console_assets import asset_url as sports_asset_url

app_include_js = [
	"/assets/sports_app/js/invoice_context_payment.js",
	sports_asset_url("console_navigation.js"),
]
