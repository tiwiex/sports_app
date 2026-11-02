import frappe
from frappe.model.document import Document
from sports_app.registrations import SERVICE_CAPABILITY, validate_intake
from sports_app.players import require_player_access
from sports_app.academy import validate_company


class SportsRegistration(Document):
    def before_insert(self):
        if self.flags.sports_registration_service is not SERVICE_CAPABILITY:
            frappe.throw("Use the public registration form to create a registration.", frappe.PermissionError)

    def before_rename(self, *args, **kwargs):
        frappe.throw("Registration references cannot be renamed or merged.")

    def validate(self):
        service = self.flags.sports_registration_service is SERVICE_CAPABILITY
        if not (self.is_new() and service):
            require_player_access()
            validate_company(self.company)
        previous = self.get_doc_before_save()
        if previous:
            immutable = ("company", "submitted_on", "request_key", "request_hash", "acceptance_key")
            if any(self.get(key) != previous.get(key) for key in immutable):
                frappe.throw("Submission identity and original timestamp cannot change.")
            if not service and any(self.get(key) != previous.get(key) for key in ("sales_invoice", "payment_entry", "payment_customer", "payment_snapshot")):
                frappe.throw("Payment links are maintained by the enrollment payment service.", frappe.PermissionError)
            if (previous.payment_entry or previous.get("sales_invoice")) and any(self.get(key) != previous.get(key) for key in ("first_name", "last_name", "contact_email", "contact_phone", "program")):
                frappe.throw("Payment-linked identity and program details are locked. Contact Finance for correction.")
            if previous.status != "Pending":
                frappe.throw("Reviewed registrations cannot be changed.")
            if not service and any(self.get(key) != previous.get(key) for key in
                ("status", "player", "reviewed_by", "reviewed_on", "rejection_reason")):
                frappe.throw("Use the registration review actions to change status.", frappe.PermissionError)
        validate_intake(self)
        program = frappe.get_doc("Sports Program", self.program)
        if program.company != self.company or not program.enabled:
            frappe.throw("Select an enabled program in the registration's company.")
        if not (self.is_new() and service):
            program.check_permission("read")
