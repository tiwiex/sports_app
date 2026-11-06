/* Sports-owned linked histories; no change to the shared console shell. */
frappe.provide("frappe.sports_player_profile");
frappe.sports_player_profile.create_tabs = (wrapper, initial = "details", onselect = () => {}) => {
	const tabs = [
		["details", "Player details"],
		["enrollments", "Program enrollments"],
		["finance", "Invoices & receipts"],
		["attendance", "Attendance & fingerprint"],
		["development", "Measurements"],
		["documents", "Documents"],
	];
	const existing = [...wrapper.children].filter(
		(el) =>
			el.tagName !== "STYLE" &&
			!el.classList.contains("player-hero") &&
			!el.classList.contains("player-profile-global-actions")
	);
	const style = document.createElement("style");
	style.textContent = `
	 .sports-profile-tabs{display:flex;gap:6px;overflow-x:auto;max-width:100%;border-bottom:1px solid var(--border-color,#d7e2ed);margin-bottom:18px;padding:2px 0 8px}
	 .sports-profile-tabs [role=tab]{flex:0 0 auto;background:transparent;border:0;border-bottom:3px solid transparent;padding:10px 12px;color:var(--text-muted,#607287);font:inherit;font-weight:600;white-space:nowrap;cursor:pointer}
	 .sports-profile-tabs [aria-selected=true]{border-bottom-color:var(--primary,#176b50);color:var(--text-color,#173042);background:var(--subtle-fg,#f4f8fb);border-radius:6px 6px 0 0}
	 .sports-profile-tabs [role=tab]:focus-visible{outline:2px solid var(--primary,#176b50);outline-offset:-2px}
	 .sports-profile-panel{min-width:0}.sports-profile-panel[hidden]{display:none!important}
	`;
	const nav = document.createElement("div");
	nav.className = "sports-profile-tabs";
	nav.setAttribute("role", "tablist");
	nav.setAttribute("aria-label", __("Player record sections"));
	wrapper.append(style, nav);
	const panels = {},
		buttons = {},
		id = `player-tabs-${crypto.randomUUID()}`;
	const select = (key, focus = false) => {
		for (const [value] of tabs) {
			const selected = value === key;
			buttons[value].setAttribute("aria-selected", String(selected));
			buttons[value].tabIndex = selected ? 0 : -1;
			panels[value].hidden = !selected;
		}
		if (focus) {
			buttons[key].focus();
			buttons[key].scrollIntoView({ block: "nearest", inline: "nearest" });
		}
		onselect(key);
	};
	tabs.forEach(([key, label], index) => {
		const button = document.createElement("button"),
			panel = document.createElement("div");
		button.type = "button";
		button.textContent = __(label);
		button.id = `${id}-${key}-tab`;
		button.setAttribute("role", "tab");
		button.setAttribute("aria-controls", `${id}-${key}`);
		panel.id = `${id}-${key}`;
		panel.className = "sports-profile-panel";
		panel.setAttribute("role", "tabpanel");
		panel.setAttribute("aria-labelledby", button.id);
		panel.dataset.playerTab = key;
		panel.tabIndex = 0;
		panels[key] = panel;
		buttons[key] = button;
		button.addEventListener("click", () => select(key));
		button.addEventListener("keydown", (event) => {
			let next;
			if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
			if (event.key === "ArrowLeft") next = (index + tabs.length - 1) % tabs.length;
			if (event.key === "Home") next = 0;
			if (event.key === "End") next = tabs.length - 1;
			if (next == null) return;
			event.preventDefault();
			select(tabs[next][0], true);
		});
		nav.append(button);
		wrapper.append(panel);
	});
	panels.details.append(...existing);
	const memberships = panels.details.querySelector("[data-player-enrollments]");
	if (memberships) panels.enrollments.append(memberships);
	select(panels[initial] ? initial : "details");
	return panels;
};
frappe.sports_player_profile.mount = async ({
	container,
	name,
	signal,
	panels = {},
	portraitTarget,
}) => {
	const dialogs = new Set();
	const call = async (method, args = {}) =>
		(
			await frappe.call({
				method: `sports_app.${
					method === "add_document" ? "player_documents" : "player_profile"
				}.${method}`,
				args: { name, ...args },
			})
		).message;
	const node = (tag, text, cls) => {
		const el = document.createElement(tag);
		if (text != null) el.textContent = text;
		if (cls) el.className = cls;
		return el;
	};
	const alive = () => !signal.aborted && container.isConnected;
	const button = (label, action) => {
		const el = node("button", __(label), "btn btn-default btn-sm");
		el.type = "button";
		el.addEventListener("click", action, { signal });
		return el;
	};
	const date = (value) =>
		value ? frappe.datetime.str_to_user(String(value).slice(0, 10)) : "—";
	const amount = (value, currency) =>
		`${currency || ""} ${new Intl.NumberFormat(undefined, {
			minimumFractionDigits: 2,
			maximumFractionDigits: 2,
		}).format(Number(value || 0))}`.trim();
	const link = (doctype, id, label = id) => {
		if (!id) return "—";
		const el = node("a", label);
		el.href = `/app/${frappe.router.slug(doctype)}/${encodeURIComponent(id)}`;
		return el;
	};
	const card = (title, target = container) => {
		const el = node("section", null, "player-card sports-profile-history");
		el.append(node("h4", __(title)));
		target.append(el);
		return el;
	};
	const table = (labels, rows) => {
		const wrap = node("div", null, "table-responsive"),
			el = node("table", null, "table table-bordered ing-console-table"),
			head = node("tr"),
			body = node("tbody");
		for (const label of labels) {
			const th = node("th", __(label));
			th.scope = "col";
			head.append(th);
		}
		const thead = node("thead");
		thead.append(head);
		el.append(thead);
		for (const cells of rows) {
			const tr = node("tr");
			for (const value of cells) {
				const td = node("td");
				if (value instanceof Node) td.append(value);
				else td.textContent = value ?? "—";
				tr.append(td);
			}
			body.append(tr);
		}
		el.append(body);
		wrap.append(el);
		return wrap;
	};
	const openDialog = (title, fields, action) => {
		const dialog = new frappe.ui.Dialog({
			title: __(title),
			fields,
			primary_action_label: __("Save"),
			async primary_action(values) {
				if (!alive()) return;
				dialog.get_primary_btn().prop("disabled", true);
				try {
					const saved = await action(values, dialog);
					if (saved !== false && alive()) dialog.hide();
				} finally {
					dialog.get_primary_btn().prop("disabled", false);
				}
			},
		});
		dialogs.add(dialog);
		dialog.show();
		return dialog;
	};
	signal.addEventListener(
		"abort",
		() => {
			for (const dialog of dialogs) dialog.hide();
			dialogs.clear();
		},
		{ once: true }
	);
	const loading = node("p", __("Loading linked player record…"), "text-muted");
	container.append(loading);
	let info;
	try {
		info = await call("overview");
	} catch {
		if (alive())
			loading.textContent = __(
				"Could not load the linked record. Close and reopen the profile to retry."
			);
		return;
	}
	if (!alive()) return;
	container.replaceChildren();
	const overview = card("Player development");
	if (info.portrait) {
		const image = node("img");
		image.src = info.portrait;
		image.alt = __("Player portrait");
		image.style.cssText =
			"width:96px;height:96px;max-width:26vw;object-fit:cover;border-radius:8px;flex-shrink:0";
		(portraitTarget || overview).prepend(image);
	}
	const age = node("p", `${__("Age today")}: ${info.age == null ? "—" : info.age}`),
		foot = node("p", `${__("Preferred foot")}: ${info.preferred_foot || __("Not specified")}`);
	overview.append(age, foot);
	if (info.can_edit_foot)
		overview.append(
			button("Update preferred foot", () =>
				openDialog(
					"Update preferred foot",
					[
						{
							fieldname: "preferred_foot",
							label: __("Preferred foot"),
							fieldtype: "Select",
							options: "\nLeft\nRight\nBoth\nNot specified",
							default: info.preferred_foot || "",
						},
					],
					async (values) => {
						info.modified = await call("save_preferred_foot", {
							preferred_foot: values.preferred_foot,
							modified: info.modified,
						});
						if (alive()) {
							info.preferred_foot = values.preferred_foot;
							foot.textContent = `${__("Preferred foot")}: ${
								info.preferred_foot || __("Not specified")
							}`;
						}
					}
				)
			)
		);
	if (info.available.invoices) {
		const balance = card("Outstanding by invoice currency", panels.finance);
		if (info.outstanding?.length)
			balance.append(
				table(
					["Currency", "Outstanding"],
					info.outstanding.map((row) => [
						row.currency,
						amount(row.outstanding, row.currency),
					])
				)
			);
		else
			balance.append(
				node("p", __("No posted outstanding invoices to display."), "text-muted")
			);
		balance.append(
			node(
				"p",
				__(
					"Submitted ERPNext invoices only. Drafts and cancelled invoices are excluded; currencies are shown separately."
				),
				"text-muted"
			)
		);
	}
	const definitions = {
		invoices: {
			title: "Invoices",
			labels: ["Invoice", "Posting date", "Due date", "Amount", "Outstanding", "Status"],
			cells: (r) => [
				link("Sales Invoice", r.name),
				date(r.posting_date),
				date(r.due_date),
				amount(r.grand_total, r.currency),
				amount(r.outstanding_amount, r.currency),
				r.docstatus === 0 ? __("Draft") : r.docstatus === 2 ? __("Cancelled") : r.status,
			],
		},
		receipts: {
			title: "Payments and receipts",
			labels: [
				"Payment",
				"Posting date",
				"Type",
				"Paid",
				"Received",
				"Bank reference",
				"Status",
			],
			cells: (r) => [
				link("Payment Entry", r.name),
				date(r.posting_date),
				r.payment_type,
				amount(r.paid_amount, r.paid_from_account_currency),
				amount(r.received_amount, r.paid_to_account_currency),
				r.reference_no || "—",
				r.docstatus === 1
					? __("Submitted")
					: r.docstatus === 2
					? __("Cancelled")
					: __("Draft"),
			],
		},
		attendance: {
			title: "Attendance history",
			labels: ["Attendance", "Session", "Date", "Session status", "Result", "Source"],
			cells: (r) => [
				link("Sports Attendance", r.name),
				r.session
					? link("Sports Session", r.session, r.session_title)
					: __("Restricted session"),
				date(r.session_date),
				r.session_status || "—",
				r.status,
				r.source,
			],
		},
		biometrics: {
			title: "Fingerprint preparation",
			labels: ["Reference", "Status", "Finger", "Prepared on", "Demo reference"],
			cells: (r) => [
				link("Sports Biometric Enrollment", r.name),
				r.status,
				r.finger,
				date(r.prepared_on),
				r.demo_reference ? `${r.demo_reference} (${__("simulated")})` : "—",
			],
		},
		measurements: {
			title: "Height and weight history",
			labels: ["Reference", "Assessed on", "Height (cm)", "Weight (kg)", "Recorded by"],
			cells: (r) => [
				link("Sports Player Measurement", r.name),
				date(r.assessed_on),
				r.height_cm > 0 ? r.height_cm : "—",
				r.weight_kg > 0 ? r.weight_kg : "—",
				r.recorded_by,
			],
		},
		documents: {
			title: "Private supporting documents",
			labels: ["Reference", "Title", "Type", "Document date", "File"],
			cells: (r) => {
				let file = "—";
				if (r.file_url?.startsWith("/private/files/")) {
					file = node("a", __("View private document"));
					file.href = r.file_url;
					file.target = "_blank";
					file.rel = "noopener noreferrer";
				}
				return [
					link("Sports Player Document", r.name),
					r.title,
					r.document_type,
					date(r.document_date),
					file,
				];
			},
		},
	};
	const readFile = (file) =>
		new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.onload = () => resolve(reader.result);
			reader.onerror = () => reject(Error("Could not read file"));
			reader.readAsDataURL(file);
		});
	const load = [];
	for (const [section, definition] of Object.entries(definitions)) {
		const target = {
			invoices: panels.finance,
			receipts: panels.finance,
			attendance: panels.attendance,
			biometrics: panels.attendance,
			measurements: panels.development,
			documents: panels.documents,
		};
		const area = card(definition.title, target[section]);
		area.dataset.history = section;
		if (!info.available[section]) {
			area.append(
				node(
					"p",
					__("Restricted — your current permissions do not allow this history."),
					"text-muted"
				)
			);
			continue;
		}
		let offset = 0,
			generation = 0;
		const actions = node("div", null, "player-actions"),
			body = node("div");
		area.append(actions, body);
		const refresh = async () => {
			const version = ++generation;
			const requested = offset;
			try {
				const result = await call("history", { section, start: requested });
				if (!alive() || version !== generation) return;
				body.replaceChildren();
				if (result.rows.length)
					body.append(table(definition.labels, result.rows.map(definition.cells)));
				else body.append(node("p", __("No records on this page."), "text-muted"));
				const pages = node("div", null, "player-actions");
				if (offset)
					pages.append(
						button("Previous", () => {
							offset = Math.max(0, offset - 20);
							refresh();
						})
					);
				if (result.has_more)
					pages.append(
						button("More", () => {
							offset += 20;
							refresh();
						})
					);
				body.append(pages);
			} catch {
				if (alive() && version === generation)
					body.replaceChildren(
						node(
							"p",
							__("History could not be loaded. Retry or reopen the profile."),
							"text-muted"
						),
						button("Retry", refresh)
					);
			}
		};
		if (section === "measurements" && info.can_add_measurement)
			actions.append(
				button("Add measurement", () => {
					const key = crypto.randomUUID();
					openDialog(
						"Add dated measurement",
						[
							{
								fieldname: "assessed_on",
								label: __("Assessed on"),
								fieldtype: "Date",
								reqd: 1,
								default: info.today,
							},
							{
								fieldname: "height_cm",
								label: __("Height (cm)"),
								fieldtype: "Float",
							},
							{
								fieldname: "weight_kg",
								label: __("Weight (kg)"),
								fieldtype: "Float",
							},
						],
						async (values) => {
							await call("add_measurement", { ...values, request_key: key });
							offset = 0;
							await refresh();
						}
					);
				})
			);
		if (section === "documents" && info.can_add_document)
			actions.append(
				button("Add private document", () => {
					const key = crypto.randomUUID();
					const dialog = openDialog(
						"Add private supporting document",
						[
							{ fieldname: "title", label: __("Title"), fieldtype: "Data", reqd: 1 },
							{
								fieldname: "document_type",
								label: __("Document type"),
								fieldtype: "Select",
								options: "Birth certificate\nMedical report\nOther",
								reqd: 1,
								default: "Birth certificate",
							},
							{
								fieldname: "document_date",
								label: __("Document date"),
								fieldtype: "Date",
							},
							{ fieldname: "file_picker", fieldtype: "HTML" },
						],
						async (values) => {
							const file = input.files[0];
							if (!file) {
								frappe.msgprint(__("Choose a document file."));
								return false;
							}
							if (file.size > 5 * 1024 * 1024) {
								frappe.msgprint(__("Choose a document no larger than 5 MB."));
								return false;
							}
							const data = await readFile(file);
							if (!alive()) return;
							await call("add_document", {
								...values,
								file_data: data,
								request_key: key,
							});
							offset = 0;
							await refresh();
						}
					);
					const input = node("input");
					input.type = "file";
					input.accept = "application/pdf,image/jpeg,image/png,image/webp";
					input.setAttribute("aria-label", __("Private supporting file"));
					dialog.fields_dict.file_picker.$wrapper.append(input);
				})
			);
		load.push(refresh());
	}
	await Promise.allSettled(load);
};
