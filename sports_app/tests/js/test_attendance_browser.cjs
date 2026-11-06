/* Browser-page fixture globals created in page.evaluate. */
/* global calls: writable, confirmMessage: writable, fixture: writable, messages: writable, pendingConfirm: writable, result: writable, view: writable */
const assert = require("node:assert/strict"),
  path = require("node:path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
const apps = path.resolve(__dirname, "../../../..");
(async () => {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  try {
    for (const width of [1440, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 950 } });
      page.setDefaultTimeout(10000);
      const errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await page.setContent(
        '<style>*{box-sizing:border-box}body{margin:12px;font-family:sans-serif}.table{width:100%;border-collapse:collapse}.table td,.table th{padding:10px;border:1px solid #ddd}.table-responsive{overflow:auto;max-width:100%}.modal-fixture{position:fixed;inset:12px;background:white;border:1px solid #aaa;padding:16px;z-index:10000;overflow:auto}.modal-fixture label{display:block}.form-control{width:100%;min-width:110px}.modal-fixture input,.modal-fixture textarea{max-width:100%}button{cursor:pointer}</style><main class="ing-console-page"><aside class="ing-console-sidebar">Sports</aside><section class="ing-console-main"><div id="host"></div></section></main>'
      );
      await page.addStyleTag({
        path: path.join(
          apps,
          "erp_boost/erp_boost/erp_boost/page/boost_console/boost_console.css"
        ),
      });
      await page.addScriptTag({
        path: path.join(
          apps,
          "frappe/frappe/public/js/lib/jquery/jquery.min.js"
        ),
      });
      await page.evaluate(() => {
        window.__ = (s, a = []) => s.replace(/\{(\d+)\}/g, (_, i) => a[i]);
        window.calls = [];
        window.messages = [];
        window.fixture = null;
        let version = 0;
        if (!crypto.randomUUID)
          crypto.randomUUID = () => "00000000-0000-4000-8000-000000000001";
        window.result = () => ({
          session: { ...fixture },
          rows: fixture.rows.map((r) => ({ ...r })),
          counts: Object.fromEntries(
            ["Unmarked", "Present", "Late", "Absent", "Excused"].map((s) => [
              s,
              fixture.rows.filter((r) => r.status === s).length,
            ])
          ),
        });
        window.frappe = {
          boost_console_views: {},
          provide() {},
          datetime: { str_to_user: (s) => s },
          show_alert() {},
          msgprint: (s) => messages.push(s),
          confirm: (message, action) => {
            window.confirmMessage = message;
            window.pendingConfirm = action;
          },
          call: async ({ method, args = {} }) => {
            const action = method.split(".").at(-1);
            calls.push({ action, args });
            if (action === "configuration")
              return {
                message: {
                  company: "Academy",
                  timezone: "Africa/Lagos",
                  today: "2026-11-03",
                  programs: [
                    { name: "PROGRAM", program_name: "Foundation football" },
                  ],
                  groups: [],
                },
              };
            if (action === "list_sessions")
              return {
                message: {
                  rows: fixture
                    ? [{ ...fixture, program_label: "Foundation football" }]
                    : [],
                  has_more: false,
                },
              };
            if (action === "create_session") {
              fixture = {
                ...args.values,
                name: "SPORTS-SES-QA",
                status: "Scheduled",
                timezone: "Africa/Lagos",
                rows: [
                  {
                    name: "ATT-A",
                    player: "P1",
                    player_name: "Sample Player One",
                    status: "Unmarked",
                    source: "Roster",
                    modified: "v0",
                  },
                  {
                    name: "ATT-B",
                    player: "P2",
                    player_name: "Sample Player Two",
                    status: "Unmarked",
                    source: "Roster",
                    modified: "v0",
                  },
                ],
              };
              return { message: fixture.name };
            }
            if (action === "roster") return { message: result() };
            if (action === "save_attendance") {
              for (const m of args.marks) {
                const r = fixture.rows.find((r) => r.name === m.name);
                Object.assign(r, {
                  status: m.status,
                  correction_reason: m.reason,
                  modified: "v" + ++version,
                  source: "Manual",
                  marked_by: "QA coach",
                  marked_on: "2026-11-03 16:00:00",
                });
              }
              return { message: result() };
            }
            if (action === "finalize_session") {
              fixture.status = "Finalized";
              for (const r of fixture.rows)
                if (r.status === "Unmarked")
                  Object.assign(r, {
                    status: "Absent",
                    source: "Finalization",
                    modified: "v" + ++version,
                  });
              return { message: result() };
            }
            if (action === "cancel_session") {
              fixture.status = "Cancelled";
              return { message: result() };
            }
            throw Error(action);
          },
          ui: {
            Dialog: class {
              constructor(options) {
                this.fields_dict = {};
                this.el = document.createElement("section");
                this.el.className = "modal-fixture";
                this.el.role = "dialog";
                const heading = document.createElement("h2");
                heading.textContent = options.title;
                this.el.append(heading);
                for (const df of options.fields) {
                  const wrap = document.createElement("div"),
                    field = { df, $wrapper: $(wrap) };
                  if (df.fieldtype !== "HTML") {
                    const label = document.createElement("label");
                    label.textContent = df.label;
                    const input = document.createElement(
                      df.fieldtype === "Small Text" ? "textarea" : "input"
                    );
                    input.name = df.fieldname;
                    input.value = df.default || "";
                    label.append(input);
                    wrap.append(label);
                    field.input = input;
                  }
                  this.el.append(wrap);
                  this.fields_dict[df.fieldname] = field;
                }
                this.primary = document.createElement("button");
                this.primary.textContent =
                  options.primary_action_label || "Close";
                this.primary.addEventListener("click", () => {
                  const values = {};
                  for (const [k, f] of Object.entries(this.fields_dict)) {
                    if (f.input) {
                      if (f.df.reqd && !f.input.value) return;
                      values[k] = f.input.value;
                    }
                  }
                  if (options.primary_action) options.primary_action(values);
                  else this.hide();
                });
                this.el.append(this.primary);
              }
              get_value(k) {
                return this.fields_dict[k].input.value;
              }
              set_value(k, v) {
                this.fields_dict[k].input.value = v;
              }
              get_primary_btn() {
                return $(this.primary);
              }
              show() {
                document.body.append(this.el);
              }
              hide() {
                this.el.remove();
              }
            },
          },
        };
      });
      await page.addScriptTag({
        path: path.join(apps, "sports_app/sports_app/public/js/attendance.js"),
      });
      await page.evaluate(async () => {
        window.view = frappe.boost_console_views["sports_app:attendance"]();
        await view.mount({
          container: document.getElementById("host"),
          signal: new AbortController().signal,
        });
      });
      await page
        .getByRole("button", { name: "New session", exact: true })
        .click();
      await page
        .getByLabel("Session title", { exact: true })
        .fill("Saturday training");
      await page.getByLabel("Program", { exact: true }).fill("PROGRAM");
      await page
        .getByRole("button", { name: "Create session", exact: true })
        .click();
      await page
        .getByRole("button", { name: "Save attendance", exact: true })
        .waitFor();
      assert.equal(
        await page.getByText("Unmarked: 2", { exact: true }).count(),
        1
      );
      await page
        .getByRole("button", { name: "Mark unmarked Present", exact: true })
        .click();
      await page
        .getByLabel("Attendance for Sample Player Two", { exact: true })
        .selectOption("Unmarked");
      await page
        .getByRole("button", { name: "Finalize session", exact: true })
        .click();
      assert.equal(await page.evaluate(() => messages.length), 1);
      assert.equal(
        await page.evaluate(() =>
          calls.some((c) => c.action === "finalize_session")
        ),
        false
      );
      await page
        .getByRole("button", { name: "Save attendance", exact: true })
        .click();
      await page.getByText("Present: 1", { exact: true }).waitFor();
      assert.equal(
        await page.getByText("Absent: 0", { exact: true }).count(),
        1
      );
      await page
        .getByRole("button", { name: "Finalize session", exact: true })
        .click();
      assert.match(await page.evaluate(() => confirmMessage), /Absent/);
      assert.equal(
        await page.evaluate(() =>
          calls.some((c) => c.action === "finalize_session")
        ),
        false
      );
      await page.evaluate(() => pendingConfirm());
      await page.getByText("Absent: 1", { exact: true }).waitFor();
      await page
        .getByLabel("Attendance for Sample Player Two", { exact: true })
        .selectOption("Excused");
      await page
        .getByLabel("Correction reason for Sample Player Two", { exact: true })
        .fill("Guardian notified coach");
      await page
        .getByRole("button", { name: "Save attendance", exact: true })
        .click();
      await page.getByText("Excused: 1", { exact: true }).waitFor();
      assert.equal(
        await page.evaluate(
          () =>
            calls.filter((c) => c.action === "save_attendance").at(-1).args
              .marks[0].reason
        ),
        "Guardian notified coach"
      );
      assert.equal(
        await page.getByRole("link", { name: "History", exact: true }).count(),
        2
      );
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth
        ),
        true
      );
      await page
        .getByRole("dialog")
        .screenshot({ path: `/tmp/sports-attendance-${width}.png` });
      await page.getByRole("button", { name: "Close", exact: true }).click();
      await page.evaluate(() => {
        fixture.status = "Scheduled";
      });
      await page
        .getByRole("button", { name: "Refresh sessions", exact: true })
        .click();
      await page
        .getByRole("button", { name: "Saturday training", exact: true })
        .click();
      await page
        .getByRole("button", { name: "Cancel session", exact: true })
        .click();
      await page
        .getByLabel("Cancellation reason", { exact: true })
        .fill("Pitch unavailable");
      await page
        .getByRole("button", { name: "Cancel session", exact: true })
        .last()
        .click();
      await page.waitForFunction(() => fixture.status === "Cancelled");
      assert.equal(
        await page
          .getByLabel("Attendance for Sample Player One", { exact: true })
          .isDisabled(),
        true
      );
      await page.evaluate(() => view.unmount());
      assert.equal(await page.getByRole("dialog").count(), 0);
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log(
      "PASS actual attendance view at desktop/phone: create, roster, batch selection/save, explicit finalize, correction reason payload, cancel/read-only, history links, no page overflow, unmount cleanup (Dialog/API fixture)"
    );
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
