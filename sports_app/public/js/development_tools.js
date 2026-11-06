/* Sports-owned, management-only documentation inside the optional Boost shell. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:development"] = () => {
 let host, signal, documents, index, reader, search, currentPath, dialog, tabs, category = "User Stories", generation = 0;
 const node = (tag, text, cls) => {
  const el = document.createElement(tag);
  if (text != null) el.textContent = text;
  if (cls) el.className = cls;
  return el;
 };
 const call = async (method, args = {}) => (await frappe.call({ method: `sports_app.development_api.${method}`, args })).message;
 const localPath = href => {
  const url = new URL(href, `https://sports-docs.invalid/${currentPath}`);
  return url.origin === "https://sports-docs.invalid" ? { path: decodeURIComponent(url.pathname.slice(1)), hash: url.hash } : null;
 };
 const stateKey = value => {
  const raw = String(value || "").toLowerCase();
  return ["in progress", "in review", "in analysis", "in uat", "retrospective", "withdrawn", "proposed", "backlog", "blocked", "deferred", "ready", "done"].find(key => raw.startsWith(key))?.replaceAll(" ", "-") || "unclassified";
 };
 const priorityKey = value => ({must:"must",should:"should",could:"could","won't":"wont"}[String(value || "").toLowerCase()] || "unclassified");
 const badge = (value, prefix, key) => node("span", value || __("Not set"), `${prefix} is-${key}`);
 const styles = `
 .sports-dev-tools{display:grid;gap:24px;min-width:0;color:var(--ing-ink,#193345)}
 .sports-dev-heading{display:flex;justify-content:space-between;gap:16px;align-items:center;padding:20px 24px;border:1px solid var(--ing-line,#d5e2ec);border-radius:12px;background:var(--card-bg,#fff)}
 .sports-dev-heading h3{margin:0 0 8px;font-size:22px;line-height:1.35;font-weight:800}
 .sports-dev-heading p{margin:0;line-height:1.6;color:var(--ing-muted,#60758a)}
 .sports-dev-tools .ing-console-admin-card{padding:20px;gap:16px}
 .sports-dev-tools .ing-console-admin-card strong,.sports-dev-tools .ing-console-admin-card span{display:block;line-height:1.5}
 .sports-dev-tools .ing-console-admin-card span{margin-top:6px}
 .sports-dev-tools .sports-dev-activity{padding:20px;border:1px solid var(--ing-line,#d5e2ec);border-radius:12px;background:var(--card-bg,#fff);min-width:0}
 .sports-dev-tools .ing-console-section-head{margin-bottom:16px}
 .sports-dev-tools .ing-console-dev-tabs{margin-bottom:18px;gap:8px}
 .sports-dev-search{display:block;max-width:520px;margin:16px 0 20px;line-height:1.5;font-weight:600}
 .sports-dev-search input{display:block;width:100%;margin-top:8px;min-height:40px;padding:8px 12px;border:1px solid var(--ing-line,#cbd5e1);border-radius:8px}
 .sports-dev-tools .sports-doc-table-wrap{max-height:110vh;overflow:auto;border:1px solid var(--ing-line,#d5e2ec);border-radius:10px}
 .sports-dev-tools .sports-doc-table{width:100%;border-collapse:separate;border-spacing:0;margin:0;table-layout:auto}
 .sports-dev-tools .sports-doc-table th{position:sticky;top:0;z-index:1;padding:16px;text-align:left;background:#edf5f9;color:#193345;font-size:14px;font-weight:800;border:0;border-bottom:2px solid #d5e2ec;white-space:nowrap}
 .sports-dev-tools .sports-doc-table td{padding:18px 16px;vertical-align:top;border:0;border-bottom:1px solid #d5e2ec;font-size:14px;line-height:1.6}
 .sports-dev-tools .sports-story-table{min-width:1280px}
 .sports-story-table .sports-story-id{min-width:115px;font-weight:800;white-space:nowrap}
 .sports-story-table .sports-story-epic{min-width:100px;white-space:nowrap}
 .sports-story-table .sports-story-title{min-width:260px;max-width:360px;white-space:normal;overflow-wrap:anywhere}
 .sports-dev-tools .sports-story-table tr.ing-console-story-row td.sports-story-origin{min-width:140px;max-width:185px;white-space:normal}
 .sports-story-table .sports-story-status-cell{min-width:210px;max-width:290px}
 .sports-story-table .sports-story-priority-cell{min-width:150px;max-width:200px}
 .sports-story-table .sports-story-action-cell{min-width:220px}
 .sports-story-table .sports-story-action-cell .sports-story-controls{display:grid;grid-template-columns:max-content max-content;margin:0;align-items:center}
 .sports-story-action-cell .sports-story-feedback{grid-column:1/-1}
 .sports-story-table label{display:block;margin:0}
 .sports-story-table .sports-story-label{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
 .sports-story-table .sports-story-select{margin-top:10px;width:100%;max-width:260px}
 .sports-visually-hidden{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;overflow:hidden!important;clip-path:inset(50%);white-space:nowrap}
 .sports-story-controls{display:flex;gap:10px;flex-wrap:wrap;align-items:end;margin:0}
 .sports-story-controls button,.sports-doc-table button{min-height:34px;padding:6px 12px;white-space:nowrap}
 .sports-story-select,.sports-doc-reader input{min-height:38px;padding:8px 10px;border:1px solid #b7c8d6;border-radius:7px;background:#fff;color:#193345;font-size:14px;line-height:1.4}
 .sports-story-feedback{flex-basis:100%;max-width:250px;font-size:13px;line-height:1.5}
 .sports-status-badge,.sports-moscow-badge{display:inline-flex;align-items:center;padding:4px 10px;border:1px solid transparent;border-radius:6px;font-size:12px;font-weight:800;line-height:1.5;white-space:normal}
 .sports-moscow-badge.is-must{background:#fee2e2;color:#991b1b;border-color:#fca5a5}
 .sports-moscow-badge.is-should{background:#fef3c7;color:#854d0e;border-color:#fcd34d}
 .sports-moscow-badge.is-could{background:#dbeafe;color:#1e40af;border-color:#93c5fd}
 .sports-moscow-badge.is-wont,.sports-moscow-badge.is-unclassified{background:#f1f5f9;color:#475569;border-color:#cbd5e1}
 .sports-story-select[data-priority=must]{background:#fff1f2;color:#991b1b;border-color:#fca5a5}
 .sports-story-select[data-priority=should]{background:#fffbeb;color:#854d0e;border-color:#fcd34d}
 .sports-story-select[data-priority=could]{background:#eff6ff;color:#1e40af;border-color:#93c5fd}
 .sports-story-select[data-priority=wont]{background:#f1f5f9;color:#475569;border-color:#cbd5e1}
 .sports-status-badge{background:#fff;color:#193345;border-color:#b7c8d6}
 .sports-story-legend{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:0 0 16px;font-size:13px;line-height:1.6}
 .sports-story-legend p{flex-basis:100%;margin:0 0 4px;color:var(--ing-muted,#60758a)}
 .sports-dev-tools .sports-story-table tr.is-story-in-uat td{background:#ede9fe}
 .sports-dev-tools .sports-story-table tr.is-story-in-uat td:first-child{border-left-color:#7c3aed}
 .sports-dev-tools .sports-story-table tr.is-story-withdrawn td,.sports-dev-tools .sports-story-table tr.is-story-unclassified td{background:#f1f5f9}
 .sports-dev-tools .sports-story-table tr.is-story-withdrawn td:first-child{border-left-color:#64748b}
 .sports-doc-reader{max-width:100%;overflow-wrap:anywhere;color:var(--ing-ink,#193345);font-size:15px;line-height:1.75}
 .sports-doc-reader .sports-reader-header{padding:20px 24px;background:#f4f8fb;border:1px solid #d5e2ec;border-radius:10px;margin-bottom:24px}
 .sports-reader-header .sports-doc-path{font-size:12px;color:#60758a;margin:0 0 18px;overflow-wrap:anywhere}
 .sports-doc-reader .sports-story-controls.is-reader{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px}
 .sports-doc-reader .sports-story-controls label{display:grid;gap:8px;margin:0;font-size:13px;font-weight:700}
 .sports-doc-reader .sports-review-note,.sports-doc-reader .sports-review-actions{grid-column:1/-1}
 .sports-doc-reader .sports-review-actions{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
 .sports-doc-reader .sports-reader-help{font-size:13px;color:#60758a;margin:18px 0 0;line-height:1.6}
 .sports-document-content{max-width:100%;padding:0 12px 20px;font-size:15px;line-height:1.8}
 .sports-document-content h1{font-size:26px;line-height:1.35;margin:8px 0 24px;font-weight:800}
 .sports-document-content h2{font-size:20px;line-height:1.4;margin:32px 0 16px;padding-bottom:10px;border-bottom:1px solid #d5e2ec;font-weight:750}
 .sports-document-content h3{font-size:17px;line-height:1.5;margin:24px 0 12px}
 .sports-document-content p,.sports-document-content ul,.sports-document-content ol{margin:0 0 16px}
 .sports-document-content li{margin-bottom:8px}
 .sports-document-content td,.sports-document-content th{padding:12px 16px!important;line-height:1.6;vertical-align:top}
 @media(max-width:640px){.sports-dev-heading{padding:18px}.sports-dev-tools{gap:18px}.sports-dev-tools .sports-dev-activity{padding:14px}.sports-doc-reader .sports-reader-header{padding:16px}.sports-doc-reader .sports-story-controls.is-reader{grid-template-columns:minmax(0,1fr)}.sports-document-content{padding:0 0 16px}.sports-document-content h1{font-size:23px}}
 `;
 const storyEditors = new Set();
 const storyControls = (path, story, inReader = false) => {
  const controls = node("div", null, "sports-story-controls");
  if (inReader) controls.classList.add("is-reader");
  const select = (label, values, current) => {
   const wrap = node("label"), input = node("select", null, "form-control sports-story-select");
   wrap.append(node("span", __(label), "sports-story-label sports-visually-hidden"));
   input.setAttribute("aria-label", __(label));
   for (const value of [...new Set([current || "Not set", ...values])]) {
    const option = node("option", __(value)); option.value = value === "Not set" ? "" : value; input.append(option);
   }
   input.value = current || ""; wrap.append(input); controls.append(wrap); return input;
  };
  const state = select("Status", story.state_options, story.state);
  const priority = select("MoSCoW", story.priority_options, story.priority);
  priority.dataset.priority = priorityKey(story.priority);
  priority.addEventListener("change", () => { priority.dataset.priority = priorityKey(priority.value); }, {signal});
  const note = node("input", null, "form-control");
  if (inReader) { const label = node("label", __("Review note (optional)"), "sports-review-note"); note.maxLength = 1000; label.append(note); controls.append(label); }
  const done = node("button", story.state === "Done" ? __("Already Done") : __("Mark Done"), "btn btn-primary btn-sm"); done.type = "button"; done.disabled = story.state === "Done";
  const feedback = node("span", null, "sports-story-feedback"); feedback.setAttribute("role", "status");
  let busy = false;
  const pending = new Set();
  const apply = updated => {
   story = updated;
   if (!busy && !pending.has("state") && document.activeElement !== state) {
    if (![...state.options].some(option => option.value === story.state)) state.append(new Option(story.state,story.state));
    state.value = story.state || "";
   }
   if (!busy && !pending.has("priority") && document.activeElement !== priority) {
    if (![...priority.options].some(option => option.value === story.priority)) priority.append(new Option(story.priority || __("Not set"),story.priority || ""));
    priority.value = story.priority || "";
   }
   priority.dataset.priority = priorityKey(priority.value);
   done.textContent = story.state === "Done" ? __("Already Done") : __("Mark Done");
   done.disabled = busy || story.state === "Done";
   const row = state.closest("tr");
   if (row) row.className = `ing-console-story-row is-story-${stateKey(story.state)}`;
  };
  const editor = {path, state, apply}; storyEditors.add(editor);
  const sync = updated => {
   documents.forEach(row => { if (row.path === path) row.story = updated; });
   for (const other of storyEditors) {
    if (!other.state.isConnected) { storyEditors.delete(other); continue; }
    if (other.path === path) other.apply(updated);
   }
   if (currentPath === path && reader) {
    // Refresh only metadata text in the document, preserving controls and scroll.
    for (const [labels,value] of [[['State','Status'],updated.state],[['Priority'],updated.priority]]) {
     const item = [...reader.querySelectorAll('.sports-document-content li')].find(el => labels.some(label => el.textContent.startsWith(label+': ')));
     if (item) item.textContent = item.textContent.split(':')[0]+': '+value;
    }
   }
  };
  const savePending = async () => {
   if (busy || signal.aborted || !pending.size) return;
   const fields = [...pending]; pending.clear();
   const args = {path, revision: story.revision, note: note.value || "Reviewer updated story metadata from Sports Development Tools."};
   if (fields.includes("state") && state.value !== story.state) args.state = state.value;
   if (fields.includes("priority") && priority.value !== story.priority) args.priority = priority.value;
   if (args.state == null && args.priority == null) return;
   busy = true; done.disabled = true; feedback.textContent = __("Saving…");
   let succeeded = false;
   try {
    const updated = await call("update_story", args);
    if (signal.aborted) return;
    sync(updated); succeeded = true; feedback.textContent = __("Saved");
    frappe.show_alert({message: __("Story updated and audit logged"), indicator: "green"});
    // Refresh the document index for new audit logs without replacing visible controls.
    call("get_documents").then(result => {
     if (signal.aborted) return;
     documents = result.documents.filter(row => !row.path.endsWith("TEMPLATE.md"));
    }).catch(() => {});
   } catch (error) {
    pending.clear(); state.value = story.state || ""; priority.value = story.priority || "";
    priority.dataset.priority = priorityKey(story.priority);
    feedback.textContent = __("Update failed. Reopen the story to load the latest version before retrying.");
   } finally {
    busy = false; done.disabled = story.state === "Done";
    if (succeeded && pending.size) savePending();
   }
  };
  state.addEventListener("change", () => { pending.add("state"); savePending(); }, {signal});
  priority.addEventListener("change", () => { pending.add("priority"); savePending(); }, {signal});
  done.addEventListener("click", () => { state.value = "Done"; pending.add("state"); savePending(); }, {signal});
  if (inReader) { const actions = node("div", null, "sports-review-actions"); actions.append(done,feedback); controls.append(actions); }
  else controls.append(done, feedback);
  controls.statusField = state.closest("label"); controls.priorityField = priority.closest("label");
  return controls;
 };
 const openDocument = async (path, hash = "") => {
  if (!dialog) {
   dialog = new frappe.ui.Dialog({ title: __("Documentation"), size: "extra-large", fields: [{ fieldname: "document", fieldtype: "HTML" }] });
   reader = node("article", null, "sports-doc-reader");
   dialog.fields_dict.document.$wrapper.empty().append(reader);
   dialog.$wrapper.on("hide.bs.modal", () => { generation++; });
  }
  dialog.$wrapper.find(".modal-title").text(documents.find(row => row.path === path)?.title || path);
  dialog.show();
  const request = ++generation;
  currentPath = path;
  reader.replaceChildren(node("p", __("Loading documentation…")));
  try {
   if (/\.(png|jpe?g)$/i.test(path)) {
    const asset = await call("get_asset", { path });
    if (signal.aborted || request !== generation) return;
    const img = node("img"); img.src = asset.data_url; img.alt = path; img.style.maxWidth = "100%";
    reader.replaceChildren(node("h4", path), img); return;
   }
   const result = await call("get_document", { path });
   if (signal.aborted || request !== generation) return;
   const content = node("div", null, "sports-document-content");
   content.innerHTML = result.html; // Sanitized on the server; no arbitrary HTML source.
   const title = node("p", path, "sports-doc-path"), heading = node("header", null, "sports-reader-header");
   heading.append(title);
   if (result.story) {
    heading.append(storyControls(path, result.story, true), node("p", __("Mark Done records your review decision. It does not run verification or complete implementation automatically."), "sports-reader-help"));
   }
   reader.replaceChildren(heading, content);
   content.querySelectorAll("table").forEach(table => {
    table.classList.add("table", "table-bordered");
    table.style.minWidth = "640px";
    table.querySelectorAll("th").forEach(th => { th.style.minWidth = "110px"; });
    const wrap = node("div", null, "table-responsive"); table.replaceWith(wrap); wrap.append(table);
   });
   content.querySelectorAll("img").forEach(img => {
    const a = node("a", img.alt || __("Open screenshot")); a.href = img.getAttribute("src") || ""; img.replaceWith(a);
   });
   content.querySelectorAll("a[href]").forEach(a => {
    a.addEventListener("click", event => {
     const href = a.getAttribute("href");
     const local = localPath(href);
     if (!local) { a.target = "_blank"; a.rel = "noopener noreferrer"; return; }
     event.preventDefault();
     if (href.startsWith("#")) {
      content.querySelector(`[id="${CSS.escape(decodeURIComponent(href.slice(1)))}"]`)?.scrollIntoView();
     } else openDocument(local.path, local.hash);
    }, { signal });
   });
   if (hash) content.querySelector(`[id="${CSS.escape(decodeURIComponent(hash.slice(1)))}"]`)?.scrollIntoView();
  } catch (error) {
   if (signal.aborted || request !== generation) return;
   const retry = node("button", __("Retry"), "btn btn-default btn-sm");
   retry.addEventListener("click", () => openDocument(path, hash), { signal });
   reader.replaceChildren(node("p", __("This documentation could not be loaded.")), retry);
  }
 };
 const openButton = (path, label = "Open", primary = false) => {
  const button = node("button", __(label), `btn btn-sm btn-${primary ? "primary" : "default"}`);
  button.type = "button"; button.dataset.documentPath = path;
  button.addEventListener("click", () => openDocument(path), { signal }); return button;
 };
 const renderIndex = () => {
  index.replaceChildren();
  const term = search.value.toLowerCase().trim();
  const rows = documents.filter(row => (!category || row.category === category) && `${row.title} ${row.path}`.toLowerCase().includes(term));
  const isStories = category === "User Stories";
  const wrap = node("div", null, "table-responsive sports-doc-table-wrap ing-console-dev-activity-table");
  const table = node("table", null, `table ing-console-table sports-doc-table${isStories ? " sports-story-table" : ""}`);
  const head = node("thead"), header = node("tr");
  for (const label of (category === "User Stories" ? ["Story", "Epic", "Title", "Origin", "Status", "MoSCoW", "Action"] : ["Document", "Category", "Action"])) { const th = node("th", __(label)); th.scope = "col"; header.append(th); }
  head.append(header); table.append(head);
  const body = node("tbody");
  for (const row of rows) {
   const tr = node("tr"), title = node("td"), kind = node("td", __(row.category)), action = node("td");
   action.append(openButton(row.path));
   if (isStories && row.story) {
    const sid = row.title.match(/US-\d{3}-\d{2}/)?.[0] || row.title;
    const controls = storyControls(row.path, row.story);
    const id = node("td", sid, "sports-story-id"), epic = node("td", sid.replace(/US-(\d{3})-\d{2}/,"EPIC-$1"), "sports-story-epic");
    title.className = "sports-story-title"; title.append(node("strong", row.title.replace(/^US-\d{3}-\d{2}:\s*/,"")));
    kind.className = "sports-story-origin"; kind.textContent = row.story.origin || __("Not recorded");
    const status = node("td", null, "sports-story-status-cell"), priority = node("td", null, "sports-story-priority-cell");
    status.append(controls.statusField);
    priority.append(controls.priorityField);
    action.className = "sports-story-action-cell"; controls.prepend(action.firstChild); action.append(controls);
    tr.className = `ing-console-story-row is-story-${stateKey(row.story.state)}`;
    tr.dataset.storyPath = row.path;
    tr.append(id, epic, title, kind, status, priority, action);
   } else {
    title.append(node("strong", row.title), node("div", row.path, "text-muted"));
    if (isStories) { title.colSpan = 3; kind.colSpan = 3; }
    tr.append(title, kind, action);
   }
   body.append(tr);
  }
  table.append(body); wrap.append(table);
  if (isStories) {
   const legend = node("div", null, "sports-story-legend");
   legend.append(node("p", __("Rows follow story status colours. MoSCoW badges distinguish priority; scroll horizontally for all columns.")));
   for (const value of ["Must", "Should", "Could", "Won't"]) legend.append(badge(value,"sports-moscow-badge",priorityKey(value)));
   index.append(legend);
  }
  index.append(wrap);
  if (!rows.length) index.append(node("p", __("No matching documents."), "ing-console-empty"));
 };
 return {
  async mount(options) {
   host = options.container; signal = options.signal;
   const result = await call("get_documents");
   if (signal.aborted) return;
   documents = result.documents.filter(row => !row.path.endsWith("TEMPLATE.md"));
   const wrapper = node("section", null, "sports-dev-tools");
   const style = node("style", styles), pageHeader = node("header", null, "sports-dev-heading"), intro = node("div");
   intro.append(node("h3", __("Sports Development Tools")), node("p", __("Product documentation, requirements and delivery evidence.")));
   pageHeader.append(intro); wrapper.append(style,pageHeader);
   const kpis = node("div", null, "ing-console-requirement-kpis");
   for (const [label, value] of [["Documents", documents.length], ["Requirement Docs", documents.filter(row => row.category === "Requirements").length], ["Stories", documents.filter(row => row.category === "User Stories").length], ["Build Logs", documents.filter(row => row.category === "Build Logs").length], ["ADRs", documents.filter(row => row.category === "Architecture Decisions").length], ["Epics", documents.filter(row => row.category === "Epics").length]]) {
    const kpi = node("section", null, "ing-console-requirement-kpi"); kpi.append(node("span", __(label)), node("strong", String(value))); kpis.append(kpi);
   }
   wrapper.append(kpis);
   const cards = node("div", null, "ing-console-admin-grid");
   cards.style.gridTemplateColumns = "repeat(auto-fit,minmax(min(100%,300px),1fr))";
   for (const [title, copy, path] of [
    ["Requirements", "Current accepted rules and scope.", "REQUIREMENTS.md"],
    ["PRD", "Product scope, workflows and release gates.", "PRD.md"],
    ["Backlog", "Epic roadmap and story delivery states.", "backlog/README.md"],
    ["Build Logs", "Implementation evidence and adjustment history.", "build-logs/index.md"],
    ["Architecture Decisions", "Design choices and their reasoning.", "adr/index.md"],
    ["Development Process", "Guardrails, branches, verification and build logs.", "DEVELOPMENT_PROCESS.md"]
   ]) {
    const card = node("section", null, "ing-console-admin-card"), copyNode = node("div");
    copyNode.append(node("strong", __(title)), node("span", __(copy))); card.append(copyNode, openButton(path, "Open", true)); cards.append(card);
   }
   wrapper.append(cards);
   const activity = node("section", null, "ing-console-section sports-dev-activity");
   const heading = node("div", null, "ing-console-section-head"); heading.append(node("strong", __("Project Activity")));
   activity.append(heading);
   tabs = node("div", null, "ing-console-dev-tabs"); tabs.style.flexWrap = "wrap"; tabs.setAttribute("role", "tablist"); tabs.setAttribute("aria-label", __("Sports development activity"));
   for (const name of ["User Stories", "Requirements", "Build Logs", "Architecture Decisions", "Epics", "Guides and Product"]) {
    const tab = node("button", __(name), `ing-console-dev-tab${category === name ? " is-active" : ""}`);
    tab.type = "button"; tab.dataset.sportsDocCategory = name; tab.setAttribute("role", "tab"); tab.setAttribute("aria-selected", String(category === name));
    tab.addEventListener("click", () => {
     category = name;
     for (const item of tabs.children) { const active = item === tab; item.classList.toggle("is-active", active); item.setAttribute("aria-selected", String(active)); }
     renderIndex();
    }, { signal }); tabs.append(tab);
   }
   activity.append(tabs);
   const label = node("label", __("Search documents"), "sports-dev-search"); label.htmlFor = "sports-doc-search";
   search = node("input", null, "form-control"); search.type = "search"; search.id = label.htmlFor;
   search.addEventListener("input", renderIndex, { signal }); label.append(search); activity.append(label);
   index = node("div", null, "ing-console-dev-panel"); index.style.overflowWrap = "anywhere"; activity.append(index); wrapper.append(activity);
   host.replaceChildren(wrapper); renderIndex();
  },
  unmount() {
   generation++; storyEditors.clear();
   if (dialog) { const closing = dialog; closing.$wrapper.one("hidden.bs.modal", () => closing.$wrapper.remove()); closing.hide(); dialog = null; }
  }
 };
};
