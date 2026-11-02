/* Sports-owned private intake queue in the optional Boost host. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:registrations"] = () => {
 let host, signal, status = "Pending", offset = 0, generation = 0;
 const dialogs = new Set();
 const call = async (method, args = {}) => (await frappe.call({method: `sports_app.registrations_api.${method}`, args})).message;
 const node = (tag, text, cls) => { const el = document.createElement(tag); if (text != null) el.textContent = text; if (cls) el.className = cls; return el; };
 const button = (text, action, primary = false) => {
  const el = node("button", __(text), `btn btn-${primary ? "primary" : "default"} btn-sm`); el.type = "button";
  el.addEventListener("click", action, {signal}); return el;
 };
 const link = (doctype, name, text = name) => {
  const el = node("a", text); el.href = `/app/${frappe.router.slug(doctype)}/${encodeURIComponent(name)}`; return el;
 };
 async function accept(record) {
  const dialog = new frappe.ui.Dialog({title: __("Accept registration"), fields: [
   {fieldname: "program", label: __("Program"), fieldtype: "Link", options: "Sports Program", reqd: 1, default: record.program,
    get_query: () => ({filters: {company: record.company, enabled: 1}})},
   {fieldname: "group", label: __("Group"), fieldtype: "Link", options: "Sports Group",
    get_query: () => ({filters: {company: record.company, program: dialog.get_value("program"), enabled: 1}})},
   {fieldname: "start_date", label: __("Start date"), fieldtype: "Date", reqd: 1, default: frappe.datetime.get_today()},
   {fieldname: "status", label: __("Enrollment status"), fieldtype: "Select", options: "Pending\nActive", default: "Pending", reqd: 1}
  ], primary_action_label: __("Accept and create player"), async primary_action(values) {
   dialog.get_primary_btn().prop("disabled", true);
   try { await call("accept_registration", {name: record.name, enrollment: values}); dialog.hide(); if (!signal.aborted) await show(record.name); }
   finally { dialog.get_primary_btn().prop("disabled", false); }
  }});
  dialog.fields_dict.program.df.onchange = () => dialog.set_value("group", "");
  dialogs.add(dialog); dialog.show();
 }
 async function reject(record) {
  const dialog = new frappe.ui.Dialog({title: __("Reject registration"), fields: [
   {fieldname: "reason", label: __("Reason"), fieldtype: "Small Text", reqd: 1}
  ], primary_action_label: __("Reject registration"), async primary_action(values) {
   dialog.get_primary_btn().prop("disabled", true);
   try { await call("reject_registration", {name: record.name, reason: values.reason}); dialog.hide(); if (!signal.aborted) await show(record.name); }
   finally { dialog.get_primary_btn().prop("disabled", false); }
  }}); dialogs.add(dialog); dialog.show();
 }
 async function show(name) {
  const current = ++generation, data = await call("get_registration", {name});
  if (signal.aborted || current !== generation) return;
  const r = data.registration, wrap = node("section");
  wrap.append(button("Back to Registrations", render), node("h3", r.full_name), node("p", `${r.name} · ${r.status}`),
   node("p", __("Submitted on: {0}", [r.submitted_on])), node("p", __("Requested pathway: {0}", [r.requested_pathway])));
  if (r.status === "Pending") {
   wrap.append(link("Sports Registration", r.name, __("Edit registration details")), node("p", __("Review possible matches before accepting. Acceptance creates a separate player and their Customer/User; matching names are not automatically linked."), "text-muted"));
   if (data.possible_matches.length) {
    wrap.append(node("h4", __("Possible existing players")));
    const matches = node("ul");
    for (const row of data.possible_matches) {const li = node("li"); li.append(link("Sports Player", row.name, `${row.name} · ${row.full_name} · ${row.birth_date || ""}`)); matches.append(li);}
    wrap.append(matches);
   }
   wrap.append(button("Accept registration", () => accept(r), true), button("Reject registration", () => reject(r)));
  }
  if (data.invoice) {
   wrap.append(node("h4", __("Enrollment invoice")), node("p", `${data.invoice.name} · ${data.invoice.workflow_state} · ${data.invoice.docstatus === 1 ? __("Submitted") : __("Not posted")}`));
   if (frappe.model.can_read("Sales Invoice")) wrap.append(link("Sales Invoice", data.invoice.name, __("Open invoice")));
  }
  if (data.payment) {
   wrap.append(node("h4", __("Enrollment payment")), node("p", `${data.payment.name} · ${data.payment.workflow_state} · ${data.payment.docstatus === 1 ? __("Submitted") : __("Not posted")}`));
   if (frappe.model.can_read("Payment Entry")) wrap.append(link("Payment Entry", data.payment.name, __("View receipt")));
  }
  if (r.player) wrap.append(node("h4", __("Accepted player")), link("Sports Player", r.player));
  if (r.rejection_reason) wrap.append(node("p", __("Reason: {0}", [r.rejection_reason])));
  const details = node("dl");
  for (const field of data.fields) {
   if (field.fieldtype === "Section Break") {details.append(node("h4", __(field.label))); continue;}
   details.append(node("dt", __(field.label)), node("dd", field.fieldtype === "Check" ? (r[field.fieldname] ? __("Yes") : __("No")) : (r[field.fieldname] || "—")));
  }
  wrap.append(details); host.replaceChildren(wrap);
 }
 async function render() {
  const current = ++generation, rows = await call("list_registrations", {status, start: offset});
  if (signal.aborted || current !== generation) return;
  const wrap = node("section"); wrap.append(node("h3", __("Registrations")));
  const label = node("label", __("Registration status")); label.htmlFor = "sports-registration-status";
  const select = node("select", null, "form-control"); select.id = label.htmlFor;
  for (const value of ["Pending", "Accepted", "Rejected"]) {const option = node("option", __(value)); option.value = value; select.append(option);}
  select.value = status; select.addEventListener("change", () => {status = select.value; offset = 0; render();}, {signal});
  wrap.append(label, select, button("Refresh registrations", render));
  const tableWrap = node("div", null, "table-responsive"), table = node("table", null, "table table-striped");
  const head = node("thead"), heading = node("tr");
  for (const text of ["Reference", "Player", "Pathway", "Submitted on", "Status"]) heading.append(node("th", __(text)));
  head.append(heading); table.append(head); const body = node("tbody");
  for (const row of rows) {
   const tr = node("tr"), ref = node("td"); ref.append(button(row.name, () => show(row.name))); tr.append(ref);
   for (const key of ["full_name", "requested_pathway", "submitted_on", "status"]) tr.append(node("td", row[key]));
   body.append(tr);
  }
  table.append(body); tableWrap.append(table); wrap.append(tableWrap);
  if (!rows.length) wrap.append(node("p", __("No registrations on this page."), "text-muted"));
  if (offset) wrap.append(button("Previous registrations", () => {offset = Math.max(0, offset - 20); render();}));
  if (rows.length === 20) wrap.append(button("More registrations", () => {offset += 20; render();}));
  host.replaceChildren(wrap);
 }
 return {async mount(options) {host = options.container; signal = options.signal; await render();},
  unmount() {generation++; for (const dialog of dialogs) dialog.hide(); dialogs.clear();}};
};
