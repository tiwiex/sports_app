/* Academy configuration belongs to Sports App; Boost only mounts the view. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:settings"] = () => {
	let host,
		signal,
		form,
		configuration,
		activeTab = "general",
		tabSerial = 0;
	const node = (tag, text, className) => {
		const element = document.createElement(tag);
		if (text) element.textContent = __(text);
		if (className) element.className = className;
		return element;
	};
	const call = async (method, args = {}) => {
		const response = await frappe.call({
			method: `sports_app.settings_api.${method}`,
			args,
		});
		return response.message;
	};
	const button = (label, action, primary = false) => {
		const element = node("button", label, `btn btn-${primary ? "primary" : "default"} btn-sm`);
		element.type = "button";
		element.addEventListener("click", action, { signal });
		return element;
	};
	const companyOptions = () => configuration.companies.map((row) => row.name);
	const programFields = [
		{
			fieldname: "program_name",
			label: __("Program name"),
			fieldtype: "Data",
			reqd: 1,
		},
		{ fieldname: "sport", label: __("Sport"), fieldtype: "Data", reqd: 1 },
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Select",
			options: [],
			reqd: 1,
		},
		{
			fieldname: "enabled",
			label: __("Enabled"),
			fieldtype: "Check",
			default: 1,
		},
	];
	const groupFields = [
		{
			fieldname: "group_name",
			label: __("Group name"),
			fieldtype: "Data",
			reqd: 1,
		},
		{
			fieldname: "program",
			label: __("Program"),
			fieldtype: "Link",
			options: "Sports Program",
			reqd: 1,
			get_query: () => ({
				filters: { enabled: 1, company: form.get_value("company") },
			}),
		},
		{
			fieldname: "enabled",
			label: __("Enabled"),
			fieldtype: "Check",
			default: 1,
		},
	];
	const dialogs = new Set();
	const editMaster = (kind, existing) => {
		const isProgram = kind === "program";
		const fields = (isProgram ? programFields : groupFields).map((field) => ({
			...field,
		}));
		if (isProgram)
			fields.find((field) => field.fieldname === "company").options = companyOptions();
		const dialog = new frappe.ui.Dialog({
			title: isProgram ? __("Program") : __("Group"),
			fields,
			primary_action_label: __("Save"),
			async primary_action(values) {
				dialog.get_primary_btn().prop("disabled", true);
				try {
					const name = existing?.name;
					await call(isProgram ? "save_program" : "save_group", {
						[kind]: { ...values, ...(name ? { name } : {}) },
					});
					dialog.hide();
					// Preserve unsaved settings when refreshing master lists.
					const current = form.get_values(true);
					await render(current);
				} finally {
					dialog.get_primary_btn().prop("disabled", false);
				}
			},
		});
		dialogs.add(dialog);
		dialog.set_values(
			existing || {
				company: form.get_value("company"),
				program: form.get_value("default_program"),
				enabled: 1,
			}
		);
		dialog.show();
	};
	const renderMasters = (parent, title, rows, kind) => {
		const section = node("section");
		section.style.marginTop = "28px";
		section.append(
			node("h4", title),
			button(kind === "program" ? "New Program" : "New Group", () => editMaster(kind))
		);
		if (!rows.length)
			section.append(
				node(
					"p",
					kind === "program" ? "No programs configured." : "No groups configured.",
					"text-muted"
				)
			);
		const table = node("table", null, "table table-striped");
		const header = node("tr");
		for (const label of [
			"Name",
			kind === "program" ? "Sport" : "Program",
			"Company",
			"Status",
			"",
		])
			header.append(node("th", label));
		const head = node("thead");
		head.append(header);
		table.append(head);
		const body = node("tbody");
		for (const row of rows) {
			const tr = node("tr");
			const program = configuration.programs.find((item) => item.name === row.program);
			for (const value of [
				row[`${kind}_name`],
				kind === "program" ? row.sport : program?.program_name || row.program,
				row.company,
				row.enabled ? __("Enabled") : __("Disabled"),
			]) {
				const td = node("td");
				td.textContent = value || "";
				tr.append(td);
			}
			const td = node("td");
			td.append(button("Edit", () => editMaster(kind, row)));
			tr.append(td);
			body.append(tr);
		}
		table.append(body);
		const scroll = node("div", null, "table-responsive");
		scroll.append(table);
		section.append(scroll);
		parent.append(section);
	};
	const render = async (preserved) => {
		configuration = await call("get_configuration");
		if (signal.aborted) return;
		const wrapper = node("div", null, "sports-academy-settings");
		const style = node("style");
		style.textContent = `.sports-academy-settings{min-width:0}.sports-academy-settings .academy-tabs{display:flex;gap:6px;overflow-x:auto;max-width:100%;margin:16px 0;border-bottom:1px solid var(--border-color,#d7e2ed);padding-bottom:6px}.sports-academy-settings [role=tab]{flex:0 0 auto;white-space:nowrap;border:0;border-bottom:3px solid transparent;background:transparent;padding:10px 12px;font:inherit;font-weight:600;color:var(--text-muted,#607287);cursor:pointer}.sports-academy-settings [role=tab][aria-selected=true]{border-color:var(--primary,#176b50);color:var(--text-color,#173042);background:var(--subtle-fg,#f4f8fb)}.sports-academy-settings [role=tab]:focus-visible{outline:2px solid var(--primary,#176b50);outline-offset:-2px}.sports-academy-settings [role=tabpanel]{min-width:0}.sports-academy-settings [role=tabpanel][hidden]{display:none!important}.sports-academy-settings .table-responsive{max-width:100%;overflow:auto}`;
		wrapper.append(style);
		wrapper.append(
			node("h3", "Academy Settings"),
			node(
				"p",
				"Choose a company, manage programs and groups in their tab, then save the academy's defaults. Saving does not create players or charges.",
				"text-muted"
			)
		);
		if (!configuration.companies.length)
			wrapper.append(
				node(
					"p",
					"No accessible company. Ask the administrator to grant access to the academy's company.",
					"alert alert-warning"
				)
			);
		const controls = node("div");
		wrapper.append(controls);
		const values = preserved || configuration.settings;
		form = new frappe.ui.FieldGroup({
			body: controls,
			fields: [
				{
					fieldname: "academy_name",
					label: __("Academy name"),
					fieldtype: "Data",
					reqd: 1,
				},
				{
					fieldname: "print_logo",
					label: __("Document logo"),
					fieldtype: "Attach Image",
					description: __("Logo for Sports invoice and receipt PDFs."),
				},
				{
					fieldname: "company",
					label: __("Company"),
					fieldtype: "Select",
					options: ["", ...companyOptions()],
					reqd: 1,
				},
				{
					fieldname: "currency",
					label: __("Fee currency"),
					fieldtype: "Link",
					options: "Currency",
					reqd: 1,
					get_query: () => ({ filters: { enabled: 1 } }),
				},
				{
					fieldname: "timezone",
					label: __("Academy timezone"),
					fieldtype: "Select",
					options: ["", ...configuration.timezones],
					reqd: 1,
				},
				{
					fieldname: "registration_prefix",
					label: __("Player ID prefix"),
					fieldtype: "Data",
					reqd: 1,
					description: __(
						"For example MSA. Backend adds year/month and a continuous counter: MSA26-08001. Existing player IDs stay unchanged."
					),
				},
				{
					fieldname: "registration_digits",
					label: __("Player sequence digits"),
					fieldtype: "Int",
					default: 3,
					reqd: 1,
				},
				{
					fieldname: "player_starting_sequence",
					label: __("Player starting sequence"),
					fieldtype: "Data",
					default: "1",
					description: __(
						"Minimum sequence for new players, for example 126 after legacy number 125. Higher issued/imported numbers take precedence. Lowering this never resets numbering or changes existing IDs. Import old players first using their ID column."
					),
				},
				{
					fieldname: "enrollment_naming_series",
					label: __("Enrollment naming series"),
					fieldtype: "Data",
					default: "MSA-ENR-.YYYY.-.#####",
					reqd: 1,
					description: __(
						"Example: MSA-ENR-.YYYY.-.##### produces MSA-ENR-2026-00001. Optional year; 4-10 counter digits. Applies to new applications; existing references and invoice numbers stay unchanged."
					),
				},
				{
					fieldname: "default_enrollment_status",
					label: __("Default enrollment status"),
					fieldtype: "Select",
					options: "Pending\nActive",
					default: "Pending",
					reqd: 1,
				},
				{
					fieldname: "default_program",
					label: __("Default program"),
					fieldtype: "Link",
					options: "Sports Program",
					reqd: 1,
					get_query: () => ({
						filters: { company: form.get_value("company"), enabled: 1 },
					}),
				},
				{
					fieldname: "default_group",
					label: __("Default group"),
					fieldtype: "Link",
					options: "Sports Group",
					get_query: () => ({
						filters: { program: form.get_value("default_program"), enabled: 1 },
					}),
				},
				{
					fieldname: "monthly_fees_enabled",
					label: __("Monthly fees enabled"),
					fieldtype: "Check",
					default: 1,
				},
				{
					fieldname: "automatic_monthly_billing",
					label: __("Automatically submit monthly invoices"),
					fieldtype: "Check",
					description: __(
						"Posts invoices after each month ends, catching up from enrollment dates. Payments are confirmed separately."
					),
				},
				{
					fieldname: "monthly_billing_start",
					label: __("Automatic billing starts"),
					hidden: 1,
					fieldtype: "Date",
					description: __(
						"First day of the earliest month to bill. Earlier months are not backfilled."
					),
				},
				{
					fieldname: "monthly_billing_user",
					label: __("Billing automation user"),
					fieldtype: "Link",
					options: "User",
					get_query: () => ({
						filters: { enabled: 1, user_type: "System User" },
					}),
					description: __(
						"Requires Sports billing and native invoice submission/workflow rights. No roles are granted."
					),
				},
				{
					fieldname: "default_monthly_fee",
					label: __("Default monthly fee"),
					fieldtype: "Currency",
					options: "currency",
					description: __(
						"Default for monthly fees. Saving this amount does not create a charge or payment."
					),
				},
				{
					fieldname: "enrollment_payment_section",
					label: __("Website enrollment payments"),
					fieldtype: "Section Break",
				},
				{
					fieldname: "enrollment_payments_enabled",
					label: __("Enable enrollment payments"),
					fieldtype: "Check",
				},
				{
					fieldname: "payment_review_emails",
					label: __("Payment review email addresses"),
					fieldtype: "Small Text",
					description: __(
						"Comma-separated email addresses to notify when an applicant reports payment. Leave blank to disable. Recipients still need their normal Finance approval permissions."
					),
				},
				{
					fieldname: "enrollment_payment_currency",
					label: __("Enrollment payment currency"),
					fieldtype: "Link",
					options: "Currency",
				},
				{
					fieldname: "enrollment_items",
					label: __("Enrollment charges"),
					fieldtype: "Table",
					options: "Sports Enrollment Charge",
					in_place_edit: true,
					fields: [
						{
							fieldname: "item_code",
							label: __("Item"),
							fieldtype: "Link",
							options: "Item",
							reqd: 1,
							in_list_view: 1,
							columns: 4,
							get_query: () => ({ filters: { disabled: 0, is_sales_item: 1 } }),
						},
						{
							fieldname: "qty",
							label: __("Quantity"),
							fieldtype: "Float",
							precision: 4,
							default: 1,
							reqd: 1,
							in_list_view: 1,
							columns: 2,
						},
						{
							fieldname: "rate",
							label: __("Rate"),
							fieldtype: "Currency",
							reqd: 1,
							in_list_view: 1,
							columns: 2,
						},
						{
							fieldname: "amount",
							label: __("Amount"),
							fieldtype: "Currency",
							read_only: 1,
							in_list_view: 1,
							columns: 2,
						},
					],
					description: __(
						"Select existing Items and set quantity/rate. These rows form the initial invoice; charging stock Items does not issue stock."
					),
				},
				{
					fieldname: "enrollment_monthly_fee",
					label: __("Monthly fee (information only)"),
					fieldtype: "Currency",
					options: "enrollment_payment_currency",
				},
				{
					fieldname: "enrollment_bank_account",
					label: __("Enrollment bank account"),
					fieldtype: "Link",
					options: "Bank Account",
					get_query: () => ({
						filters: {
							company: form.get_value("company"),
							is_company_account: 1,
							disabled: 0,
						},
					}),
				},
				{
					fieldname: "enrollment_receivable_account",
					label: __("Enrollment receivable account"),
					fieldtype: "Link",
					options: "Account",
					get_query: () => ({
						filters: {
							company: form.get_value("company"),
							account_type: "Receivable",
							is_group: 0,
							disabled: 0,
						},
					}),
				},
			],
		});
		form.make();
		await form.set_values(values);
		const updateCharges = () => {
			if (signal.aborted) return;
			for (const row of form.get_value("enrollment_items") || [])
				row.amount = Math.round(Number(row.qty || 0) * Number(row.rate || 0) * 100) / 100;
			for (const row of form.fields_dict.enrollment_items.grid?.grid_rows || [])
				row.refresh_field("amount");
		};
		form.fields_dict.enrollment_items.grid?.wrapper.on("change.sportsChargeTotals", () =>
			setTimeout(updateCharges, 0)
		);
		updateCharges();
		if (signal.aborted) return;
		const preview = node("p", null, "text-muted");
		const updatePreview = () => {
			const digits = Math.min(
				10,
				Math.max(3, Number(form.get_value("registration_digits")) || 3)
			);
			preview.textContent = __("Registration example: {0} (preview only)", [
				`${form.get_value("registration_prefix") || "…"}YY-MM${String(
					form.get_value("player_starting_sequence") || "1"
				).padStart(digits, "0")}`,
			]);
		};
		form.fields_dict.registration_prefix.df.onchange = updatePreview;
		form.fields_dict.registration_digits.df.onchange = updatePreview;
		form.fields_dict.player_starting_sequence.df.onchange = updatePreview;
		form.fields_dict.company.df.onchange = () => {
			form.set_value("default_program", "");
			form.set_value("default_group", "");
		};
		form.fields_dict.default_program.df.onchange = () => form.set_value("default_group", "");
		updatePreview();
		const groups = [
			[
				"general",
				"General",
				["academy_name", "print_logo", "company", "currency", "timezone"],
			],
			[
				"numbering",
				"Player IDs",
				[
					"registration_prefix",
					"registration_digits",
					"player_starting_sequence",
					"enrollment_naming_series",
				],
			],
			[
				"defaults",
				"Enrollment defaults",
				["default_enrollment_status", "default_program", "default_group"],
			],
			[
				"fees",
				"Monthly fees",
				[
					"monthly_fees_enabled",
					"automatic_monthly_billing",
					"monthly_billing_start",
					"monthly_billing_user",
					"default_monthly_fee",
				],
			],
			[
				"payments",
				"Website payments",
				[
					"enrollment_payments_enabled",
					"payment_review_emails",
					"enrollment_payment_currency",
					"enrollment_items",
					"enrollment_monthly_fee",
					"enrollment_bank_account",
					"enrollment_receivable_account",
				],
			],
			["masters", "Programs & groups", []],
		];
		// Keep controls inside their original FieldGroup wrapper so native change,
		// dependency and validation handlers still operate across all sections.
		const root = form.wrapper?.[0] || controls;
		const nav = node("div", null, "academy-tabs"),
			panels = {},
			tabs = {},
			fieldTabs = {};
		nav.setAttribute("role", "tablist");
		nav.setAttribute("aria-label", __("Academy settings sections"));
		root.append(nav);
		const id = `academy-settings-${Date.now()}-${++tabSerial}`;
		const selectTab = (key, focus = false) => {
			activeTab = key;
			for (const [name] of groups) {
				const selected = key === name;
				tabs[name].setAttribute("aria-selected", String(selected));
				tabs[name].tabIndex = selected ? 0 : -1;
				panels[name].hidden = !selected;
			}
			if (focus) {
				tabs[key].focus();
				tabs[key].scrollIntoView({ block: "nearest", inline: "nearest" });
			}
		};
		groups.forEach(([key, label, fields], index) => {
			const tab = button(label, () => selectTab(key)),
				panel = node("section");
			tab.id = `${id}-${key}-tab`;
			tab.setAttribute("role", "tab");
			tab.setAttribute("aria-controls", `${id}-${key}`);
			panel.id = `${id}-${key}`;
			panel.setAttribute("role", "tabpanel");
			panel.setAttribute("aria-labelledby", tab.id);
			panel.tabIndex = 0;
			panel.append(node("h4", label));
			tabs[key] = tab;
			panels[key] = panel;
			tab.addEventListener(
				"keydown",
				(event) => {
					let next;
					if (event.key === "ArrowRight") next = (index + 1) % groups.length;
					if (event.key === "ArrowLeft")
						next = (index + groups.length - 1) % groups.length;
					if (event.key === "Home") next = 0;
					if (event.key === "End") next = groups.length - 1;
					if (next == null) return;
					event.preventDefault();
					selectTab(groups[next][0], true);
				},
				{ signal }
			);
			for (const name of fields) {
				fieldTabs[name] = key;
				const control = form.fields_dict[name];
				const element = control.$wrapper?.[0] || control.wrapper;
				if (element) panel.append(element);
			}
			nav.append(tab);
			root.append(panel);
		});
		// Original section containers are now empty; all controls retain their
		// native FieldGroup objects and stay inside its event-delegation wrapper.
		if (form.page?.[0]) form.page[0].hidden = true;
		const oldHeading = form.fields_dict.enrollment_payment_section?.$wrapper?.[0];
		if (oldHeading) oldHeading.hidden = true;
		panels.numbering.append(preview);
		selectTab(panels[activeTab] ? activeTab : "general");
		const save = button(
			"Save Settings",
			async () => {
				const settings = form.get_values();
				if (!settings) {
					const missing = Object.values(form.fields_dict).find(
						(field) => field.df.reqd && !field.get_value?.()
					);
					if (missing && fieldTabs[missing.df.fieldname]) {
						selectTab(fieldTabs[missing.df.fieldname]);
						missing.set_focus?.();
					}
					return;
				}
				settings.enrollment_items = (settings.enrollment_items || []).map((row) => ({
					item_code: row.item_code,
					qty: row.qty,
					rate: row.rate,
				}));
				save.disabled = true;
				try {
					const result = await call("save_configuration", {
						settings: {
							...settings,
							modified: configuration.settings.modified,
						},
					});
					if (signal.aborted) return;
					configuration.settings = result;
					frappe.show_alert({
						message: __("Academy settings saved"),
						indicator: "green",
					});
				} finally {
					save.disabled = false;
				}
			},
			true
		);
		wrapper.append(save);
		renderMasters(panels.masters, "Programs", configuration.programs, "program");
		renderMasters(panels.masters, "Groups", configuration.groups, "group");
		host.replaceChildren(wrapper);
	};
	return {
		async mount(options) {
			host = options.container;
			signal = options.signal;
			await render();
		},
		unmount() {
			for (const dialog of dialogs) dialog.hide();
			dialogs.clear();
		},
	};
};
