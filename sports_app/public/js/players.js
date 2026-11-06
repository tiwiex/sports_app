/* Sports-owned private registration and enrollment in the shared Boost shell. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:players"] = () => {
	let liveSnapshot;
	let host,
		signal,
		search = "",
		offset = 0,
		generation = 0,
		profileDialog,
		profileController,
		profileTab = "details",
		profileName,
		sortBy = "registered_on",
		sortOrder = "desc";
	const lifecycle = new AbortController();
	const dialogs = new Set();
	const node = (tag, text, cls) => {
		const el = document.createElement(tag);
		if (text != null) el.textContent = text;
		if (cls) el.className = cls;
		return el;
	};
	const call = async (method, args = {}) =>
		(await frappe.call({ method: `sports_app.players_api.${method}`, args })).message;
	const button = (label, action, primary = false) => {
		const el = node("button", __(label), `btn btn-${primary ? "primary" : "default"} btn-sm`);
		el.type = "button";
		el.addEventListener("click", action, { signal });
		return el;
	};
	const link = (doctype, name, label = name) => {
		const el = node("a", label);
		el.href = `/app/${frappe.router.slug(doctype)}/${encodeURIComponent(name)}`;
		return el;
	};
	const table = (labels, rows) => {
		const wrap = node("div", null, "table-responsive");
		const el = node("table", null, "table table-bordered ing-console-table");
		const head = node("thead"),
			tr = node("tr");
		for (const label of labels) {
			const th = node("th", __(label));
			th.scope = "col";
			tr.append(th);
		}
		head.append(tr);
		el.append(head);
		const body = node("tbody");
		for (const values of rows) {
			const row = node("tr");
			for (const value of values) {
				const td = node("td");
				if (value instanceof Node) td.append(value);
				else td.textContent = value || "";
				row.append(td);
			}
			body.append(row);
		}
		el.append(body);
		wrap.append(el);
		return wrap;
	};
	const formatDate = (value) =>
		value
			? frappe.datetime.str_to_user
				? frappe.datetime.str_to_user(String(value).split(".")[0])
				: value
			: "—";
	const statusChip = (status) => {
		const chip = node("span", __(status), "ing-console-status-chip");
		chip.classList.add(
			status === "Active"
				? "is-approved"
				: status === "Pending"
				? "is-pending-review"
				: "is-draft"
		);
		return chip;
	};
	const closeMenus = () => {
		for (const menu of host.querySelectorAll(".sports-player-menu")) {
			menu.classList.remove("is-open");
			menu.querySelector("button").setAttribute("aria-expanded", "false");
			menu.querySelector(".dropdown-menu").removeAttribute("style");
		}
	};
	const startEnrollment = async (name) => {
		const result = await call("get_player", { name });
		if (signal.aborted) return;
		if (!result.can_enroll) {
			frappe.msgprint(
				__("You do not have permission to add an enrollment for this player.")
			);
			return;
		}
		return newEnrollment(result.player);
	};
	const referenceMenu = (row) => {
		const menu = node("div", null, "ing-console-action-menu sports-player-menu"),
			list = node("ul", null, "dropdown-menu");
		list.setAttribute("role", "menu");
		const toggle = button(row.name, (event) => {
			event.preventDefault();
			event.stopPropagation();
			const open = menu.classList.contains("is-open");
			closeMenus();
			if (open) return;
			menu.classList.add("is-open");
			toggle.setAttribute("aria-expanded", "true");
			const rect = toggle.getBoundingClientRect(),
				width = Math.max(170, list.getBoundingClientRect().width);
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
		toggle.setAttribute("aria-label", __("Actions for player {0}", [row.name]));
		toggle.setAttribute("aria-haspopup", "menu");
		toggle.setAttribute("aria-expanded", "false");
		toggle.append(node("span", "▾", "ing-console-action-caret"));
		const add = (label, action) => {
			const li = node("li"),
				item = button(label, (event) => {
					event.preventDefault();
					event.stopPropagation();
					closeMenus();
					action();
				});
			item.className = "dropdown-item";
			item.setAttribute("role", "menuitem");
			item.style.cssText = "width:100%;text-align:left;border:0;background:transparent";
			li.append(item);
			list.append(li);
		};
		add("View", () => showPlayer(row.name));
		if (row.can_change_id) add("Change Player ID", () => changeId(row.name));
		if (row.can_enroll) add("New program enrollment", () => startEnrollment(row.name));
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
	};
	const changeId = async (name) => {
		const dialog = await frappe.sports_player_ids.change(name, async (newName) => {
			if (signal.aborted) return;
			await render();
			await showPlayer(newName);
		});
		if (dialog) {
			dialogs.add(dialog);
			if (signal.aborted) dialog.hide();
		}
	};
	const showPlayer = async (name, start = 0) => {
		const current = ++generation;
		profileController?.abort();
		const result = await call("get_player", { name, start });
		if (signal.aborted || current !== generation) return;
		if (profileName !== name) profileTab = "details";
		profileName = name;
		const p = result.player,
			wrapper = node("section", null, "sports-player-profile");
		const style = node("style");
		style.textContent = `
   .sports-player-profile{color:var(--text-color,#173042);font-size:14px;line-height:1.5}
   .sports-player-profile .player-hero{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:18px}
   .sports-player-profile .player-identity{display:flex;align-items:center;gap:14px;min-width:0;max-width:100%}
   .sports-player-profile .player-identity>div{min-width:0}
   .sports-player-profile .player-hero h3{margin:3px 0 5px;font-size:24px;overflow-wrap:anywhere}
   .sports-player-profile .player-eyebrow{color:var(--text-muted,#607287);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em}
   .sports-player-profile .player-card{border:1px solid var(--border-color,#d7e2ed);border-radius:8px;padding:18px;margin-bottom:16px;background:var(--card-bg,#fff)}
   .sports-player-profile .player-summary{background:var(--subtle-fg,#f4f8fb)}
   .sports-player-profile .player-card h4{font-size:15px;margin:0 0 14px;font-weight:700}
   .sports-player-profile .player-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 24px;margin:0}
   .sports-player-profile .player-field{min-width:0}.sports-player-profile .player-field.is-wide{grid-column:1/-1}
   .sports-player-profile dt{font-size:12px;font-weight:500;color:var(--text-muted,#607287);margin-bottom:4px}
   .sports-player-profile dd{font-size:14px;font-weight:500;margin:0;white-space:pre-wrap;overflow-wrap:anywhere}
   .sports-player-profile a{overflow-wrap:anywhere}
   .sports-player-profile .player-actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:14px}
   @media(max-width:640px){.sports-player-profile .player-grid{grid-template-columns:minmax(0,1fr)}.sports-player-profile .player-card{padding:14px}.sports-player-profile .player-hero h3{font-size:21px}}
  `;
		wrapper.append(style);
		const card = (label, cls = "") => {
			const section = node("section", null, `player-card ${cls}`);
			section.append(node("h4", __(label)));
			wrapper.append(section);
			return section;
		};
		const grid = (section) => {
			const dl = node("dl", null, "player-grid");
			section.append(dl);
			return dl;
		};
		const field = (dl, label, value, wide = false) => {
			const cell = node("div", null, `player-field${wide ? " is-wide" : ""}`),
				dd = node("dd");
			if (value instanceof Node) dd.append(value);
			else dd.textContent = value == null || value === "" ? "—" : value;
			cell.append(node("dt", __(label)), dd);
			dl.append(cell);
		};
		const hero = node("header", null, "player-hero"),
			portraitTarget = node("div", null, "player-identity"),
			identity = node("div");
		identity.append(
			node("div", __("Player profile"), "player-eyebrow"),
			node("h3", p.full_name)
		);
		portraitTarget.append(identity);
		hero.append(portraitTarget, node("span", p.name, "ing-console-status-chip"));
		wrapper.append(hero);
		const summary = grid(card("Player summary", "player-summary"));
		field(summary, "Player ID", p.name);
		field(summary, "Academy company", p.company);
		field(summary, "Registered on", formatDate(p.registered_on));
		const actions = node("div", null, "player-actions player-profile-global-actions");
		actions.append(link("Sports Player", p.name, __("Open player record")));
		if (result.can_enroll)
			actions.append(button("New program enrollment", () => newEnrollment(p), true));
		if (result.can_change_id) {
			actions.append(button("Change Player ID", () => changeId(p.name)));
			const history = node("a", __("ID change history"), "btn btn-default btn-sm");
			history.href = `/app/sports-player-id-change?player=${encodeURIComponent(p.name)}`;
			actions.append(history);
		}
		wrapper.append(actions);
		const accounts = grid(card("Linked accounts"));
		field(
			accounts,
			"Customer",
			p.customer
				? frappe.model.can_read("Customer")
					? link("Customer", p.customer, p.full_name)
					: p.customer
				: null
		);
		field(accounts, "Self-service account", p.portal_user || null);
		field(accounts, "Guardian account", p.guardian_user || null);
		const memberships = card("Program enrollments");
		memberships.dataset.playerEnrollments = "true";
		memberships.append(
			table(
				["Enrollment", "Program", "Group", "Start", "End", "Status", "Eligible today"],
				result.enrollments.map((row) => [
					link("Sports Enrollment", row.name),
					row.program_name || row.program,
					row.group_name || row.group || "—",
					formatDate(row.start_date),
					formatDate(row.end_date),
					statusChip(row.status),
					row.eligible_today ? __("Yes") : __("No"),
				])
			)
		);
		if (!result.enrollments.length)
			memberships.append(
				node("p", __("No program enrollments on this page."), "text-muted")
			);
		const pages = node("div", null, "player-actions");
		if (start)
			pages.append(
				button("Previous enrollments", () => showPlayer(name, Math.max(0, start - 20)))
			);
		if (result.enrollments.length === 20)
			pages.append(button("More enrollments", () => showPlayer(name, start + 20)));
		memberships.append(pages);
		memberships.append(
			node(
				"p",
				__(
					"Active, date-eligible program enrollments are used for attendance rosters. Adding an enrollment does not create an invoice or payment."
				),
				"text-muted"
			)
		);
		let values;
		for (const item of result.fields || []) {
			if (item.fieldtype === "Section Break") {
				values = grid(card(item.label === "The player" ? "Player details" : item.label));
				continue;
			}
			if (!values) values = grid(card("Player details"));
			field(
				values,
				item.label,
				item.fieldtype === "Check"
					? p[item.fieldname]
						? __("Yes")
						: __("No")
					: p[item.fieldname],
				item.fieldtype === "Small Text"
			);
		}
		const panels = frappe.sports_player_profile?.create_tabs(wrapper, profileTab, (key) => {
			profileTab = key;
		});
		const linked = node("div");
		(panels?.details || wrapper).append(linked);
		if (profileDialog) profileDialog.hide();
		profileController = new AbortController();
		const currentController = profileController;
		profileDialog = new frappe.ui.Dialog({
			title: __("Player: {0}", [p.name]),
			size: "extra-large",
			fields: [{ fieldname: "player_view", fieldtype: "HTML" }],
		});
		profileDialog.fields_dict.player_view.$wrapper.append(wrapper);
		dialogs.add(profileDialog);
		profileDialog.onhide = () => currentController.abort();
		profileDialog.show();
		frappe.sports_player_profile?.mount({
			container: linked,
			name,
			signal: currentController.signal,
			panels,
			portraitTarget,
		});
	};
	const enrollmentFields = (company) => [
		{
			fieldname: "program",
			label: __("Program"),
			fieldtype: "Link",
			options: "Sports Program",
			reqd: 1,
			get_query: () => ({ filters: { company, enabled: 1 } }),
		},
		{
			fieldname: "group",
			label: __("Group"),
			fieldtype: "Link",
			options: "Sports Group",
			get_query() {
				return {
					filters: { program: this.layout.get_value("program"), enabled: 1 },
				};
			},
		},
		{
			fieldname: "start_date",
			label: __("Start date"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.get_today(),
		},
		{ fieldname: "end_date", label: __("End date"), fieldtype: "Date" },
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "Pending\nActive\nSuspended\nWithdrawn\nCompleted",
			reqd: 1,
			default: "Pending",
		},
	];
	const showDialog = async (title, fields, action, defaults) => {
		const dialog = new frappe.ui.Dialog({
			title: __(title),
			fields,
			primary_action_label: __("Save"),
			async primary_action(values) {
				dialog.get_primary_btn().prop("disabled", true);
				try {
					const saved = await action(values);
					if (saved !== false && !signal.aborted) dialog.hide();
				} finally {
					dialog.get_primary_btn().prop("disabled", false);
				}
			},
		});
		dialogs.add(dialog);
		dialog.fields_dict.program.df.onchange = () => dialog.set_value("group", "");
		dialog.fields_dict.group.df.get_query = () => ({
			filters: { program: dialog.get_value("program"), enabled: 1 },
		});
		await dialog.set_values({ ...(defaults || {}), group: "" });
		// Program onchange clears Group asynchronously; apply the configured group last.
		await dialog.set_value("group", defaults?.group || "");
		if (signal.aborted) {
			dialog.hide();
			return;
		}
		dialog.show();
		return dialog;
	};
	const newEnrollment = (player) =>
		showDialog("New program enrollment", enrollmentFields(player.company), async (values) => {
			await call("save_enrollment", {
				player: player.name,
				enrollment: values,
			});
			if (!signal.aborted) {
				profileTab = "enrollments";
				await showPlayer(player.name);
			}
		});
	const register = async () => {
		const defaults = await call("get_registration_defaults");
		if (signal.aborted) return;
		const key = crypto.randomUUID();
		const playerFields = defaults.player_fields;
		const fields = [
			...playerFields.map((field) => ({
				...field,
				label: __(field.label),
				description: field.description ? __(field.description) : undefined,
			})),
			{
				fieldname: "enrollment_section",
				label: __("Initial enrollment"),
				fieldtype: "Section Break",
			},
			...enrollmentFields(defaults.company),
		];
		showDialog(
			"Register Player",
			fields,
			async (values) => {
				const similar = await call("list_players", {
					search: `${values.first_name} ${values.last_name}`,
				});
				if (signal.aborted) return;
				if (
					similar.some(
						(row) =>
							row.full_name.toLowerCase() ===
							`${values.first_name} ${values.last_name}`.trim().toLowerCase()
					)
				) {
					const confirmed = await new Promise((resolve) =>
						frappe.confirm(
							__(
								"A player with this name already exists. Register a separate player? Check Players first if unsure."
							),
							() => resolve(true),
							() => resolve(false)
						)
					);
					if (!confirmed || signal.aborted) return false;
				}
				const player = {},
					enrollment = {};
				for (const field of playerFields.filter(
					(field) => field.fieldtype !== "Section Break"
				))
					player[field.fieldname] = values[field.fieldname] ?? "";
				for (const field of ["program", "group", "start_date", "end_date", "status"])
					enrollment[field] = values[field] || "";
				const name = await call("register_player", {
					player,
					enrollment,
					request_key: key,
				});
				if (!signal.aborted) {
					await render();
					await showPlayer(name);
				}
			},
			{
				program: defaults.default_program,
				group: defaults.default_group,
				status: defaults.default_enrollment_status,
			}
		);
	};
	async function render(options = {}) {
		const background = options.background === true;
		const canApply = options.canApply || (() => true);
		if (!background) closeMenus();
		const current = background ? generation : ++generation;
		const rows = await call("list_players", {
			search,
			start: offset,
			sort_by: sortBy,
			sort_order: sortOrder,
		});
		if (signal.aborted || current !== generation || !canApply()) return false;
		const snapshot = JSON.stringify(rows);
		if (background && snapshot === liveSnapshot) return;
		liveSnapshot = snapshot;
		const wrapper = node("section");
		wrapper.append(
			node("h3", __("Players")),
			node(
				"p",
				__("Manage player profiles and program enrollments without leaving the console."),
				"text-muted"
			),
			button("Register Player", register, true)
		);
		const label = node("label", __("Search by registration ID or name"));
		label.htmlFor = "sports-player-search";
		const input = node("input", null, "form-control");
		input.id = label.htmlFor;
		input.value = search;
		input.type = "search";
		const form = node("form");
		form.style.cssText = "display:flex;flex-wrap:wrap;align-items:end;gap:12px;margin:14px 0";
		const searchField = node("div");
		searchField.append(label, input);
		form.append(
			searchField,
			button("Search", () => {
				search = input.value;
				offset = 0;
				render();
			})
		);
		form.addEventListener(
			"submit",
			(event) => {
				event.preventDefault();
				search = input.value;
				offset = 0;
				render();
			},
			{ signal }
		);
		wrapper.append(form);
		const listing = table(
			["Player ID", "Name", "Date of birth", "Company", "Registered on"],
			rows.map((row) => [
				referenceMenu(row),
				row.full_name,
				formatDate(row.birth_date),
				row.company,
				formatDate(row.registered_on),
			])
		);
		for (const [index, field] of [
			"name",
			"full_name",
			"birth_date",
			"company",
			"registered_on",
		].entries()) {
			const th = listing.querySelectorAll("th")[index],
				label = th.textContent,
				active = sortBy === field;
			th.setAttribute(
				"aria-sort",
				active ? (sortOrder === "asc" ? "ascending" : "descending") : "none"
			);
			const sort = button(
				label + (active ? (sortOrder === "asc" ? " ↑" : " ↓") : " ↕"),
				() => {
					sortOrder = active && sortOrder === "asc" ? "desc" : "asc";
					sortBy = field;
					offset = 0;
					render();
				}
			);
			sort.setAttribute("aria-label", __("Sort by {0}", [label]));
			sort.style.cssText =
				"font:inherit;color:inherit;background:transparent;border:0;padding:0;white-space:nowrap";
			th.replaceChildren(sort);
		}
		wrapper.append(listing);
		if (!rows.length) wrapper.append(node("p", __("No players found."), "text-muted"));
		if (offset)
			wrapper.append(
				button("Previous", () => {
					offset = Math.max(0, offset - 20);
					render();
				})
			);
		if (rows.length === 20)
			wrapper.append(
				button("Next", () => {
					offset += 20;
					render();
				})
			);
		host.replaceChildren(wrapper);
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
						const toggle = host.querySelector(".sports-player-menu.is-open > button");
						closeMenus();
						if (toggle) toggle.focus();
					}
				},
				{ signal }
			);
			window.addEventListener("resize", closeMenus, { signal });
			host.addEventListener("scroll", closeMenus, { capture: true, signal });
			await render();
			options.watch?.({
				doctypes: ["Sports Player", "Sports Enrollment", "User", "Customer"],
				refresh: ({ canApply }) => render({ background: true, canApply }),
			});
		},
		unmount() {
			generation++;
			closeMenus();
			lifecycle.abort();
			profileController?.abort();
			for (const dialog of dialogs) dialog.hide();
			dialogs.clear();
		},
	};
};
