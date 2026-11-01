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
 const openDocument = async (path, hash = "") => {
  if (!dialog) {
   dialog = new frappe.ui.Dialog({ title: __("Documentation"), size: "extra-large", fields: [{ fieldname: "document", fieldtype: "HTML" }] });
   reader = node("article"); reader.style.cssText = "max-width:100%;overflow-wrap:anywhere";
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
   const title = node("p", path, "text-muted");
   reader.replaceChildren(title, content);
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
  const wrap = node("div", null, "table-responsive");
  const table = node("table", null, "table table-bordered");
  const head = node("thead"), header = node("tr");
  for (const label of ["Document", "Category", "Action"]) header.append(node("th", __(label)));
  head.append(header); table.append(head);
  const body = node("tbody");
  for (const row of rows) {
   const tr = node("tr"), title = node("td"), kind = node("td", __(row.category)), action = node("td");
   title.append(node("strong", row.title), node("div", row.path, "text-muted"));
   action.append(openButton(row.path)); tr.append(title, kind, action); body.append(tr);
  }
  table.append(body); wrap.append(table); index.append(wrap);
  if (!rows.length) index.append(node("p", __("No matching documents."), "ing-console-empty"));
 };
 return {
  async mount(options) {
   host = options.container; signal = options.signal;
   const result = await call("get_documents");
   if (signal.aborted) return;
   documents = result.documents.filter(row => !row.path.endsWith("TEMPLATE.md"));
   const wrapper = node("section"); wrapper.style.minWidth = "0";
   wrapper.append(node("h3", __("Sports Development Tools")), node("p", __("Product documentation, requirements and delivery evidence."), "text-muted"));
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
   const activity = node("section", null, "ing-console-section");
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
   const label = node("label", __("Search documents")); label.htmlFor = "sports-doc-search";
   search = node("input", null, "form-control"); search.type = "search"; search.id = label.htmlFor;
   search.addEventListener("input", renderIndex, { signal }); activity.append(label, search);
   index = node("div", null, "ing-console-dev-panel"); index.style.overflowWrap = "anywhere"; activity.append(index); wrapper.append(activity);
   host.replaceChildren(wrapper); renderIndex();
  },
  unmount() {
   generation++;
   if (dialog) { const closing = dialog; closing.$wrapper.one("hidden.bs.modal", () => closing.$wrapper.remove()); closing.hide(); dialog = null; }
  }
 };
};
