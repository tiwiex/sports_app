/* Finance reviews the invoice; receipt creation and allocation stay on the server. */
frappe.ui.form.on("Sales Invoice", {
	async refresh(frm) {
		if (
			!frm.doc.sports_registration ||
			frm.doc.docstatus !== 0 ||
			frm.doc.workflow_state !== "Pending Review"
		)
			return;
		const response = await frappe.call({
			method: "sports_app.enrollment_invoices.completion_access",
			args: { name: frm.doc.name },
		});
		if (
			!response.message ||
			frm.doc.docstatus !== 0 ||
			frm.doc.workflow_state !== "Pending Review"
		)
			return;
		frm.dashboard.add_comment(
			__(
				"Use Complete Payment only after verifying the full bank credit. The invoice and its allocated receipt will be submitted together."
			),
			"blue",
			true
		);
		frm.add_custom_button(__("Complete Payment"), async () => {
			if (frm.__sports_completing) return;
			frm.__sports_completing = true;
			try {
				await frappe.call({
					method: "sports_app.enrollment_invoices.complete_payment",
					args: { name: frm.doc.name },
					freeze: true,
					freeze_message: __("Completing invoice payment…"),
				});
				await frm.reload_doc();
				frappe.show_alert({
					message: __("Payment completed and allocated to this invoice."),
					indicator: "green",
				});
			} finally {
				frm.__sports_completing = false;
			}
		});
	},
});
