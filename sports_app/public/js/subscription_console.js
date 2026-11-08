/* Sports subscription overview and explicit checkbox payment/reversal actions. */
frappe.sports_subscription_panel = async ({
  section,
  call,
  config,
  signal,
  state,
  offset,
  refresh,
  reset,
}) => {
  const node = (tag, text, cls) => {
    const el = document.createElement(tag);
    if (text != null) el.textContent = text;
    if (cls) el.className = cls;
    return el;
  };
  const money = (value) =>
    `${config.currency} ${Number(value || 0).toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`;
  const element = node("section", null, "sports-subscriptions");
  const style = node("style");
  style.textContent =
    ".sports-subscriptions{min-width:0}.sports-subscriptions [hidden]{display:none!important}.sports-subscription-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:16px 0}.sports-subscription-card{padding:16px;border:1px solid #d8e5de;border-left:4px solid #247455;border-radius:8px;background:#f6faf7}.sports-subscription-card strong{display:block;font-size:22px;margin-top:8px}.sports-subscriptions .grid-wrap{overflow:auto;max-width:100%}.sports-subscriptions table{border-collapse:collapse;min-width:100%;font-size:13px}.sports-subscriptions th,.sports-subscriptions td{border:1px solid #e0e5e2;padding:9px;vertical-align:top}.sports-subscriptions th{background:#edf5f0;white-space:nowrap}.sports-subscriptions td{min-width:125px}.sports-subscriptions tbody td:first-child{position:sticky;left:0;background:white;min-width:160px;z-index:1}.sports-subscriptions td.paid{background:#e8f6ec}.sports-subscriptions td.unpaid,.sports-subscriptions td.partial{background:#fff7e2}.sports-subscriptions label{display:inline-flex;align-items:center;gap:6px}.sports-subscriptions .grid-links{display:flex;flex-direction:column;gap:4px;margin-top:6px}.sports-subscriptions a{color:#1565a6;text-decoration:underline;font-weight:600}.sports-subscriptions .grid-toolbar{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0}.sports-subscriptions .grid-toolbar>label{flex-direction:column;align-items:flex-start}.sports-subscriptions input,.sports-subscriptions select{max-width:100%;padding:6px}.sports-subscriptions small{display:block;color:#59655e}.sports-subscriptions .selection-summary{font-weight:700;padding:10px;background:#edf5f0;border-radius:6px}";
  style.textContent +=
    ".sports-subscriptions .payment-month-grid{table-layout:fixed;min-width:850px;width:100%}.sports-subscriptions .payment-month-grid th,.sports-subscriptions .payment-month-grid td{min-width:0;text-align:center;width:48px;padding:10px 4px}.sports-subscriptions .payment-month-grid th:first-child,.sports-subscriptions .payment-month-grid td:first-child{width:220px;min-width:220px;text-align:left;padding:10px}.sports-subscriptions .player-label{font-weight:700}.sports-subscriptions .player-label small{font-weight:400}.sports-subscriptions .cell-documents{position:relative;font-size:12px;display:inline-block;margin-left:4px}.sports-subscriptions .cell-documents summary{cursor:pointer;list-style:none}.sports-subscriptions .cell-documents .grid-links{position:absolute;right:0;top:100%;background:white;border:1px solid #dae3dd;padding:12px;min-width:220px;z-index:5;box-shadow:0 4px 12px #0002}.sports-subscriptions .payment-month-grid input[type=checkbox]{width:16px;height:16px;accent-color:#247455}";
  style.textContent +=
    ".sports-subscription-card{--card-tone:#1d4ed8;--card-tint:#eff6ff;--card-border:#cbdcf9;background:var(--card-tint);border-color:var(--card-border);border-left-color:var(--card-tone);border-radius:12px;box-shadow:0 2px 6px #14372a08}.sports-subscription-card .card-label{color:#48566b;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}.sports-subscription-card strong{color:var(--card-tone);font-weight:750;font-variant-numeric:tabular-nums}.sports-subscription-card.tone-active{--card-tone:#0f766e;--card-tint:#f0fdfa;--card-border:#bce7df}.sports-subscription-card.tone-billed,.sports-subscription-card.tone-clear{--card-tone:#16834a;--card-tint:#f0fdf4;--card-border:#c6e8d2}.sports-subscription-card.tone-outstanding{--card-tone:#b42318;--card-tint:#fff3f2;--card-border:#f5cdca}";
  element.append(style);
  const button = (label, action) => {
    const el = node("button", __(label), "btn btn-default btn-sm");
    el.type = "button";
    el.addEventListener("click", action, { signal });
    return el;
  };
  const field = (text, type, value) => {
    const label = node("label", __(text)),
      input = node("input");
    input.type = type;
    input.value = value || "";
    input.setAttribute("aria-label", __(text));
    label.append(input);
    return { label, input };
  };
  if (config.can_read_finance === false) {
    element.append(
      node(
        "p",
        __(
          "Invoice read permission is required for subscription totals and payments. Scholarship decisions and fee plans remain available according to your Sports role."
        )
      )
    );
    return { element, has_more: false };
  }
  if (!state.year) state.year = config.current_month.slice(0, 4);
  const filters = node("div", null, "grid-toolbar"),
    year = field("Year", "number", state.year);
  year.input.min = "2000";
  year.input.max = "2099";
  filters.append(year.label);
  const search = field("Player name", "search", state.search);
  if (section === "payments") filters.append(search.label);
  filters.append(
    button("Apply filters", () => {
      state.year = year.input.value;
      state.search = search.input.value;
      return reset();
    }),
    button("Refresh", refresh)
  );
  element.append(filters);
  const [totals, paymentData] = await Promise.all([
    call("subscription_payments.overview", { year: state.year }),
    section === "payments"
      ? call("subscription_payments.grid", {
          year: state.year,
          start: offset,
          search: state.search,
        })
      : Promise.resolve(null),
  ]);
  const data = paymentData || totals;
  if (signal.aborted) return { element };
  const table = node("table"),
    head = node("thead"),
    body = node("tbody"),
    wrap = node("div", null, "grid-wrap");
  const row = (values, parent, heading = false) => {
    const tr = node("tr");
    for (const value of values) {
      const cell = node(heading ? "th" : "td");
      if (heading) cell.scope = "col";
      if (value instanceof Node) cell.append(value);
      else cell.textContent = value;
      tr.append(cell);
    }
    parent.append(tr);
    return tr;
  };
  {
    const cards = node("div", null, "sports-subscription-cards");
    for (const [label, value, tone] of [
      ["Program enrollments", totals.enrollments, "enrollments"],
      ["Active enrollments", totals.active, "active"],
      ["Billed this year", money(totals.billed), "billed"],
      [
        "Outstanding",
        money(totals.outstanding),
        Number(totals.outstanding) > 0 ? "outstanding" : "clear",
      ],
    ]) {
      const card = node("div", null, `sports-subscription-card tone-${tone}`);
      card.append(node("span", __(label), "card-label"), node("strong", value));
      cards.append(card);
    }
    element.append(
      cards,
      node(
        "p",
        __(
          "Totals use submitted monthly invoices visible to your account. Settled includes payments and accounting credits; it is not a cash-receipts total."
        )
      )
    );
    if (section === "payments")
      element.append(
        node(
          "small",
          __(
            "Year totals cover all visible enrollments; player search filters the grid only."
          )
        )
      );
  }
  if (section === "overview") {
    row(
      ["Month", "Invoices", "Billed", "Settled", "Outstanding"].map(__),
      head,
      true
    );
    for (const m of data.months)
      row(
        [
          m.month,
          m.invoices,
          money(m.billed),
          money(m.settled),
          money(m.outstanding),
        ],
        body
      );
  } else {
    const toolbar = node("div", null, "grid-toolbar"),
      date = field("Payment date", "date", data.today),
      reference = field("Bank / cash reference", "text", ""),
      bankLabel = node("label", __("Paid to")),
      bank = node("select"),
      summary = node("p", __("No months selected"), "selection-summary");
    bank.setAttribute("aria-label", __("Paid to"));
    bank.append(new Option(__("Select account"), ""));
    for (const account of data.payment_accounts)
      bank.append(new Option(account, account));
    if (data.default_payment_account) bank.value = data.default_payment_account;
    reference.input.placeholder = __("Optional — generated if blank");
    bankLabel.append(bank);
    const selected = new Map(),
      reversals = new Set();
    let reverseMode = false,
      requestKey = null;
    const update = () => {
      const total = [...selected.values()].reduce(
        (sum, c) => sum + Number(c.outstanding),
        0
      );
      summary.textContent = reverseMode
        ? `${reversals.size} ${__("receipts selected for reversal")}`
        : `${selected.size} ${__("months selected")} · ${money(total)}`;
      element.toggleAttribute(
        "data-subscription-dirty",
        !!(selected.size || reversals.size)
      );
    };
    const showResult = (results) => {
      const box = node("div");
      box.append(node("h4", __("Subscription update results")));
      for (const r of results)
        box.append(
          node(
            "p",
            `${r.month || ""} ${r.enrollment || r.receipt || ""}: ${
              r.error || r.state
            }`
          )
        );
      frappe.msgprint({ message: box.outerHTML, title: __("Subscriptions") });
    };
    const confirm = async (message) =>
      new Promise((resolve) =>
        frappe.confirm(
          message,
          () => resolve(true),
          () => resolve(false)
        )
      );
    const save = button("Save payments", async () => {
      if (!selected.size || selected.size > 20 || !bank.value) {
        frappe.msgprint(
          __("Check 1–20 months and select a Bank/Cash account.")
        );
        return;
      }
      const total = [...selected.values()].reduce(
        (sum, c) => sum + Number(c.outstanding),
        0
      );
      if (
        !(await confirm(
          __(
            "Confirm bank/cash funds received and submit receipts for the selected subscriptions?"
          ) + ` ${selected.size} · ${money(total)}`
        ))
      )
        return;
      requestKey ||= crypto.randomUUID();
      element.setAttribute("aria-busy", "true");
      save.disabled = true;
      try {
        const results = await call("subscription_payments.pay", {
          rows: [...selected.values()],
          paid_to: bank.value,
          posting_date: date.input.value,
          reference_no: reference.input.value,
          request_key: requestKey,
        });
        if (!signal.aborted) {
          await refresh();
          showResult(results);
        }
      } finally {
        element.removeAttribute("aria-busy");
        save.disabled = false;
      }
    });
    const reason = field("Reversal reason", "text", ""),
      reverse = button("Reverse selected", async () => {
        if (
          !reversals.size ||
          reversals.size > 20 ||
          !reason.input.value.trim()
        ) {
          frappe.msgprint(
            __("Select 1–20 receipts and enter a reversal reason.")
          );
          return;
        }
        if (
          !(await confirm(
            __(
              "Cancel selected subscription receipts and reopen their invoice balances?"
            )
          ))
        )
          return;
        reverse.disabled = true;
        element.setAttribute("aria-busy", "true");
        try {
          const results = await call("subscription_payments.reverse", {
            payment_entries: [...reversals],
            reason: reason.input.value,
          });
          if (!signal.aborted) {
            await refresh();
            showResult(results);
          }
        } finally {
          reverse.disabled = false;
          element.removeAttribute("aria-busy");
        }
      });
    reason.label.hidden = true;
    reverse.hidden = true;
    const toggle = button("Activate reversal", () => {
      reverseMode = !reverseMode;
      selected.clear();
      reversals.clear();
      requestKey = null;
      for (const input of body.querySelectorAll(
        "input[data-select-payment],input[data-select-reversal]"
      )) {
        const paidMarker = input.hasAttribute("data-paid-marker");
        input.checked = paidMarker && !reverseMode;
        input.disabled = input.hasAttribute("data-select-payment")
          ? reverseMode
          : !reverseMode;
        input.closest("label").hidden =
          input.hasAttribute("data-select-reversal") &&
          !paidMarker &&
          !reverseMode;
      }
      save.hidden = reverseMode;
      reason.label.hidden = !reverseMode;
      reverse.hidden = !reverseMode;
      toggle.textContent = __(
        reverseMode ? "Exit reversal" : "Activate reversal"
      );
      update();
    });
    toolbar.append(date.label, bankLabel, reference.label);
    if (data.can_pay) toolbar.append(save);
    if (data.can_reverse) toolbar.append(toggle, reason.label, reverse);
    element.append(
      node(
        "p",
        __(
          "Invoices are posted automatically after each month ends. Check received payments, then Save payments. Checked green cells are paid; Activate reversal corrects a posted receipt."
        )
      ),
      toolbar,
      summary
    );
    table.classList.add("payment-month-grid");
    row(
      [
        __("Player / program"),
        ...Array.from({ length: 12 }, (_, i) =>
          new Date(2000, i, 1).toLocaleString(undefined, { month: "short" })
        ),
      ],
      head,
      true
    );
    for (const player of data.rows) {
      const who = node("div", player.player_name, "player-label");
      who.append(node("small", `${player.player} · ${player.program}`));
      const tr = row([who], body);
      for (const cell of player.cells) {
        const td = node(
          "td",
          null,
          cell.state.toLowerCase().replaceAll(" ", "-")
        );
        td.title = `${cell.month}: ${__(cell.state)}${
          cell.amount ? " · " + money(cell.amount) : ""
        }${cell.overdue ? " · " + __("Overdue") : ""}${
          cell.issue ? " · " + cell.issue : ""
        }`;
        const key = `${player.enrollment}/${cell.month}`;
        if (
          data.can_pay &&
          ["Unpaid", "Partial"].includes(cell.state) &&
          Number(cell.outstanding) > 0
        ) {
          const label = node("label"),
            check = node("input");
          check.type = "checkbox";
          check.setAttribute("data-select-payment", "");
          check.setAttribute(
            "aria-label",
            `${__("Pay")} ${player.player_name} ${cell.month}`
          );
          check.addEventListener(
            "change",
            () => {
              requestKey = null;
              if (check.checked)
                selected.set(key, {
                  enrollment: player.enrollment,
                  month: cell.month,
                  source_hash: cell.source_hash,
                  outstanding: cell.outstanding,
                });
              else selected.delete(key);
              update();
            },
            { signal }
          );
          label.append(check);
          td.append(label);
        } else if (cell.state === "Paid") {
          const label = node("label"),
            check = node("input");
          check.type = "checkbox";
          check.checked = true;
          check.disabled = true;
          check.setAttribute(
            "aria-label",
            `${__("Paid")} ${player.player_name} ${cell.month}`
          );
          if (data.can_reverse && cell.receipts?.length === 1) {
            const receipt = cell.receipts[0];
            check.setAttribute("data-select-reversal", "");
            check.setAttribute("data-paid-marker", "");
            check.setAttribute("aria-label", `${__("Reverse")} ${receipt}`);
            check.addEventListener(
              "change",
              () => {
                check.checked
                  ? reversals.add(receipt)
                  : reversals.delete(receipt);
                update();
              },
              { signal }
            );
          }
          label.append(check);
          td.append(label);
        } else {
          const status = node(
            "span",
            ["Not billed", "Review billing", "Draft"].includes(cell.state)
              ? "…"
              : "—"
          );
          status.setAttribute("aria-label", __(cell.state));
          td.append(status);
        }

        const links = node("div", null, "grid-links");
        if (cell.invoice)
          links.append(
            frappe.sports_finance_documents.pdfLink(
              "Sales Invoice",
              cell.invoice
            )
          );
        for (const receipt of cell.receipts || []) {
          links.append(
            frappe.sports_finance_documents.pdfLink("Payment Entry", receipt)
          );
          if (
            data.can_reverse &&
            !(cell.state === "Paid" && cell.receipts.length === 1)
          ) {
            const label = node("label"),
              check = node("input");
            check.type = "checkbox";
            check.setAttribute("data-select-reversal", "");
            check.disabled = true;
            check.setAttribute("aria-label", `${__("Reverse")} ${receipt}`);
            check.addEventListener(
              "change",
              () => {
                check.checked
                  ? reversals.add(receipt)
                  : reversals.delete(receipt);
                update();
              },
              { signal }
            );
            label.hidden = true;
            label.append(check, node("span", __("Reverse receipt")));
            links.append(label);
          }
        }
        if (links.childNodes.length) {
          const details = node("details", null, "cell-documents"),
            summary = node("summary", "⋯");
          summary.setAttribute(
            "aria-label",
            `${__("Documents")} ${player.player_name} ${cell.month}`
          );
          details.append(summary, links);
          td.append(details);
        }
        tr.append(td);
      }
    }
    if (!data.rows.length)
      element.append(node("p", __("No matching player enrollments.")));
  }
  table.append(head, body);
  wrap.append(table);
  element.append(wrap);
  return { element, has_more: data.has_more };
};
