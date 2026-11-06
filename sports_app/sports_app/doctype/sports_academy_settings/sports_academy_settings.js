frappe.ui.form.on("Sports Academy Settings", {
	setup(frm) {
		frm.set_query("default_program", () => ({
			filters: { company: frm.doc.company, enabled: 1 },
		}));
		frm.set_query("default_group", () => ({
			filters: { program: frm.doc.default_program, enabled: 1 },
		}));
		frm.set_query("currency", () => ({ filters: { enabled: 1 } }));
	},
});
