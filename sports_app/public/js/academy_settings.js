/* Academy configuration belongs to Sports App; Boost only mounts the view. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:settings"] = () => {
 let host, signal, form, configuration;
 const node = (tag, text, className) => {
  const element = document.createElement(tag);
  if (text) element.textContent = __(text);
  if (className) element.className = className;
  return element;
 };
 const call = async (method, args = {}) => {
  const response = await frappe.call({ method: `sports_app.settings_api.${method}`, args });
  return response.message;
 };
 const button = (label, action, primary = false) => {
  const element = node("button", label, `btn btn-${primary ? "primary" : "default"} btn-sm`);
  element.type = "button";
  element.addEventListener("click", action, { signal });
  return element;
 };
 const companyOptions = () => configuration.companies.map(row => row.name);
 const programFields = [
  { fieldname: "program_name", label: __("Program name"), fieldtype: "Data", reqd: 1 },
  { fieldname: "sport", label: __("Sport"), fieldtype: "Data", reqd: 1 },
  { fieldname: "company", label: __("Company"), fieldtype: "Select", options: [], reqd: 1 },
  { fieldname: "enabled", label: __("Enabled"), fieldtype: "Check", default: 1 },
 ];
 const groupFields = [
  { fieldname: "group_name", label: __("Group name"), fieldtype: "Data", reqd: 1 },
  { fieldname: "program", label: __("Program"), fieldtype: "Link", options: "Sports Program", reqd: 1,
   get_query: () => ({ filters: { enabled: 1, company: form.get_value("company") } }) },
  { fieldname: "enabled", label: __("Enabled"), fieldtype: "Check", default: 1 },
 ];
 const dialogs = new Set();
 const editMaster = (kind, existing) => {
  const isProgram = kind === "program";
  const fields = (isProgram ? programFields : groupFields).map(field => ({ ...field }));
  if (isProgram) fields.find(field => field.fieldname === "company").options = companyOptions();
  const dialog = new frappe.ui.Dialog({
   title: isProgram ? __("Program") : __("Group"), fields,
   primary_action_label: __("Save"),
   async primary_action(values) {
    dialog.get_primary_btn().prop("disabled", true);
    try {
     const name = existing?.name;
     await call(isProgram ? "save_program" : "save_group", { [kind]: { ...values, ...(name ? { name } : {}) } });
     dialog.hide();
     // Preserve unsaved settings when refreshing master lists.
     const current = form.get_values(true);
     await render(current);
    } finally { dialog.get_primary_btn().prop("disabled", false); }
   },
  });
  dialogs.add(dialog);
  dialog.set_values(existing || { company: form.get_value("company"), program: form.get_value("default_program"), enabled: 1 });
  dialog.show();
 };
 const renderMasters = (parent, title, rows, kind) => {
  const section = node("section");
  section.style.marginTop = "28px";
  section.append(node("h4", title), button(kind === "program" ? "New Program" : "New Group", () => editMaster(kind)));
  if (!rows.length) section.append(node("p", kind === "program" ? "No programs configured." : "No groups configured.", "text-muted"));
  const table = node("table", null, "table table-striped");
  const header = node("tr");
  for (const label of ["Name", kind === "program" ? "Sport" : "Program", "Company", "Status", ""]) header.append(node("th", label));
  const head = node("thead"); head.append(header); table.append(head);
  const body = node("tbody");
  for (const row of rows) {
   const tr = node("tr");
   const program = configuration.programs.find(item => item.name === row.program);
   for (const value of [row[`${kind}_name`], kind === "program" ? row.sport : (program?.program_name || row.program), row.company, row.enabled ? __("Enabled") : __("Disabled")]) {
    const td = node("td"); td.textContent = value || ""; tr.append(td);
   }
   const td = node("td"); td.append(button("Edit", () => editMaster(kind, row))); tr.append(td); body.append(tr);
  }
  table.append(body);
  const scroll = node("div", null, "table-responsive"); scroll.append(table); section.append(scroll); parent.append(section);
 };
 const render = async (preserved) => {
  configuration = await call("get_configuration");
  if (signal.aborted) return;
  const wrapper = node("div");
  wrapper.append(node("h3", "Academy Settings"), node("p", "Choose a company, add programs and groups below, then save the academy's defaults. Saving does not create players or charges.", "text-muted"));
  if (!configuration.companies.length) wrapper.append(node("p", "No accessible company. Ask the administrator to grant access to the academy's company.", "alert alert-warning"));
  const controls = node("div"); wrapper.append(controls);
  const values = preserved || configuration.settings;
  form = new frappe.ui.FieldGroup({ body: controls, fields: [
   { fieldname: "academy_name", label: __("Academy name"), fieldtype: "Data", reqd: 1 },
   { fieldname: "company", label: __("Company"), fieldtype: "Select", options: ["", ...companyOptions()], reqd: 1 },
   { fieldname: "currency", label: __("Fee currency"), fieldtype: "Link", options: "Currency", reqd: 1, get_query: () => ({ filters: { enabled: 1 } }) },
   { fieldname: "timezone", label: __("Academy timezone"), fieldtype: "Select", options: ["", ...configuration.timezones], reqd: 1 },
   { fieldname: "registration_prefix", label: __("Registration prefix"), fieldtype: "Data", reqd: 1, description: __("For example ACADEMY. Existing player IDs will never be renumbered.") },
   { fieldname: "registration_digits", label: __("Registration digits"), fieldtype: "Int", default: 5, reqd: 1 },
   { fieldname: "default_enrollment_status", label: __("Default enrollment status"), fieldtype: "Select", options: "Pending\nActive", default: "Pending", reqd: 1 },
   { fieldname: "default_program", label: __("Default program"), fieldtype: "Link", options: "Sports Program", reqd: 1, get_query: () => ({ filters: { company: form.get_value("company"), enabled: 1 } }) },
   { fieldname: "default_group", label: __("Default group"), fieldtype: "Link", options: "Sports Group", get_query: () => ({ filters: { program: form.get_value("default_program"), enabled: 1 } }) },
   { fieldname: "monthly_fees_enabled", label: __("Monthly fees enabled"), fieldtype: "Check", default: 1 },
   { fieldname: "default_monthly_fee", label: __("Default monthly fee"), fieldtype: "Currency", options: "currency", description: __("Default for monthly fees. Saving this amount does not create a charge or payment.") },
  ] });
  form.make();
  await form.set_values(values);
  if (signal.aborted) return;
  const preview = node("p", null, "text-muted");
  const updatePreview = () => {
   const digits = Math.min(10, Math.max(4, Number(form.get_value("registration_digits")) || 5));
   preview.textContent = __("Registration example: {0} (preview only)", [`${form.get_value("registration_prefix") || "…"}-${"1".padStart(digits, "0")}`]);
  };
  form.fields_dict.registration_prefix.df.onchange = updatePreview;
  form.fields_dict.registration_digits.df.onchange = updatePreview;
  form.fields_dict.company.df.onchange = () => { form.set_value("default_program", ""); form.set_value("default_group", ""); };
  form.fields_dict.default_program.df.onchange = () => form.set_value("default_group", "");
  updatePreview(); wrapper.append(preview);
  const save = button("Save Settings", async () => {
   const settings = form.get_values();
   if (!settings) return;
   save.disabled = true;
   try {
    const result = await call("save_configuration", { settings: { ...settings, modified: configuration.settings.modified } });
    if (signal.aborted) return;
    configuration.settings = result;
    frappe.show_alert({ message: __("Academy settings saved"), indicator: "green" });
   } finally { save.disabled = false; }
  }, true);
  wrapper.append(save);
  renderMasters(wrapper, "Programs", configuration.programs, "program");
  renderMasters(wrapper, "Groups", configuration.groups, "group");
  host.replaceChildren(wrapper);
 };
 return {
  async mount(options) { host = options.container; signal = options.signal; await render(); },
  unmount() { for (const dialog of dialogs) dialog.hide(); dialogs.clear(); },
 };
};
