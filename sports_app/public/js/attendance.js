/* Sports-owned manual attendance prototype; no biometric capture or finance calls. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:attendance"] = () => {
	let host,
		signal,
		config,
		offset = 0,
		status = "",
		generation = 0;
	const dialogs = new Set(),
		lifecycle = new AbortController();
	const node = (tag, text, cls) => {
		const el = document.createElement(tag);
		if (text != null) el.textContent = text;
		if (cls) el.className = cls;
		return el;
	};
	const call = async (method, args = {}) =>
		(await frappe.call({ method: "sports_app.attendance_api." + method, args })).message;
	const button = (label, action, primary = false) => {
		const el = node("button", __(label), `btn btn-${primary ? "primary" : "default"} btn-sm`);
		el.type = "button";
		el.addEventListener("click", action, { signal });
		return el;
	};
	const table = (headers) => {
		const scroll = node("div", null, "table-responsive");
		scroll.tabIndex = 0;
		scroll.setAttribute("aria-label", __("Attendance table; scroll for more columns"));
		const el = node("table", null, "table table-bordered ing-console-table"),
			thead = node("thead"),
			tr = node("tr");
		for (const label of headers) {
			const th = node("th", __(label));
			th.scope = "col";
			tr.append(th);
		}
		thead.append(tr);
		const body = node("tbody");
		el.append(thead, body);
		scroll.append(el);
		return { scroll, body };
	};
	const date = (value) =>
		frappe.datetime.str_to_user ? frappe.datetime.str_to_user(String(value)) : value;
	const programLabel = (name) =>
		config.programs.find((r) => r.name === name)?.program_name || name;
	const groupLabel = (name) => config.groups.find((r) => r.name === name)?.group_name || name;
	const dialog = (options) => {
		const d = new frappe.ui.Dialog(options);
		dialogs.add(d);
		return d;
	};
	async function newSession() {
		const requestKey = crypto.randomUUID();
		const d = dialog({
			title: __("New training session"),
			fields: [
				{
					fieldname: "title",
					label: __("Session title"),
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
						filters: { company: config.company, enabled: 1 },
					}),
				},
				{
					fieldname: "group",
					label: __("Group (optional)"),
					fieldtype: "Link",
					options: "Sports Group",
					get_query: () => ({
						filters: {
							company: config.company,
							program: d.get_value("program"),
							enabled: 1,
						},
					}),
				},
				{
					fieldname: "session_date",
					label: __("Session date"),
					fieldtype: "Date",
					default: config.today,
					reqd: 1,
				},
				{
					fieldname: "start_time",
					label: __("Start time"),
					fieldtype: "Time",
					default: "16:00:00",
					reqd: 1,
				},
				{
					fieldname: "end_time",
					label: __("End time"),
					fieldtype: "Time",
					default: "18:00:00",
					reqd: 1,
				},
				{ fieldname: "venue", label: __("Venue"), fieldtype: "Data" },
			],
			primary_action_label: __("Create session"),
			async primary_action(values) {
				d.get_primary_btn().prop("disabled", true);
				try {
					const name = await call("create_session", {
						values,
						request_key: requestKey,
					});
					d.hide();
					if (!signal.aborted) {
						await render();
						await open(name);
					}
				} finally {
					d.get_primary_btn().prop("disabled", false);
				}
			},
		});
		d.fields_dict.program.df.onchange = () => d.set_value("group", "");
		d.show();
	}
	async function open(name) {
		const data = await call("roster", { name });
		if (signal.aborted) return;
		const d = dialog({
			title: __("Attendance: {0}", [data.session.title]),
			size: "extra-large",
			fields: [{ fieldname: "roster", fieldtype: "HTML" }],
		});
		const paint = (result) => {
			const s = result.session,
				body = node("section"),
				changes = [];
			const subtitle = node(
				"p",
				`${date(s.session_date)} · ${s.start_time}–${s.end_time} · ${s.timezone} · ${
					s.status
				}`,
				"text-muted"
			);
			body.append(
				subtitle,
				node(
					"p",
					[programLabel(s.program), s.group ? groupLabel(s.group) : "", s.venue || ""]
						.filter(Boolean)
						.join(" · ")
				),
				node("p", __("Responsible operator: {0}", [s.operator || "—"]), "text-muted")
			);
			if (s.finalized_on)
				body.append(
					node(
						"p",
						__("Finalized by {0} on {1}", [s.finalized_by, date(s.finalized_on)]),
						"text-muted"
					)
				);
			if (s.cancellation_reason)
				body.append(
					node(
						"p",
						__("Cancellation reason: {0}", [s.cancellation_reason]),
						"text-muted"
					)
				);
			const totals = node("div");
			totals.style.cssText = "display:flex;flex-wrap:wrap;gap:8px;margin:12px 0";
			for (const [label, count] of Object.entries(result.counts))
				totals.append(node("span", `${__(label)}: ${count}`, "ing-console-status-chip"));
			body.append(
				totals,
				node(
					"p",
					__(
						"Roster is fixed at session creation from Active, date-eligible enrollments. Unmarked is not Absent. Correcting a recorded status requires a reason."
					),
					"text-muted"
				)
			);
			const actions = node("div");
			actions.style.cssText = "display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px";
			const { scroll, body: rows } = table([
				"Player",
				"Attendance",
				"Correction reason",
				"Last recorded",
				"Audit",
			]);
			for (const r of result.rows) {
				const tr = node("tr"),
					identity = node("td");
				identity.append(
					node("strong", r.player_name),
					node("div", r.player, "text-muted")
				);
				const select = node("select", null, "form-control");
				select.setAttribute("aria-label", __("Attendance for {0}", [r.player_name]));
				for (const value of [
					...(r.status === "Unmarked" ? ["Unmarked"] : []),
					"Present",
					"Late",
					"Absent",
					"Excused",
				]) {
					const option = node("option", __(value));
					option.value = value;
					select.append(option);
				}
				select.value = r.status;
				select.disabled = s.status === "Cancelled";
				const reason = node("input", null, "form-control");
				reason.type = "text";
				reason.maxLength = 1000;
				reason.placeholder = __("Reason for a correction");
				reason.setAttribute(
					"aria-label",
					__("Correction reason for {0}", [r.player_name])
				);
				reason.disabled = s.status === "Cancelled";
				changes.push({ r, select, reason });
				const recorded = node(
					"td",
					r.marked_on
						? `${r.source} · ${date(r.marked_on)} · ${r.marked_by}`
						: __("Not marked")
				);
				recorded.style.cssText =
					"white-space:normal;max-width:240px;overflow-wrap:anywhere";
				if (r.correction_reason)
					recorded.append(node("div", r.correction_reason, "text-muted"));
				const state = node("td"),
					why = node("td"),
					audit = node("td"),
					link = node("a", __("History"));
				link.href = "/app/sports-attendance/" + encodeURIComponent(r.name);
				link.target = "_blank";
				link.rel = "noopener noreferrer";
				audit.append(link);
				state.append(select);
				why.append(reason);
				tr.append(identity, state, why, recorded, audit);
				rows.append(tr);
			}
			const dirty = () => changes.some(({ r, select }) => r.status !== select.value);
			const commit = button(
				"Save attendance",
				async () => {
					const marks = changes
						.filter(({ r, select }) => r.status !== select.value)
						.map(({ r, select, reason }) => ({
							name: r.name,
							status: select.value,
							modified: r.modified,
							reason: reason.value,
						}));
					if (!marks.length) {
						frappe.show_alert({
							message: __("No attendance changes."),
							indicator: "blue",
						});
						return;
					}
					commit.disabled = true;
					try {
						const updated = await call("save_attendance", {
							name: s.name,
							marks,
						});
						if (!signal.aborted) {
							paint(updated);
							await render();
							frappe.show_alert({
								message: __("Attendance saved."),
								indicator: "green",
							});
						}
					} finally {
						commit.disabled = false;
					}
				},
				true
			);
			actions.append(
				button("Refresh roster", () => {
					const refresh = async () => {
						const updated = await call("roster", { name: s.name });
						if (!signal.aborted) paint(updated);
					};
					if (dirty())
						frappe.confirm(
							__("Discard unsaved changes and refresh the roster?"),
							refresh
						);
					else refresh();
				})
			);
			if (s.status !== "Cancelled" && result.rows.length) {
				actions.append(commit);
				if (s.status === "Scheduled")
					actions.append(
						button("Mark unmarked Present", () => {
							for (const c of changes)
								if (c.r.status === "Unmarked") c.select.value = "Present";
						})
					);
			}
			if (s.status === "Scheduled") {
				const finalize = button("Finalize session", () => {
					if (dirty()) {
						frappe.msgprint(__("Save attendance changes before finalizing."));
						return;
					}
					frappe.confirm(
						__(
							"Finalize this session? Remaining unmarked players will be recorded as Absent."
						),
						async () => {
							finalize.disabled = true;
							try {
								const updated = await call("finalize_session", {
									name: s.name,
								});
								if (!signal.aborted) {
									paint(updated);
									await render();
								}
							} finally {
								finalize.disabled = false;
							}
						}
					);
				});
				actions.append(
					finalize,
					button("Cancel session", () => {
						if (dirty()) {
							frappe.msgprint(__("Save attendance changes before cancelling."));
							return;
						}
						const cancel = dialog({
							title: __("Cancel session"),
							fields: [
								{
									fieldname: "reason",
									label: __("Cancellation reason"),
									fieldtype: "Small Text",
									reqd: 1,
								},
							],
							primary_action_label: __("Cancel session"),
							async primary_action(values) {
								cancel.get_primary_btn().prop("disabled", true);
								try {
									const updated = await call("cancel_session", {
										name: s.name,
										reason: values.reason,
									});
									cancel.hide();
									if (!signal.aborted) {
										paint(updated);
										await render();
									}
								} finally {
									cancel.get_primary_btn().prop("disabled", false);
								}
							},
						});
						cancel.show();
					})
				);
			}
			body.append(actions, scroll);
			if (!result.rows.length)
				body.append(
					node(
						"p",
						__(
							"No eligible players. Check Active enrollment status, program/group and effective dates before creating a new session."
						),
						"text-muted"
					)
				);
			d.fields_dict.roster.$wrapper.empty().append(body);
		};
		paint(data);
		d.show();
	}
	async function render() {
		const current = ++generation,
			data = await call("list_sessions", { status, start: offset });
		if (signal.aborted || current !== generation) return;
		const wrap = node("section");
		wrap.append(
			node("h3", __("Attendance")),
			node(
				"p",
				__("Manual session attendance prototype. Biometric devices are not connected."),
				"text-muted"
			)
		);
		const toolbar = node("div");
		toolbar.style.cssText =
			"display:flex;flex-wrap:wrap;align-items:end;gap:12px;margin-bottom:16px";
		const label = node("label", __("Session status")),
			select = node("select", null, "form-control");
		select.id = "sports-session-status";
		label.htmlFor = select.id;
		for (const value of ["", "Scheduled", "Finalized", "Cancelled"]) {
			const option = node("option", value ? __(value) : __("All sessions"));
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
		const mobile = node("a", __("Open attendance app"), "btn btn-default btn-sm");
		mobile.href = "/sports-attendance";
		mobile.target = "_blank";
		mobile.rel = "noopener";
		const filter = node("div");
		filter.append(label, select);
		toolbar.append(
			filter,
			button("New session", newSession, true),
			button("Refresh sessions", render),
			mobile
		);
		wrap.append(toolbar);
		const { scroll, body } = table([
			"Session",
			"Date / time",
			"Program / group",
			"Venue",
			"Status",
		]);
		for (const r of data.rows) {
			const tr = node("tr"),
				ref = node("td");
			ref.append(
				button(r.title, () => open(r.name)),
				node("div", r.name, "text-muted")
			);
			tr.append(
				ref,
				node(
					"td",
					`${date(r.session_date)} · ${r.start_time}–${r.end_time} (${r.timezone})`
				),
				node("td", `${r.program_label}${r.group ? " / " + groupLabel(r.group) : ""}`),
				node("td", r.venue || "—"),
				node("td", __(r.status))
			);
			body.append(tr);
		}
		wrap.append(scroll);
		if (!data.rows.length)
			wrap.append(
				node(
					"p",
					__("No sessions yet. Create a session to generate its eligible roster."),
					"text-muted"
				)
			);
		if (offset)
			wrap.append(
				button("Previous sessions", () => {
					offset = Math.max(0, offset - 20);
					render();
				})
			);
		if (data.has_more)
			wrap.append(
				button("More sessions", () => {
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
			config = await call("configuration");
			if (!signal.aborted) await render();
		},
		unmount() {
			generation++;
			lifecycle.abort();
			for (const d of dialogs) d.hide();
			dialogs.clear();
		},
	};
};
