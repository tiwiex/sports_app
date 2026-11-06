frappe.ui.form.on("Sports Enrollment", {
	setup(frm) {
		frm.set_query("program", () => ({
			filters: { company: frm.doc.company, enabled: 1 },
		}));
		frm.set_query("group", () => ({
			filters: { program: frm.doc.program, enabled: 1 },
		}));
	},
	async player(frm) {
		if (frm.doc.player) {
			const row = await frappe.db.get_value("Sports Player", frm.doc.player, [
				"company",
				"customer",
			]);
			frm.set_value("company", row.message.company);
			frm.set_value("payer_customer", row.message.customer);
		}
	},
	program(frm) {
		frm.set_value("group", "");
	},
});
