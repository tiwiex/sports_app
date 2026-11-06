/* Sports-owned correction UI, shared by the console and native Player form. */
frappe.provide("frappe.sports_player_ids");
frappe.sports_player_ids.change = async (name, afterChange) => {
	const response = await frappe.call({
		method: "sports_app.players_api.get_player",
		args: { name },
	});
	const result = response.message;
	if (!result.can_change_id) {
		frappe.msgprint(
			__("Only an academy administrator with write access can change this player ID.")
		);
		return;
	}
	const requestKey = crypto.randomUUID();
	const dialog = new frappe.ui.Dialog({
		title: __("Change Player ID"),
		fields: [
			{
				fieldname: "old_id",
				label: __("Current player ID"),
				fieldtype: "Data",
				read_only: 1,
				default: name,
			},
			{
				fieldname: "new_id",
				label: __("New player ID"),
				fieldtype: "Data",
				reqd: 1,
				description: __(
					"Use a unique ID. Existing and retired IDs cannot be reused. Linked records are updated; Customer and User accounts stay the same."
				),
			},
			{
				fieldname: "reason",
				label: __("Reason for change"),
				fieldtype: "Small Text",
				reqd: 1,
				description: __(
					"Recorded in the ID change history. Refresh downloaded attendance rosters after the change; preserve pending offline work for conflict review."
				),
			},
		],
		primary_action_label: __("Change Player ID"),
		async primary_action(values) {
			dialog.get_primary_btn().prop("disabled", true);
			try {
				const saved = await frappe.call({
					method: "sports_app.player_ids.change_player_id",
					args: {
						name,
						new_id: values.new_id,
						reason: values.reason,
						modified: result.player.modified,
						request_key: requestKey,
					},
				});
				dialog.hide();
				await afterChange(saved.message);
			} finally {
				dialog.get_primary_btn().prop("disabled", false);
			}
		},
	});
	dialog.show();
	return dialog;
};
if (frappe.ui.form?.on) {
	frappe.ui.form.on("Sports Player", {
		async refresh(frm) {
			if (frm.is_new()) return;
			const response = await frappe.call({
				method: "sports_app.players_api.get_player",
				args: { name: frm.doc.name },
			});
			if (response.message.can_change_id && response.message.player.name === frm.doc.name)
				frm.add_custom_button(__("Change Player ID"), () =>
					frappe.sports_player_ids.change(frm.doc.name, (newName) =>
						frappe.set_route("Form", "Sports Player", newName)
					)
				);
		},
	});
}
