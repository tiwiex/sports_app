/* Sports-owned private registration and enrollment in the shared Boost shell. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:players"] = () => {
 let host, signal, search = "", offset = 0, generation = 0;
 const dialogs = new Set();
 const node = (tag, text, cls) => {
  const el = document.createElement(tag);
  if (text != null) el.textContent = text;
  if (cls) el.className = cls;
  return el;
 };
 const call = async (method, args = {}) => (await frappe.call({ method: `sports_app.players_api.${method}`, args })).message;
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
  const el = node("table", null, "table table-striped");
  const head = node("thead"), tr = node("tr");
  for (const label of labels) tr.append(node("th", __(label)));
  head.append(tr); el.append(head);
  const body = node("tbody");
  for (const values of rows) {
   const row = node("tr");
   for (const value of values) {
    const td = node("td");
    if (value instanceof Node) td.append(value); else td.textContent = value || "";
    row.append(td);
   }
   body.append(row);
  }
  el.append(body); wrap.append(el); return wrap;
 };
 const showPlayer = async (name, start = 0) => {
  const current = ++generation;
  const result = await call("get_player", { name, start });
  if (signal.aborted || current !== generation) return;
  const p = result.player, wrapper = node("section");
  wrapper.append(button("Back to Players", render), node("h3", p.full_name), node("p", `${p.name} · ${p.company}`));
  wrapper.append(node("p", __("Registered on: {0}", [p.registered_on])), link("Sports Player", p.name));
  if (p.customer) wrapper.append(node("p", __("Customer")), link("Customer", p.customer, p.full_name));
  if (p.portal_user) wrapper.append(node("p", __("Self-service User: {0} (prepared for future activation)", [p.portal_user]), "text-muted"));
  wrapper.append(node("h4", __("Enrollments")));
  wrapper.append(button("New Enrollment", () => newEnrollment(p)));
  wrapper.append(table(["Enrollment", "Program", "Group", "Customer", "Start", "End", "Status", "Eligible today"], result.enrollments.map(row => [
   link("Sports Enrollment", row.name), row.program_name || row.program, row.group_name || row.group, link("Customer", row.payer_customer, p.full_name), row.start_date, row.end_date, row.status, row.eligible_today ? __("Yes") : __("No")
  ])));
  if (!result.enrollments.length) wrapper.append(node("p", __("No enrollments on this page."), "text-muted"));
  if (start) wrapper.append(button("Previous enrollments", () => showPlayer(name, Math.max(0, start - 20))));
  if (result.enrollments.length === 20) wrapper.append(button("More enrollments", () => showPlayer(name, start + 20)));
  wrapper.append(node("p", __("Each player has their own Customer account, created during registration. Registration and enrollment do not create invoices or payments."), "text-muted"));
  host.replaceChildren(wrapper);
 };
 const enrollmentFields = company => [
  { fieldname: "program", label: __("Program"), fieldtype: "Link", options: "Sports Program", reqd: 1, get_query: () => ({ filters: { company, enabled: 1 } }) },
  { fieldname: "group", label: __("Group"), fieldtype: "Link", options: "Sports Group", get_query() { return { filters: { program: this.layout.get_value("program"), enabled: 1 } }; } },
  { fieldname: "start_date", label: __("Start date"), fieldtype: "Date", reqd: 1, default: frappe.datetime.get_today() },
  { fieldname: "end_date", label: __("End date"), fieldtype: "Date" },
  { fieldname: "status", label: __("Status"), fieldtype: "Select", options: "Pending\nActive\nSuspended\nWithdrawn\nCompleted", reqd: 1, default: "Pending" },
 ];
 const showDialog = async (title, fields, action, defaults) => {
  const dialog = new frappe.ui.Dialog({ title: __(title), fields, primary_action_label: __("Save"),
   async primary_action(values) {
    dialog.get_primary_btn().prop("disabled", true);
    try { const saved = await action(values); if (saved !== false && !signal.aborted) dialog.hide(); }
    finally { dialog.get_primary_btn().prop("disabled", false); }
   }
  });
  dialogs.add(dialog);
  dialog.fields_dict.program.df.onchange = () => dialog.set_value("group", "");
  dialog.fields_dict.group.df.get_query = () => ({ filters: { program: dialog.get_value("program"), enabled: 1 } });
  await dialog.set_values({ ...(defaults || {}), group: "" });
  // Program onchange clears Group asynchronously; apply the configured group last.
  await dialog.set_value("group", defaults?.group || "");
  if (signal.aborted) { dialog.hide(); return; }
  dialog.show(); return dialog;
 };
 const newEnrollment = player => showDialog("New Enrollment", enrollmentFields(player.company), async values => {
  await call("save_enrollment", { player: player.name, enrollment: values });
  if (!signal.aborted) await showPlayer(player.name);
 });
 const register = async () => {
  const defaults = await call("get_registration_defaults");
  if (signal.aborted) return;
  const key = crypto.randomUUID();
  const playerFields = defaults.player_fields;
  const fields = [
   ...playerFields.map(field => ({ ...field, label: __(field.label), description: field.description ? __(field.description) : undefined })),
   { fieldname: "enrollment_section", label: __("Initial enrollment"), fieldtype: "Section Break" },
   ...enrollmentFields(defaults.company)
  ];
  showDialog("Register Player", fields, async values => {
   const similar = await call("list_players", { search: `${values.first_name} ${values.last_name}` });
   if (signal.aborted) return;
   if (similar.some(row => row.full_name.toLowerCase() === `${values.first_name} ${values.last_name}`.trim().toLowerCase())) {
    const confirmed = await new Promise(resolve => frappe.confirm(__("A player with this name already exists. Register a separate player? Check Players first if unsure."), () => resolve(true), () => resolve(false)));
    if (!confirmed || signal.aborted) return false;
   }
   const player = {}, enrollment = {};
   for (const field of playerFields.filter(field => field.fieldtype !== "Section Break")) player[field.fieldname] = values[field.fieldname] ?? "";
   for (const field of ["program", "group", "start_date", "end_date", "status"]) enrollment[field] = values[field] || "";
   const name = await call("register_player", { player, enrollment, request_key: key });
   if (!signal.aborted) await showPlayer(name);
  }, { program: defaults.default_program, group: defaults.default_group, status: defaults.default_enrollment_status });
 };
 async function render() {
  const current = ++generation;
  const rows = await call("list_players", { search, start: offset });
  if (signal.aborted || current !== generation) return;
  const wrapper = node("section");
  wrapper.append(node("h3", __("Players")), button("Register Player", register, true));
  const label = node("label", __("Search by registration ID or name"));
  label.htmlFor = "sports-player-search";
  const input = node("input", null, "form-control"); input.id = label.htmlFor; input.value = search; input.type = "search";
  const form = node("form");
  form.append(label, input, button("Search", () => { search = input.value; offset = 0; render(); }));
  form.addEventListener("submit", event => { event.preventDefault(); search = input.value; offset = 0; render(); }, { signal });
  wrapper.append(form);
  wrapper.append(table(["Registration ID", "Name", "Date of birth", "Company"], rows.map(row => [button(row.name, () => showPlayer(row.name)), row.full_name, row.birth_date, row.company])));
  if (!rows.length) wrapper.append(node("p", __("No players found."), "text-muted"));
  if (offset) wrapper.append(button("Previous", () => { offset = Math.max(0, offset - 20); render(); }));
  if (rows.length === 20) wrapper.append(button("Next", () => { offset += 20; render(); }));
  host.replaceChildren(wrapper);
 }
 return {
  async mount(options) { host = options.container; signal = options.signal; await render(); },
  unmount() { generation++; for (const dialog of dialogs) dialog.hide(); dialogs.clear(); }
 };
};
