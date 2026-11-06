import frappe
from frappe import _
from frappe.model.document import Document

from sports_app.academy import enrollment_series, get_configured_settings, validate_company
from sports_app.player_numbering import academy_date
from sports_app.players import require_player_access
from sports_app.registration import validate_application_age
from sports_app.registrations import SERVICE_CAPABILITY, validate_intake


class SportsRegistration(Document):
	def autoname(self):
		from frappe.model.naming import make_autoname

		settings = get_configured_settings()
		self.name = make_autoname(enrollment_series(settings.get("enrollment_naming_series")), doc=self)

	def before_insert(self):
		if self.flags.sports_registration_service is not SERVICE_CAPABILITY:
			frappe.throw(
				_("Use the public registration form to create a registration."), frappe.PermissionError
			)

	def before_rename(self, *args, **kwargs):
		frappe.throw(_("Registration references cannot be renamed or merged."))

	def validate(self):
		service = self.flags.sports_registration_service is SERVICE_CAPABILITY
		if not (self.is_new() and service):
			require_player_access()
			validate_company(self.company)
		previous = self.get_doc_before_save()
		if previous:
			immutable = (
				"company",
				"submitted_on",
				"request_key",
				"request_hash",
				"acceptance_key",
				"photo_hash",
				"player_photo",
			)
			if any(self.get(key) != previous.get(key) for key in immutable):
				frappe.throw(_("Submission identity and original timestamp cannot change."))
			if not service and any(
				self.get(key) != previous.get(key)
				for key in ("sales_invoice", "payment_entry", "payment_customer", "payment_snapshot")
			):
				frappe.throw(
					_("Payment links are maintained by the enrollment payment service."),
					frappe.PermissionError,
				)
			if (previous.payment_entry or previous.get("sales_invoice")) and any(
				self.get(key) != previous.get(key)
				for key in ("first_name", "last_name", "contact_email", "contact_phone", "program")
			):
				frappe.throw(
					_(
						"Payment-linked identity and program details are locked. Contact Finance for correction."
					)
				)
			if previous.status != "Pending":
				frappe.throw(_("Reviewed registrations cannot be changed."))
			if not service and any(
				self.get(key) != previous.get(key)
				for key in ("status", "player", "reviewed_by", "reviewed_on", "rejection_reason")
			):
				frappe.throw(
					_("Use the registration review actions to change status."), frappe.PermissionError
				)
		validate_intake(self)
		if self.is_new() or (previous and previous.contact_email != self.contact_email):
			from sports_app.enrollment_accounts import normalize_email, require_available_player_email

			require_available_player_email(self.contact_email, self.name)
			if normalize_email(self.guardian_email) == self.contact_email:
				frappe.throw(_("Player and guardian must use separate email addresses."))
		previous_birth = previous.get("birth_date") if previous else None
		if self.is_new() or (previous and str(previous_birth) != str(self.birth_date)):
			validate_application_age(self.birth_date, academy_date(get_configured_settings()))
		program = frappe.get_doc("Sports Program", self.program)
		if program.company != self.company or not program.enabled:
			frappe.throw(_("Select an enabled program in the registration's company."))
		if not (self.is_new() and service):
			program.check_permission("read")
