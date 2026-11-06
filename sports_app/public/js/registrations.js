/* Sports-owned private intake queue in the optional Boost host. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:registrations"] = () => {
	let liveSnapshot;
	let host,
		signal,
		status = "Pending",
		offset = 0,
		generation = 0,
		sortBy = "submitted_on",
		sortOrder = "desc",
		detailDialog;
	const lifecycle = new AbortController();
	const dialogs = new Set();
	const call = async (method, args = {}) =>
		(
			await frappe.call({
				method: `sports_app.registrations_api.${method}`,
				args,
			})
		).message;
	const node = (tag, text, cls) => {
		const el = document.createElement(tag);
		if (text != null) el.textContent = text;
		if (cls) el.className = cls;
		return el;
	};
	const button = (text, action, primary = false) => {
		const el = node("button", __(text), `btn btn-${primary ? "primary" : "default"} btn-sm`);
		el.type = "button";
		el.addEventListener("click", action, { signal });
		return el;
	};
	const link = (doctype, name, text = name) => {
		const el = node("a", text);
		el.href = `/app/${frappe.router.slug(doctype)}/${encodeURIComponent(name)}`;
		return el;
	};
	const closeMenus = () => {
		host.querySelectorAll(".sports-registration-menu").forEach((menu) => {
			menu.classList.remove("is-open");
			menu.querySelector("button").setAttribute("aria-expanded", "false");
			menu.querySelector(".dropdown-menu").removeAttribute("style");
		});
	};
	const formatDate = (value) =>
		value && frappe.datetime.str_to_user
			? frappe.datetime.str_to_user(String(value).split(".")[0])
			: value || "—";
	async function changed(name) {
		if (signal.aborted) return;
		await render();
		if (!signal.aborted) await show(name);
	}
	async function accept(record, matches = []) {
		const dialog = new frappe.ui.Dialog({
			title: __("Accept enrollment"),
			fields: [
				{
					fieldname: "program",
					label: __("Program"),
					fieldtype: "Link",
					options: "Sports Program",
					reqd: 1,
					default: record.program,
					get_query: () => ({
						filters: { company: record.company, enabled: 1 },
					}),
				},
				{
					fieldname: "group",
					label: __("Group"),
					fieldtype: "Link",
					options: "Sports Group",
					get_query: () => ({
						filters: {
							company: record.company,
							program: dialog.get_value("program"),
							enabled: 1,
						},
					}),
				},
				{
					fieldname: "start_date",
					label: __("Start date"),
					fieldtype: "Date",
					reqd: 1,
					default: frappe.datetime.get_today(),
				},
				{
					fieldname: "status",
					label: __("Enrollment status"),
					fieldtype: "Select",
					options: "Pending\nActive",
					default: "Pending",
					reqd: 1,
				},
				{ fieldname: "review_notice", fieldtype: "HTML" },
			],
			primary_action_label: __(
				record.sales_invoice ? "Accept and confirm payment" : "Accept and create player"
			),
			async primary_action(values) {
				dialog.get_primary_btn().prop("disabled", true);
				try {
					await call("accept_registration", {
						name: record.name,
						enrollment: values,
					});
					dialog.hide();
					await changed(record.name);
				} finally {
					dialog.get_primary_btn().prop("disabled", false);
				}
			},
		});
		const notice = node(
			"div",
			__(
				"Review possible player matches before admitting this applicant. Acceptance adds the player to the selected program. For a linked invoice, confirm you have verified the transfer: this action submits the invoice and records its payment."
			),
			"text-muted"
		);
		if (matches.length) {
			notice.append(node("h5", __("Possible existing players")));
			for (const match of matches)
				notice.append(
					node("p", `${match.name} · ${match.full_name} · ${match.birth_date || ""}`)
				);
		}
		dialog.fields_dict.review_notice.$wrapper.append(notice);
		dialog.fields_dict.program.df.onchange = () => dialog.set_value("group", "");
		dialogs.add(dialog);
		dialog.show();
	}
	async function reject(record) {
		const dialog = new frappe.ui.Dialog({
			title: __("Reject enrollment"),
			fields: [
				{
					fieldname: "reason",
					label: __("Reason"),
					fieldtype: "Small Text",
					reqd: 1,
				},
			],
			primary_action_label: __("Reject enrollment"),
			async primary_action(values) {
				dialog.get_primary_btn().prop("disabled", true);
				try {
					await call("reject_registration", {
						name: record.name,
						reason: values.reason,
					});
					dialog.hide();
					await changed(record.name);
				} finally {
					dialog.get_primary_btn().prop("disabled", false);
				}
			},
		});
		dialogs.add(dialog);
		dialog.show();
	}
	async function show(name) {
		const current = ++generation,
			data = await call("get_registration", { name });
		if (signal.aborted || current !== generation) return;
		const r = data.registration,
			wrap = node("section", null, "sports-enrollment-profile");
		const style = node("style");
		style.textContent = `
   .sports-enrollment-profile{color:var(--text-color,#173042);font-size:14px;line-height:1.5}
   .sports-enrollment-profile .enrollment-hero{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:18px}
   .sports-enrollment-profile .enrollment-hero h3{margin:3px 0 5px;font-size:24px;overflow-wrap:anywhere}
   .sports-enrollment-profile .enrollment-eyebrow{color:var(--text-muted,#607287);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em}
   .sports-enrollment-profile .enrollment-card{border:1px solid var(--border-color,#d7e2ed);border-radius:8px;padding:18px;margin-bottom:16px;background:var(--card-bg,#fff)}
   .sports-enrollment-profile .enrollment-card h4{font-size:15px;margin:0 0 14px;font-weight:700}
   .sports-enrollment-profile .enrollment-summary{background:var(--subtle-fg,#f4f8fb)}
   .sports-enrollment-profile .enrollment-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 24px;margin:0}
   .sports-enrollment-profile .enrollment-field{min-width:0}
   .sports-enrollment-profile .enrollment-field.is-wide{grid-column:1/-1}
   .sports-enrollment-profile dt{font-size:12px;font-weight:500;color:var(--text-muted,#607287);margin-bottom:4px}
   .sports-enrollment-profile dd{font-size:14px;font-weight:500;margin:0;white-space:pre-wrap;overflow-wrap:anywhere}
   .sports-enrollment-profile a{overflow-wrap:anywhere}
   .sports-enrollment-profile .enrollment-actions{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
   .sports-enrollment-profile .enrollment-note{margin:0;color:var(--text-muted,#607287);font-size:13px}
   .sports-enrollment-profile .enrollment-matches{margin:0;padding-left:18px}
   .sports-enrollment-profile .enrollment-rejection{border-left:3px solid #dc2626}
   @media(max-width:640px){.sports-enrollment-profile .enrollment-grid{grid-template-columns:minmax(0,1fr)}.sports-enrollment-profile .enrollment-card{padding:14px}.sports-enrollment-profile .enrollment-hero{flex-wrap:wrap}.sports-enrollment-profile .enrollment-hero h3{font-size:21px}}
  `;
		wrap.append(style);
		const card = (title, extra = "") => {
			const section = node("section", null, `enrollment-card ${extra}`);
			section.append(node("h4", __(title)));
			wrap.append(section);
			return section;
		};
		const grid = (section) => {
			const dl = node("dl", null, "enrollment-grid");
			section.append(dl);
			return dl;
		};
		const field = (dl, label, value, wide = false) => {
			const cell = node("div", null, `enrollment-field${wide ? " is-wide" : ""}`),
				dd = node("dd");
			if (value instanceof Node) dd.append(value);
			else dd.textContent = value == null || value === "" ? "—" : value;
			cell.append(node("dt", __(label)), dd);
			dl.append(cell);
		};
		const chip = node("span", __(r.status), "ing-console-status-chip");
		chip.classList.add(
			r.status === "Accepted"
				? "is-approved"
				: r.status === "Rejected"
				? "is-cancelled"
				: "is-pending-review"
		);
		const hero = node("header", null, "enrollment-hero"),
			identity = node("div");
		identity.append(
			node("div", __("Enrollment application"), "enrollment-eyebrow"),
			node("h3", r.full_name)
		);
		hero.append(identity, chip);
		if (r.player_photo && r.player_photo.startsWith("/private/files/")) {
			const photo = node("img");
			photo.src = r.player_photo;
			photo.alt = __("Player photograph");
			photo.style.cssText = "width:96px;height:96px;object-fit:cover;border-radius:8px";
			identity.append(photo);
		}
		wrap.append(hero);
		const summary = grid(card("Application summary", "enrollment-summary"));
		field(summary, "Enrollment reference", r.name);
		field(summary, "Submitted on", formatDate(r.submitted_on));
		field(summary, "Requested pathway", r.requested_pathway);
		field(summary, "Academy company", r.company);
		if (r.status === "Pending") {
			const review = card("Admission review");
			if (data.can_review) {
				const actions = node("div", null, "enrollment-actions");
				actions.append(
					...(data.can_accept
						? [
								button(
									"Accept enrollment",
									() => accept(r, data.possible_matches),
									true
								),
						  ]
						: []),
					button("Reject enrollment", () => reject(r)),
					link("Sports Registration", r.name, __("Edit enrollment details"))
				);
				review.append(actions);
			}
			review.append(
				node(
					"p",
					__(
						"Review the application and any possible player matches before accepting. Accepting an application with a linked invoice also confirms its payment. Draft invoices must first be reported paid; Finance approval permissions are required."
					),
					"enrollment-note"
				)
			);
			if (data.possible_matches.length) {
				const matches = node("ul", null, "enrollment-matches");
				review.append(node("h5", __("Possible existing players")));
				for (const row of data.possible_matches) {
					const li = node("li");
					li.append(
						link(
							"Sports Player",
							row.name,
							`${row.full_name} · ${row.name} · ${row.birth_date || ""}`
						)
					);
					matches.append(li);
				}
				review.append(matches);
			}
		}
		if (r.player)
			field(
				grid(card("Player record")),
				"Accepted player",
				link("Sports Player", r.player, r.full_name || r.player)
			);
		if (r.rejection_reason) {
			const reason = card("Rejection reason", "enrollment-rejection");
			field(grid(reason), "Reason", r.rejection_reason, true);
		}
		const billing = card("Billing and payment");
		if (!data.invoice && !data.payment)
			billing.append(
				node(
					"p",
					__("No invoice or receipt is linked to this application."),
					"enrollment-note"
				)
			);
		if (data.invoice) {
			const invoice = data.invoice,
				values = grid(billing);
			field(
				values,
				"Invoice reference",
				frappe.model.can_read("Sales Invoice")
					? link("Sales Invoice", invoice.name)
					: invoice.name
			);
			field(values, "Invoice review status", invoice.workflow_state);
			field(
				values,
				"Posting status",
				invoice.docstatus === 1
					? __("Submitted")
					: invoice.docstatus === 2
					? __("Cancelled")
					: __("Not posted")
			);
			field(
				values,
				"Payment status",
				invoice.docstatus === 2
					? __("Cancelled")
					: invoice.docstatus === 1 && Number(invoice.outstanding_amount) === 0
					? __("Paid")
					: __("Awaiting Finance confirmation")
			);
		}
		if (data.payment) {
			const payment = data.payment,
				values = grid(billing);
			values.style.marginTop = data.invoice ? "16px" : "0";
			field(
				values,
				"Receipt reference",
				frappe.model.can_read("Payment Entry")
					? link("Payment Entry", payment.name)
					: payment.name
			);
			field(
				values,
				"Receipt status",
				payment.docstatus === 1
					? __("Submitted")
					: payment.docstatus === 2
					? __("Cancelled")
					: payment.workflow_state || __("Not posted")
			);
		}
		let values;
		for (const item of data.fields) {
			if (item.fieldtype === "Section Break") {
				values = grid(card(item.label === "The player" ? "Player details" : item.label));
				continue;
			}
			if (!values) values = grid(card("Player details"));
			const value =
				item.fieldtype === "Check"
					? r[item.fieldname]
						? __("Yes")
						: __("No")
					: r[item.fieldname];
			field(values, item.label, value, item.fieldtype === "Small Text");
		}
		if (detailDialog) detailDialog.hide();
		detailDialog = new frappe.ui.Dialog({
			title: __("Enrollment: {0}", [r.name]),
			size: "extra-large",
			fields: [{ fieldname: "registration_view", fieldtype: "HTML" }],
		});
		detailDialog.fields_dict.registration_view.$wrapper.append(wrap);
		dialogs.add(detailDialog);
		detailDialog.show();
	}
	async function reviewAction(name, action) {
		const current = ++generation,
			data = await call("get_registration", { name });
		if (signal.aborted || current !== generation) return;
		if (
			!data.can_review ||
			(action === "accept" && !data.can_accept) ||
			data.registration.status !== "Pending"
		) {
			await render();
			frappe.msgprint(
				__(
					"This enrollment application is no longer available for review. Refresh and view its current status."
				)
			);
			return;
		}
		if (action === "accept") await accept(data.registration, data.possible_matches);
		else await reject(data.registration);
	}
	function referenceMenu(row) {
		const menu = node("div", null, "ing-console-action-menu sports-registration-menu");
		const toggle = button(row.name, (event) => {
			event.preventDefault();
			event.stopPropagation();
			const wasOpen = menu.classList.contains("is-open");
			closeMenus();
			if (wasOpen) return;
			menu.classList.add("is-open");
			toggle.setAttribute("aria-expanded", "true");
			const rect = toggle.getBoundingClientRect(),
				width = Math.max(list.getBoundingClientRect().width, 170);
			list.style.cssText = `position:fixed;left:${Math.max(
				8,
				Math.min(rect.left, innerWidth - width - 8)
			)}px;top:${Math.max(
				8,
				Math.min(rect.bottom + 4, innerHeight - list.getBoundingClientRect().height - 8)
			)}px;z-index:9999`;
		});
		toggle.classList.add(
			"ing-console-action-menu-toggle",
			"ing-console-action-menu-toggle-name"
		);
		toggle.setAttribute("aria-haspopup", "menu");
		toggle.setAttribute("aria-expanded", "false");
		toggle.setAttribute("aria-label", __("Actions for enrollment {0}", [row.name]));
		toggle.append(node("span", "▾", "ing-console-action-caret"));
		const list = node("ul", null, "dropdown-menu");
		list.setAttribute("role", "menu");
		const add = (label, action, danger = false) => {
			const li = node("li"),
				item = button(label, (event) => {
					event.preventDefault();
					event.stopPropagation();
					closeMenus();
					action();
				});
			item.className = `dropdown-item${danger ? " text-danger" : ""}`;
			item.setAttribute("role", "menuitem");
			item.style.cssText = "border:0;background:transparent;width:100%;text-align:left";
			li.append(item);
			list.append(li);
		};
		add("View", () => show(row.name));
		if (row.status === "Pending" && row.can_review) {
			if (row.can_accept) add("Accept enrollment", () => reviewAction(row.name, "accept"));
			add("Reject enrollment", () => reviewAction(row.name, "reject"), true);
		}
		toggle.addEventListener(
			"keydown",
			(event) => {
				if (event.key === "ArrowDown") {
					event.preventDefault();
					if (!menu.classList.contains("is-open")) toggle.click();
					list.querySelector("button").focus();
				}
			},
			{ signal }
		);
		list.addEventListener(
			"keydown",
			(event) => {
				const items = [...list.querySelectorAll("button")],
					index = items.indexOf(document.activeElement);
				if (["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) {
					event.preventDefault();
					items[
						event.key === "Home"
							? 0
							: event.key === "End"
							? items.length - 1
							: (index + (event.key === "ArrowDown" ? 1 : -1) + items.length) %
							  items.length
					].focus();
				}
			},
			{ signal }
		);
		menu.append(toggle, list);
		return menu;
	}
	async function render(options = {}) {
		const background = options.background === true;
		const canApply = options.canApply || (() => true);
		if (!background) closeMenus();
		const current = background ? generation : ++generation,
			rows = await call("list_registrations", {
				status,
				start: offset,
				sort_by: sortBy,
				sort_order: sortOrder,
			});
		if (signal.aborted || current !== generation || !canApply()) return false;
		const snapshot = JSON.stringify(rows);
		if (background && snapshot === liveSnapshot) return;
		liveSnapshot = snapshot;
		const wrap = node("section");
		wrap.append(
			node("h3", __("Enrollments")),
			node(
				"p",
				__("Review applications and manage admission without leaving the console."),
				"text-muted"
			)
		);
		const label = node("label", __("Enrollment status"));
		label.htmlFor = "sports-registration-status";
		const select = node("select", null, "form-control");
		select.id = label.htmlFor;
		for (const value of ["Pending", "Accepted", "Rejected"]) {
			const option = node("option", __(value));
			option.value = value;
			select.append(option);
		}
		select.value = status;
		select.addEventListener(
			"change",
			() => {
				status = select.value;
				offset = 0;
				render();
			},
			{ signal }
		);
		const controls = node("div");
		controls.style.cssText =
			"display:flex;flex-wrap:wrap;align-items:end;gap:12px;margin-bottom:16px";
		const filter = node("div");
		filter.append(label, select);
		controls.append(filter, button("Refresh enrollments", render));
		wrap.append(controls);
		const tableWrap = node("div", null, "ing-console-table-wrap"),
			table = node("table", null, "table table-bordered ing-console-table");
		tableWrap.style.maxHeight = "65vh";
		const head = node("thead"),
			heading = node("tr");
		for (const [text, field] of [
			["Reference", "name"],
			["Player", "full_name"],
			["Pathway", "requested_pathway"],
			["Submitted on", "submitted_on"],
			["Status", "status"],
		]) {
			const th = node("th");
			th.scope = "col";
			th.setAttribute(
				"aria-sort",
				sortBy === field ? (sortOrder === "asc" ? "ascending" : "descending") : "none"
			);
			const sort = button(text, () => {
				sortOrder = sortBy === field && sortOrder === "asc" ? "desc" : "asc";
				sortBy = field;
				offset = 0;
				render();
			});
			sort.setAttribute("aria-label", __("Sort by {0}", [__(text)]));
			sort.style.cssText =
				"font:inherit;color:inherit;border:0;background:transparent;padding:0;white-space:nowrap";
			sort.append(
				node(
					"span",
					sortBy === field ? (sortOrder === "asc" ? " ↑" : " ↓") : " ↕",
					"text-muted"
				)
			);
			th.append(sort);
			heading.append(th);
		}
		for (const title of ["Invoice", "Invoice workflow"]) heading.append(node("th", __(title)));
		head.append(heading);
		table.append(head);
		const body = node("tbody");
		for (const row of rows) {
			const tr = node("tr"),
				ref = node("td");
			ref.append(referenceMenu(row));
			tr.append(ref);
			for (const key of ["full_name", "requested_pathway", "submitted_on"])
				tr.append(node("td", key === "submitted_on" ? formatDate(row[key]) : row[key]));
			const state = node("td"),
				chip = node("span", __(row.status), "ing-console-status-chip");
			chip.classList.add(
				row.status === "Accepted"
					? "is-approved"
					: row.status === "Rejected"
					? "is-cancelled"
					: "is-pending-review"
			);
			state.append(chip);
			tr.append(
				state,
				node("td", row.sales_invoice || "—"),
				node("td", row.invoice_workflow || "—")
			);
			body.append(tr);
		}
		table.append(body);
		tableWrap.append(table);
		wrap.append(tableWrap);
		if (!rows.length) wrap.append(node("p", __("No enrollments on this page."), "text-muted"));
		if (offset)
			wrap.append(
				button("Previous enrollments", () => {
					offset = Math.max(0, offset - 20);
					render();
				})
			);
		if (rows.length === 20)
			wrap.append(
				button("More enrollments", () => {
					offset += 20;
					render();
				})
			);
		host.replaceChildren(wrap);
	}
	return {
		async mount(options) {
			host = options.container;
			signal = lifecycle.signal;
			if (options.signal.aborted) {
				lifecycle.abort();
				return;
			}
			options.signal.addEventListener("abort", () => lifecycle.abort(), {
				once: true,
				signal,
			});
			document.addEventListener("click", closeMenus, { signal });
			document.addEventListener(
				"keydown",
				(event) => {
					if (event.key === "Escape") {
						const open = host.querySelector(
							".sports-registration-menu.is-open > button"
						);
						closeMenus();
						if (open) open.focus();
					}
				},
				{ signal }
			);
			window.addEventListener("resize", closeMenus, { signal });
			host.addEventListener("scroll", closeMenus, { capture: true, signal });
			await render();
			options.watch?.({
				doctypes: [
					"Sports Registration",
					"Sports Player",
					"Sales Invoice",
					"Payment Entry",
				],
				refresh: ({ canApply }) => render({ background: true, canApply }),
			});
		},
		unmount() {
			generation++;
			closeMenus();
			lifecycle.abort();
			for (const dialog of dialogs) dialog.hide();
			dialogs.clear();
		},
	};
};
