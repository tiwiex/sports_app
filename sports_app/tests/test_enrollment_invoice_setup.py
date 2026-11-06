from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import payment_setup


class TestInvoiceWorkflowCompatibility(TestCase):
	def workflow(self):
		return SimpleNamespace(
			name="Existing customer workflow",
			states=[frappe._dict(state="Approved", doc_status=1)],
			transitions=[
				frappe._dict(state="Pending Review", action="Complete Payment", next_state="Approved")
			],
			save=Mock(),
		)

	def test_compatible_existing_workflow_is_not_replaced_or_modified(self):
		workflow = self.workflow()
		fake = SimpleNamespace(get_all=Mock(return_value=[workflow.name]))
		with (
			patch.object(payment_setup, "frappe", fake),
			patch("sports_app.enrollment_invoices.invoice_workflow", return_value=workflow),
		):
			payment_setup.ensure_invoice_workflow()
		workflow.save.assert_not_called()

	def test_incompatible_existing_workflow_is_rejected_without_mutation(self):
		workflow = self.workflow()
		workflow.transitions = []

		def throw(message):
			raise frappe.ValidationError(message)

		fake = SimpleNamespace(get_all=Mock(return_value=[workflow.name]), throw=throw)
		with (
			patch.object(payment_setup, "frappe", fake),
			patch("sports_app.enrollment_invoices.invoice_workflow", return_value=workflow),
			self.assertRaises(frappe.ValidationError),
		):
			payment_setup.ensure_invoice_workflow()
		workflow.save.assert_not_called()
