/* Sports-owned scholarship decisions, fee plans and monthly receivables. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:billing"] = () => {
	const lifecycle = new AbortController(),
		dialogs = new Set();
	let host,
		config,
		section = "overview",
		offset = 0,
		month = "",
		program = "",
		version = 0;
	const subscriptionState = { year: "", search: "" };
	const node = (tag, text, cls) => {
		const el = document.createElement(tag);
		if (text != null) el.textContent = text;
		if (cls) el.className = cls;
		return el;
	};
	const alive = () => !lifecycle.signal.aborted;
	const call = async (method, args = {}) =>
		(await frappe.call({ method: `sports_app.${method}`, args })).message;
	const button = (label, action) => {
		const el = node("button", __(label), "btn btn-default btn-sm");
		el.type = "button";
		el.addEventListener("click", action, { signal: lifecycle.signal });
		return el;
	};
	const link = (doctype, id) => {
		if (!id) return "—";
		const el = node("a", id);
		el.href = `/app/${frappe.router.slug(doctype)}/${encodeURIComponent(id)}`;
		return el;
	};
	const table = (labels, rows) => {
		const wrap = node("div", null, "table-responsive"),
			el = node("table", null, "table table-bordered ing-console-table"),
			head = node("thead"),
			tr = node("tr"),
			body = node("tbody");
		for (const label of labels) {
			const th = node("th", __(label));
			th.scope = "col";
			tr.append(th);
		}
		head.append(tr);
		for (const row of rows) {
			const line = node("tr");
			for (const value of row) {
				const td = node("td");
				if (value instanceof Node) td.append(value);
				else td.textContent = value ?? "—";
				line.append(td);
			}
			body.append(line);
		}
		el.append(head, body);
		wrap.append(el);
		return wrap;
	};
	const money = (value, currency) =>
		`${currency} ${Number(value || 0).toLocaleString(undefined, {
			minimumFractionDigits: 2,
			maximumFractionDigits: 2,
		})}`;
	const dialog = (title, fields, action) => {
		const d = new frappe.ui.Dialog({
			title: __(title),
			fields,
			primary_action_label: action ? __("Save") : undefined,
			primary_action: action
				? async (values) => {
						if (!alive()) return;
						d.get_primary_btn().prop("disabled", true);
						try {
							await action(values);
							if (alive()) {
								d.hide();
								await render();
							}
						} finally {
							d.get_primary_btn().prop("disabled", false);
						}
				  }
				: undefined,
		});
		dialogs.add(d);
		d.show();
		return d;
	};
	const planFields = (row = {}) =>
		[
			{
				fieldname: "title",
				label: __("Plan name"),
				fieldtype: "Data",
				reqd: 1,
			},
			{
				fieldname: "program",
				label: __("Program"),
				fieldtype: "Link",
				options: "Sports Program",
				reqd: 1,
				get_query: () => ({ filters: { company: config.company, enabled: 1 } }),
			},
			{
				fieldname: "enabled",
				label: __("Enabled"),
				fieldtype: "Check",
				default: 1,
			},
			{
				fieldname: "effective_from",
				label: __("Effective from"),
				fieldtype: "Date",
				reqd: 1,
				default: month + "-01",
			},
			{
				fieldname: "effective_to",
				label: __("Effective to"),
				fieldtype: "Date",
			},
			{
				fieldname: "currency",
				label: __("Currency"),
				fieldtype: "Link",
				options: "Currency",
				reqd: 1,
				default: config.currency,
			},
			{
				fieldname: "monthly_amount",
				label: __("Monthly amount"),
				fieldtype: "Currency",
				reqd: 1,
				default: config.default_monthly_fee,
			},
			{
				fieldname: "joining_policy",
				label: __("Eligibility policy"),
				fieldtype: "Select",
				options: "\nFull fee if active at month start",
				reqd: 1,
			},
			{
				fieldname: "due_day",
				label: __("Due day (1–28)"),
				fieldtype: "Int",
				reqd: 1,
			},
			{
				fieldname: "item",
				label: __("Service item"),
				fieldtype: "Link",
				options: "Item",
				reqd: 1,
				get_query: () => ({
					filters: { is_stock_item: 0, is_sales_item: 1, disabled: 0 },
				}),
			},
			{
				fieldname: "income_account",
				label: __("Income account"),
				fieldtype: "Link",
				options: "Account",
				reqd: 1,
				get_query: () => ({
					filters: {
						company: config.company,
						root_type: "Income",
						is_group: 0,
						disabled: 0,
					},
				}),
			},
			{
				fieldname: "cost_center",
				label: __("Cost center"),
				fieldtype: "Link",
				options: "Cost Center",
				reqd: 1,
				get_query: () => ({
					filters: { company: config.company, is_group: 0, disabled: 0 },
				}),
			},
		].map((f) => ({
			...f,
			default: row[f.fieldname] ?? f.default,
			read_only: !config.can_manage,
		}));
	const editPlan = (row) => {
		let editor;
		const fields = planFields(row);
		fields.splice(
			fields.findIndex((f) => f.fieldname === "monthly_amount"),
			0,
			{
				fieldname: "subscription_plan",
				label: __("ERPNext Subscription Plan"),
				fieldtype: "Link",
				options: "Subscription Plan",
				description: __(
					"Optional: use the Item and current monthly Fixed Rate from this ERPNext plan. Monthly invoices are submitted through the configured billing schedule."
				),
				default: row?.subscription_plan,
				read_only: !config.can_manage,
				get_query: () => ({
					filters: {
						billing_interval: "Month",
						billing_interval_count: 1,
						price_determination: "Fixed Rate",
						currency: config.currency,
					},
				}),
				async onchange() {
					const name = editor?.get_value("subscription_plan");
					if (!name) return;
					const pricing = await call("subscription_pricing.plan_details", {
						name,
					});
					if (alive() && editor.get_value("subscription_plan") === name)
						await editor.set_values({
							item: pricing.item,
							monthly_amount: pricing.monthly_amount,
							currency: pricing.currency,
						});
				},
			}
		);
		editor = dialog(
			row ? "Fee plan" : "New fee plan",
			fields,
			config.can_manage
				? (values) =>
						call("fee_plans.save", {
							values,
							name: row?.name,
							modified: row?.modified,
						})
				: null
		);
		return editor;
	};
	const newDecision = () =>
		dialog(
			"New scholarship decision",
			[
				{
					fieldname: "enrollment",
					label: __("Program enrollment"),
					fieldtype: "Link",
					options: "Sports Enrollment",
					reqd: 1,
					get_query: () => ({ filters: { company: config.company } }),
				},
				{
					fieldname: "effective_from",
					label: __("Effective from"),
					fieldtype: "Date",
					reqd: 1,
				},
				{
					fieldname: "effective_to",
					label: __("Effective to"),
					fieldtype: "Date",
				},
				{
					fieldname: "coverage_type",
					label: __("Monthly fee coverage"),
					fieldtype: "Select",
					options: "Full\nPercentage\nFixed amount",
					default: "Full",
					reqd: 1,
				},
				{
					fieldname: "coverage_value",
					label: __("Percentage or fixed amount"),
					fieldtype: "Currency",
				},
				{
					fieldname: "reason",
					label: __("Confidential decision reason"),
					fieldtype: "Small Text",
					reqd: 1,
				},
				...["kit_benefit", "trip_benefit", "trial_benefit", "tournament_benefit"].map(
					(fieldname) => ({
						fieldname,
						label: __(fieldname.replaceAll("_", " ")),
						fieldtype: "Check",
					})
				),
			],
			(values) => call("scholarships.create", { values })
		);
	const viewDecision = async (row) => {
		const detail = await call("billing_api.decision", { name: row.name });
		if (!alive()) return;
		dialog(
			"Scholarship decision",
			Object.entries(detail)
				.filter(([k]) => !["modified", "docstatus"].includes(k))
				.map(([key, value]) => ({
					fieldname: key,
					label: __(key.replaceAll("_", " ")),
					fieldtype: ["reason", "revocation_reason"].includes(key)
						? "Small Text"
						: "Data",
					default: value ?? "",
					read_only: 1,
				}))
		);
	};
	const transition = (row, action) =>
		dialog(
			action + " scholarship",
			[
				{
					fieldname: "reason",
					label: __("Reason for revocation"),
					fieldtype: "Small Text",
					reqd: action === "Revoke",
					hidden: action !== "Revoke",
				},
			],
			(values) =>
				call("scholarships.transition", {
					name: row.name,
					action,
					modified: row.modified,
					reason: values.reason || "",
				})
		);
	const reference = (row) => {
		const details = node("details"),
			summary = node("summary", row.name);
		summary.style.cursor = "pointer";
		details.append(
			summary,
			button("View", () => viewDecision(row))
		);
		if (config.can_manage && row.docstatus !== 2)
			details.append(
				button(row.docstatus === 0 ? "Approve" : "Revoke", () =>
					transition(row, row.docstatus === 0 ? "Approve" : "Revoke")
				)
			);
		return details;
	};
	async function render(options = {}) {
		try {
			await draw(options);
		} catch {
			if (alive())
				host.replaceChildren(
					node(
						"p",
						__("Billing could not be loaded. Check your access and reopen the view."),
						"text-muted"
					)
				);
		}
	}
	async function draw({ canApply = () => true } = {}) {
		const generation = ++version;
		config = await call("billing_api.configuration");
		if (!alive() || generation !== version || !canApply()) return;
		if (!month) month = config.current_month;
		const wrapper = node("section", null, "sports-billing-view"),
			style = node("style");
		style.textContent =
			".sports-billing-view{min-width:0}.sports-billing-view .billing-actions{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}.sports-billing-view .table-responsive{max-width:100%;overflow:auto}.sports-billing-view th{white-space:nowrap}.sports-billing-view td{overflow-wrap:anywhere}.sports-billing-view details button{display:block;margin:6px 0}.sports-billing-view input{max-width:100%}";
		wrapper.append(style, node("h3", __("Scholarships & Billing")));
		const nav = node("div", null, "billing-actions");
		for (const [key, label] of [
			["overview", "Overview"],
			["payments", "Payments"],
			["preview", "Monthly billing"],
			["plans", "Fee plans"],
			["decisions", "Scholarship decisions"],
			["obligations", "Billing history"],
		]) {
			const b = button(label, () => {
				section = key;
				offset = 0;
				render();
			});
			b.setAttribute("aria-pressed", String(section === key));
			nav.append(b);
		}
		wrapper.append(nav);
		if (["overview", "payments"].includes(section)) {
			const panel = await frappe.sports_subscription_panel({
				section,
				call,
				config,
				signal: lifecycle.signal,
				state: subscriptionState,
				offset,
				refresh: () => render(),
				reset: () => {
					offset = 0;
					return render();
				},
			});
			if (!alive() || generation !== version || !canApply()) return;
			wrapper.append(panel.element);
			if (section === "payments") paging(wrapper, panel.has_more);
		} else if (section === "preview") {
			wrapper.append(
				node(
					"p",
					__(
						"Completed monthly fees are submitted automatically from enrollment dates. This tab shows invoices and billing exceptions; payment checkboxes are on Payments."
					),
					"text-muted"
				)
			);
			wrapper.append(
				node(
					"p",
					config.automatic_monthly_billing
						? __(
								"Automatic submission enabled: completed months are billed daily, with catch-up when enrollment or fee plans change."
						  )
						: __(
								"Automatic submission is disabled. Configure it in Academy Settings → Monthly fees."
						  ),
					"text-muted"
				)
			);
			const controls = node("div", null, "billing-actions"),
				label = node("label", __("Billing month")),
				input = node("input");
			input.type = "month";
			input.value = month;
			input.setAttribute("aria-label", __("Billing month"));
			input.addEventListener(
				"change",
				() => {
					month = input.value;
					offset = 0;
					render();
				},
				{ signal: lifecycle.signal }
			);
			label.append(input);
			controls.append(
				label,
				button("Refresh preview", () => render())
			);
			wrapper.append(controls);
			const result = await call("monthly_billing.preview", {
				month,
				program,
				start: offset,
			});
			if (!alive() || generation !== version || !canApply()) return;
			if (config.monthly_fees_enabled === false)
				wrapper.append(
					node("p", __("Monthly fees are disabled in Academy Settings."), "text-muted")
				);
			wrapper.append(
				table(
					[
						"Enrollment",
						"Player",
						"Currency",
						"Amount",
						"Due date",
						"State",
						"Invoice / issue",
					],
					result.rows.map((r) => [
						link("Sports Enrollment", r.enrollment),
						r.player_name || r.player,
						r.currency || "—",
						r.amount == null ? "—" : money(r.amount, r.currency),
						r.due_date,
						r.state === "Ready to generate"
							? __(
									month >= config.current_month
										? "Month not completed"
										: "Awaiting automatic billing"
							  )
							: r.state,
						r.error || link("Sales Invoice", r.sales_invoice),
					])
				)
			);
			paging(wrapper, result.has_more);
		} else {
			if (config.can_manage && section === "plans")
				wrapper.append(button("New fee plan", () => editPlan()));
			if (config.can_manage && section === "decisions")
				wrapper.append(button("New scholarship decision", newDecision));
			const result = await call("billing_api.records", {
				section,
				start: offset,
			});
			if (!alive() || generation !== version || !canApply()) return;
			if (section === "plans")
				wrapper.append(
					table(
						["Plan", "Program", "From", "To", "Monthly fee", "Due day", "Enabled"],
						result.rows.map((r) => [
							button(r.title, () => editPlan(r)),
							link("Sports Program", r.program),
							r.effective_from,
							r.effective_to || "—",
							money(r.monthly_amount, r.currency),
							r.due_day,
							r.enabled ? __("Yes") : __("No"),
						])
					)
				);
			if (section === "decisions")
				wrapper.append(
					table(
						["Decision", "Enrollment", "Player", "From", "To", "Status"],
						result.rows.map((r) => [
							reference(r),
							link("Sports Enrollment", r.enrollment),
							r.player,
							r.effective_from,
							r.effective_to || "—",
							[__("Draft"), __("Approved"), __("Revoked")][r.docstatus],
						])
					)
				);
			if (section === "obligations")
				wrapper.append(
					table(
						[
							"Reference",
							"Enrollment",
							"Player",
							"Month",
							"Amount",
							"Due date",
							"Invoice",
						],
						result.rows.map((r) => [
							link("Sports Billing Obligation", r.name),
							link("Sports Enrollment", r.enrollment),
							r.player,
							r.billing_month,
							money(r.amount, r.currency),
							r.due_date,
							link("Sales Invoice", r.sales_invoice),
						])
					)
				);
			if (!result.rows.length)
				wrapper.append(node("p", __("No records on this page."), "text-muted"));
			paging(wrapper, result.has_more);
		}
		if (alive() && generation === version && canApply()) host.replaceChildren(wrapper);
	}
	function paging(wrapper, more) {
		const controls = node("div", null, "billing-actions");
		if (offset)
			controls.append(
				button("Previous", () => {
					offset = Math.max(0, offset - 20);
					render();
				})
			);
		if (more)
			controls.append(
				button("More", () => {
					offset += 20;
					render();
				})
			);
		wrapper.append(controls);
	}
	return {
		async mount(options) {
			host = options.container;
			if (options.signal.aborted) return;
			options.signal.addEventListener("abort", () => lifecycle.abort(), {
				once: true,
				signal: lifecycle.signal,
			});
			await render();
			options.watch?.({
				doctypes: [
					"Sports Scholarship Decision",
					"Sports Fee Plan",
					"Sports Billing Obligation",
					"Sports Enrollment",
					"Sales Invoice",
					"Payment Entry",
				],
				refresh: ({ canApply }) => {
					if (
						[...dialogs].some((d) => d.$wrapper?.is(":visible")) ||
						host.contains(document.activeElement) ||
						host.querySelector("[data-subscription-dirty], [aria-busy=true]")
					)
						return;
					return render({ canApply });
				},
			});
		},
		unmount() {
			version++;
			lifecycle.abort();
			for (const d of dialogs) d.hide();
			dialogs.clear();
		},
	};
};
