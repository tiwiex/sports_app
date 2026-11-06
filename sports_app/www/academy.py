from frappe.sessions import get_csrf_token

from sports_app.registration import get_registration_fields
from sports_app.website import asset_url, get_website_content

no_cache = 1
sitemap = 0


def get_context(context):
	context.academy = get_website_content()
	context.registration_fields = get_registration_fields()
	context.csrf_token = get_csrf_token()
	from sports_app.academy import get_configured_settings

	settings = get_configured_settings()
	from sports_app.player_numbering import academy_date

	context.admission_date = str(academy_date(settings))
	context.payment_enabled = bool(settings.get("enrollment_payments_enabled"))
	context.website_css = asset_url("css/academy.css")
	context.website_js = asset_url("js/academy.js")
	context.no_cache = 1
	context.sitemap = 0
