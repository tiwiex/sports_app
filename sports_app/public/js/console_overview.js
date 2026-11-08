/* Sports-owned read-only academy dashboard using the Boost v1 view contract. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:overview"] = () => {
  const lifecycle = new AbortController();
  let host,
    year,
    revision = 0;
  const node = (tag, text, cls) => {
    const el = document.createElement(tag);
    if (text != null) el.textContent = text;
    if (cls) el.className = cls;
    return el;
  };
  const button = (label, action) => {
    const el = node("button", __(label), "btn btn-default btn-sm");
    el.type = "button";
    el.addEventListener("click", action, { signal: lifecycle.signal });
    return el;
  };
  const render = async ({ canApply = () => true } = {}) => {
    const current = ++revision;
    const data = (
      await frappe.call({
        method: "sports_app.dashboard.get_dashboard",
        args: year ? { year } : {},
      })
    ).message;
    if (lifecycle.signal.aborted || current !== revision || !canApply()) return;
    const root = node("section", null, "sports-dashboard");
    const style = node("style");
    style.textContent = `.sports-dashboard{min-width:0;color:#203b35}.sports-dashboard *{box-sizing:border-box}.sports-dashboard h3,.sports-dashboard h4{margin:0 0 12px;font-weight:700}.sports-dashboard .dash-hero{display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px;padding:24px;border-radius:14px;background:linear-gradient(120deg,#163f38,#21684f);color:white;margin-bottom:20px}.sports-dashboard .dash-hero p{margin:0;opacity:.9}.sports-dashboard .dash-toolbar{display:flex;align-items:center;flex-wrap:wrap;gap:8px}.sports-dashboard .dash-toolbar label{margin:0}.sports-dashboard select{padding:7px;border-radius:6px;color:#203b35;background:white;border:1px solid #d7e4df}.sports-dashboard .dash-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:16px 0}.sports-dashboard .dash-card{--tone:#1d4ed8;--tint:#eff6ff;padding:18px;background:var(--tint);border:1px solid #dfe7e4;border-left:4px solid var(--tone);border-radius:12px}.sports-dashboard .dash-card span{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:#4b5e68}.sports-dashboard .dash-card strong{display:block;font-size:24px;color:var(--tone);margin-top:8px;font-variant-numeric:tabular-nums;overflow-wrap:anywhere}.sports-dashboard .teal{--tone:#0f766e;--tint:#f0fdfa}.sports-dashboard .amber{--tone:#975507;--tint:#fffbeb}.sports-dashboard .green{--tone:#16834a;--tint:#f0fdf4}.sports-dashboard .red{--tone:#b42318;--tint:#fff3f2}.sports-dashboard .dash-columns{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:18px}.sports-dashboard .dash-panel{min-width:0;padding:20px;border:1px solid #e1e9e5;border-radius:12px;background:#fff;margin-bottom:18px}.sports-dashboard .dash-muted{color:#64766d;font-size:13px}.sports-dashboard .dash-actions{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 20px}.sports-dashboard .dash-actions button{border-radius:8px;font-weight:600}.sports-dashboard .dash-chart{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:8px;align-items:end;height:190px;margin-top:20px}.sports-dashboard .dash-month{display:flex;flex-direction:column;justify-content:flex-end;height:100%;min-width:0;text-align:center}.sports-dashboard .dash-track{height:150px;display:flex;align-items:flex-end;justify-content:center;gap:2px;border-bottom:1px solid #dce6e0}.sports-dashboard .dash-bar{width:42%;border-radius:4px 4px 0 0;background:#16834a}.sports-dashboard .dash-bar.balance{background:#b42318}.sports-dashboard .dash-month small{font-size:11px;margin-top:8px;color:#53685d}.sports-dashboard .dash-legend{display:flex;gap:16px;margin-top:14px;font-size:12px}.sports-dashboard .dash-legend span:before{content:'';display:inline-block;width:9px;height:9px;background:#16834a;border-radius:2px;margin-right:5px}.sports-dashboard .dash-legend span:last-child:before{background:#b42318}.sports-dashboard .dash-session{padding:12px 0;border-bottom:1px solid #edf1ef}.sports-dashboard .dash-session:last-child{border-bottom:0}.sports-dashboard .dash-session strong{display:block;margin-bottom:4px}.sports-dashboard .dash-session a{color:#1565a6;font-weight:600}.sports-dashboard .dash-error{padding:20px;background:#fff3f2;border-radius:10px;color:#b42318}@media(max-width:700px){.sports-dashboard .dash-columns{grid-template-columns:1fr}.sports-dashboard .dash-hero{padding:18px}.sports-dashboard .dash-cards{grid-template-columns:repeat(2,minmax(0,1fr))}.sports-dashboard .dash-card{padding:13px}.sports-dashboard .dash-card strong{font-size:20px}.sports-dashboard .dash-chart{gap:3px}.sports-dashboard .dash-panel{padding:14px}}`;
    root.append(style);
    if (data.restricted) {
      root.append(
        node("h3", __("Sports Academy")),
        node(
          "p",
          __(
            "Your account has console access. Academy dashboard data requires an authorized Sports role."
          )
        )
      );
      host.replaceChildren(root);
      return;
    }
    year = String(data.year);
    const hero = node("header", null, "dash-hero"),
      intro = node("div"),
      toolbar = node("div", null, "dash-toolbar");
    intro.append(
      node("h3", __("Academy at a glance")),
      node("p", `${data.academy_name || data.company} · ${data.today}`)
    );
    const label = node("label", __("Billing year")),
      select = node("select");
    select.setAttribute("aria-label", __("Billing year"));
    const currentYear = Number(data.today.slice(0, 4));
    for (let y = currentYear; y >= 2000; y--)
      select.append(new Option(String(y), String(y)));
    select.value = year;
    select.addEventListener(
      "change",
      () => {
        year = select.value;
        return refresh();
      },
      { signal: lifecycle.signal }
    );
    toolbar.append(label, select, button("Refresh dashboard", refresh));
    hero.append(intro, toolbar);
    root.append(hero);
    const cards = (values) => {
      const list = node("div", null, "dash-cards");
      for (const [label, value, tone] of values) {
        const card = node("div", null, `dash-card ${tone || ""}`);
        card.append(
          node("span", __(label)),
          node("strong", value == null ? __("Restricted") : value)
        );
        list.append(card);
      }
      return list;
    };
    root.append(
      cards([
        ["Players", data.counts.players, ""],
        ["Active enrollments", data.counts.active, "teal"],
        ["Pending applications", data.counts.pending, "amber"],
        ["Sessions this month", data.counts.sessions, "teal"],
      ])
    );
    root.append(
      node(
        "p",
        __(
          "Operational counts show current records. Sessions exclude cancellations and use the academy's current calendar month."
        ),
        "dash-muted"
      )
    );
    const actions = node("nav", null, "dash-actions");
    actions.setAttribute("aria-label", __("Academy shortcuts"));
    for (const link of data.links) {
      const b = button(link.label, () => {});
      // Existing host dashboard navigation contract, scoped by server capabilities.
      b.dataset.dashboardView = link.view;
      actions.append(b);
    }
    root.append(actions);
    const columns = node("div", null, "dash-columns"),
      finance = node("section", null, "dash-panel"),
      sessions = node("section", null, "dash-panel");
    finance.append(node("h4", `${__("Monthly subscriptions")} · ${year}`));
    if (data.finance) {
      const f = data.finance;
      const money = (value) =>
        `${f.currency} ${Number(value || 0).toLocaleString(undefined, {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        })}`;
      const settled = Number(f.billed) - Number(f.outstanding);
      finance.append(
        cards([
          ["Billed", money(f.billed), "green"],
          ["Settled", money(settled), "teal"],
          [
            "Outstanding",
            money(f.outstanding),
            Number(f.outstanding) > 0 ? "red" : "green",
          ],
        ])
      );
      finance.append(
        node(
          "p",
          __(
            "Submitted monthly invoices visible to your account. Settled includes payments and accounting credits; it is not cash received."
          ),
          "dash-muted"
        )
      );
      const chart = node("div", null, "dash-chart"),
        maximum = Math.max(
          1,
          ...f.months.map((m) =>
            Math.max(Number(m.billed), Number(m.outstanding))
          )
        );
      chart.setAttribute("role", "group");
      chart.setAttribute(
        "aria-label",
        __(
          "Monthly billed and outstanding subscriptions; each month lists its amounts."
        )
      );
      for (const m of f.months) {
        const month = node("div", null, "dash-month"),
          track = node("div", null, "dash-track");
        const description = `${m.month}: ${__("Billed")} ${money(
          m.billed
        )}; ${__("Outstanding")} ${money(m.outstanding)}`;
        month.title = description;
        month.setAttribute("aria-label", description);
        month.tabIndex = 0;
        for (const [value, cls] of [
          [m.billed, ""],
          [m.outstanding, "balance"],
        ]) {
          const bar = node("div", null, `dash-bar ${cls}`);
          bar.style.height = `${(Math.max(0, Number(value)) / maximum) * 100}%`;
          track.append(bar);
        }
        month.append(
          track,
          node(
            "small",
            new Date(
              Number(year),
              Number(m.month.slice(-2)) - 1,
              1
            ).toLocaleString(undefined, { month: "short" })
          )
        );
        chart.append(month);
      }
      const legend = node("div", null, "dash-legend");
      legend.append(
        node("span", __("Billed")),
        node("span", __("Outstanding"))
      );
      finance.append(chart, legend);
      if (!Number(f.billed))
        finance.append(
          node(
            "p",
            __("No submitted monthly invoices for this year."),
            "dash-muted"
          )
        );
    } else
      finance.append(
        node(
          "p",
          __(
            "Restricted — subscription totals require Sports billing access and native invoice read permission."
          ),
          "dash-muted"
        )
      );
    sessions.append(
      node("h4", __("Upcoming sessions")),
      node("p", __("Next five scheduled sessions from today."), "dash-muted")
    );
    if (data.upcoming == null)
      sessions.append(
        node(
          "p",
          __("Restricted — session read access is required."),
          "dash-muted"
        )
      );
    else if (!data.upcoming.length)
      sessions.append(
        node("p", __("No upcoming sessions scheduled."), "dash-muted")
      );
    else
      for (const s of data.upcoming) {
        const item = node("div", null, "dash-session"),
          a = node("a", s.title);
        a.href = `/app/sports-session/${encodeURIComponent(s.name)}`;
        const strong = node("strong");
        strong.append(a);
        item.append(
          strong,
          node("div", `${s.session_date} · ${s.start_time}`),
          node("small", s.venue || __("Venue not set"), "dash-muted")
        );
        sessions.append(item);
      }
    columns.append(finance, sessions);
    root.append(columns);
    host.replaceChildren(root);
  };
  const refresh = async (options) => {
    const expected = revision + 1;
    try {
      await render(options);
    } catch (error) {
      if (lifecycle.signal.aborted || revision !== expected) return;
      const box = node("div", null, "sports-dashboard"),
        notice = node("div", null, "dash-error");
      notice.setAttribute("role", "alert");
      notice.append(
        node(
          "p",
          __(
            "Dashboard could not be loaded. Check academy setup and access, then retry."
          )
        ),
        button("Retry dashboard", refresh)
      );
      box.append(notice);
      host.replaceChildren(box);
      console.error("Sports dashboard load failed", error);
    }
  };
  return {
    async mount(options) {
      host = options.container;
      if (options.signal.aborted) return;
      options.signal.addEventListener("abort", () => lifecycle.abort(), {
        once: true,
        signal: lifecycle.signal,
      });
      host.replaceChildren(node("p", __("Loading academy dashboard…")));
      await refresh();
      options.watch?.({
        doctypes: [
          "Sports Player",
          "Sports Enrollment",
          "Sports Registration",
          "Sports Session",
          "Sports Billing Obligation",
          "Sales Invoice",
          "Payment Entry",
        ],
        refresh,
      });
    },
    unmount() {
      revision++;
      lifecycle.abort();
    },
  };
};
