/* Actual Sports profile module, synthetic APIs/controls; no ERP writes. */
const assert = require("node:assert/strict"),
  path = require("node:path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
(async () => {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  try {
    for (const width of [1440, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 950 } }),
        errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await page.setContent(
        '<style>*{box-sizing:border-box}body{margin:12px;font-family:sans-serif}.player-card{border:1px solid #ccc;padding:14px;margin-bottom:14px}.player-actions{display:flex;gap:8px;margin:12px 0;flex-wrap:wrap}.table-responsive{overflow:auto;max-width:100%}table{border-collapse:collapse;width:100%}td,th{padding:8px;border:1px solid #ccc;white-space:nowrap}.modal-fixture{position:fixed;inset:16px;background:white;z-index:100;overflow:auto;padding:14px;border:1px solid #ccc}label{display:block;margin:12px 0}input{display:block;max-width:100%}</style><main id="host"></main>'
      );
      await page.evaluate(() => {
        window.__ = (s) => s;
        let serial = 0;
        window.crypto.randomUUID = () =>
          `9dca7dcc-8e25-41bc-81a5-${String(++serial).padStart(12, "0")}`;
        window.calls = [];
        window.messages = [];
        window.restricted = false;
        window.measurements = [];
        window.documents = [];
        window.frappe = {
          sports_player_profile: {},
          provide() {},
          datetime: { str_to_user: (s) => s },
          router: { slug: (s) => s.toLowerCase().replaceAll(" ", "-") },
          msgprint: (s) => window.messages.push(s),
          call: async ({ method, args }) => {
            const action = method.split(".").at(-1);
            window.calls.push({ action, args });
            if (action === "overview")
              return {
                message: {
                  age: 10,
                  portrait: "/private/files/player-photo.jpg",
                  preferred_foot: "Left",
                  today: "2026-11-06",
                  modified: "v1",
                  can_edit_foot: true,
                  can_add_measurement: true,
                  can_add_document: !window.restricted,
                  available: {
                    invoices: !window.restricted,
                    receipts: !window.restricted,
                    attendance: true,
                    biometrics: !window.restricted,
                    measurements: true,
                    documents: !window.restricted,
                  },
                  outstanding: [
                    { currency: "NGN", outstanding: 250000 },
                    { currency: "USD", outstanding: 20 },
                  ],
                },
              };
            if (action === "history") {
              let rows = [];
              if (args.section === "invoices")
                rows = [
                  {
                    name: args.start ? "INV-21" : "INV-1",
                    posting_date: "2026-11-06",
                    currency: "NGN",
                    grand_total: 250000,
                    outstanding_amount: 250000,
                    status: "Unpaid",
                    docstatus: 1,
                  },
                ];
              if (args.section === "receipts")
                rows = [
                  {
                    name: "PAY-1",
                    payment_type: "Receive",
                    paid_amount: 10,
                    received_amount: 10,
                    paid_from_account_currency: "USD",
                    paid_to_account_currency: "USD",
                    docstatus: 0,
                  },
                ];
              if (args.section === "attendance")
                rows = [
                  {
                    name: "ATT-1",
                    session: "SESSION-1",
                    session_title: "Training",
                    session_date: "2026-11-06",
                    session_status: "Scheduled",
                    status: "Present",
                    source: "Manual",
                  },
                ];
              if (args.section === "biometrics")
                rows = [
                  {
                    name: "BIO-1",
                    status: "Pending capture",
                    finger: "Right thumb",
                    demo_reference: "DEMO-123",
                  },
                ];
              if (args.section === "measurements") rows = window.measurements;
              if (args.section === "documents") rows = window.documents;
              return {
                message: {
                  rows,
                  has_more: args.section === "invoices" && !args.start,
                },
              };
            }
            if (action === "save_preferred_foot") return { message: "v2" };
            if (action === "add_measurement") {
              window.measurements = [
                { ...args, name: "MEASURE-1", recorded_by: "Staff" },
              ];
              return { message: "MEASURE-1" };
            }
            if (action === "add_document") {
              window.documents = [
                {
                  ...args,
                  name: "DOC-1",
                  file_url: "/private/files/sample.pdf",
                },
              ];
              return { message: "DOC-1" };
            }
            throw Error(action);
          },
          ui: {
            Dialog: class {
              constructor(options) {
                this.options = options;
                this.fields_dict = {};
                this.el = document.createElement("section");
                this.el.className = "modal-fixture";
                this.el.role = "dialog";
                const h = document.createElement("h2");
                h.textContent = options.title;
                this.el.append(h);
                for (const df of options.fields) {
                  const wrap = document.createElement("div");
                  let input;
                  if (df.fieldtype !== "HTML") {
                    const label = document.createElement("label");
                    label.textContent = df.label;
                    input = document.createElement("input");
                    input.name = df.fieldname;
                    input.value = df.default || "";
                    label.append(input);
                    wrap.append(label);
                  }
                  this.fields_dict[df.fieldname] = {
                    df,
                    input,
                    $wrapper: { append: (node) => wrap.append(node) },
                  };
                  this.el.append(wrap);
                }
                this.primary = document.createElement("button");
                this.primary.textContent = options.primary_action_label;
                this.primary.onclick = () => {
                  const values = {};
                  for (const [key, field] of Object.entries(this.fields_dict)) {
                    if (field.input) {
                      if (field.df.reqd && !field.input.value) return;
                      values[key] = field.input.value;
                    }
                  }
                  options.primary_action(values);
                };
                this.el.append(this.primary);
              }
              show() {
                document.body.append(this.el);
              }
              hide() {
                this.el.remove();
              }
              get_primary_btn() {
                return {
                  prop: (name, value) => {
                    this.primary[name] = value;
                  },
                };
              }
            },
          },
        };
        window.controller = new AbortController();
      });
      await page.addScriptTag({
        path: path.resolve(__dirname, "../../public/js/player_profile.js"),
      });
      await page.evaluate(async () => {
        const hero = document.createElement("header");
        hero.className = "player-hero";
        const portraitTarget = document.createElement("div");
        hero.append(portraitTarget);
        document.querySelector("#host").append(hero);
        const panels = window.frappe.sports_player_profile.create_tabs(
          document.querySelector("#host")
        );
        const container = document.createElement("div");
        panels.details.append(container);
        await window.frappe.sports_player_profile.mount({
          container,
          panels,
          portraitTarget,
          name: "PLAYER-1",
          signal: window.controller.signal,
        });
      });
      assert.equal(
        await page.getByText("Age today: 10", { exact: true }).count(),
        1
      );
      assert.equal(
        await page.getByRole("tab", { selected: true }).textContent(),
        "Player details"
      );
      assert.equal(await page.locator('[role="tabpanel"]:visible').count(), 1);
      await page
        .getByRole("tab", { name: "Invoices & receipts", exact: true })
        .click();
      assert.equal(
        await page.getByRole("img", { name: "Player portrait" }).isVisible(),
        true
      );
      assert.equal(await page.locator(".player-hero img").count(), 1);
      assert.equal(
        await page.evaluate(
          () =>
            document.querySelector(".player-hero").getBoundingClientRect().top <
            document.querySelector('[role="tablist"]').getBoundingClientRect()
              .top
        ),
        true
      );
      const balance = page.locator("section").filter({
        has: page.getByRole("heading", {
          name: "Outstanding by invoice currency",
          exact: true,
        }),
      });
      assert.match(await balance.textContent(), /NGN 250,000.00/);
      assert.match(await balance.textContent(), /USD 20.00/);
      assert.match(
        await page.locator('[data-history="biometrics"]').textContent(),
        /simulated/
      );
      const before = await page.evaluate(
        () =>
          window.calls.filter(
            (c) => c.action === "history" && c.args.section === "attendance"
          ).length
      );
      await page
        .locator('[data-history="invoices"]')
        .getByRole("button", { name: "More", exact: true })
        .click();
      await page.getByRole("link", { name: "INV-21", exact: true }).waitFor();
      assert.equal(
        await page.evaluate(
          () =>
            window.calls.filter(
              (c) => c.action === "history" && c.args.section === "attendance"
            ).length
        ),
        before
      );
      await page
        .getByRole("tab", { name: "Player details", exact: true })
        .click();
      await page
        .getByRole("button", { name: "Update preferred foot", exact: true })
        .click();
      await page.getByLabel("Preferred foot", { exact: true }).fill("Right");
      await page.getByRole("button", { name: "Save", exact: true }).click();
      await page.getByText("Preferred foot: Right", { exact: true }).waitFor();
      await page
        .getByRole("tab", { name: "Measurements", exact: true })
        .click();
      await page
        .getByRole("button", { name: "Add measurement", exact: true })
        .click();
      await page.getByLabel("Height (cm)", { exact: true }).fill("142.75");
      await page.getByLabel("Weight (kg)", { exact: true }).fill("35");
      await page.getByRole("button", { name: "Save", exact: true }).click();
      await page
        .getByRole("link", { name: "MEASURE-1", exact: true })
        .waitFor();
      await page.getByRole("tab", { name: "Documents", exact: true }).click();
      await page
        .getByRole("button", { name: "Add private document", exact: true })
        .click();
      await page.getByLabel("Title", { exact: true }).fill("Birth record");
      await page.getByRole("button", { name: "Save", exact: true }).click();
      await page.waitForFunction(() => window.messages.length === 1);
      assert.equal(await page.getByRole("dialog").count(), 1);
      await page
        .getByLabel("Private supporting file", { exact: true })
        .setInputFiles({
          name: "birth.pdf",
          mimeType: "application/pdf",
          buffer: Buffer.from("synthetic UI file"),
        });
      await page.getByRole("button", { name: "Save", exact: true }).click();
      await page
        .getByRole("link", { name: "View private document", exact: true })
        .waitFor();
      assert.equal(
        await page
          .getByRole("link", { name: "View private document", exact: true })
          .getAttribute("href"),
        "/private/files/sample.pdf"
      );
      const uploaded = await page.evaluate(
        () => window.calls.find((c) => c.action === "add_document").args
      );
      assert.match(uploaded.file_data, /^data:application\/pdf;base64,/);
      assert.equal(uploaded.name, "PLAYER-1");
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth > innerWidth
        ),
        false
      );
      await page.evaluate(async () => {
        window.controller.abort();
        window.controller = new AbortController();
        window.restricted = true;
        window.calls = [];
        document.querySelector("#host").replaceChildren();
        const hero = document.createElement("header");
        hero.className = "player-hero";
        const portraitTarget = document.createElement("div");
        hero.append(portraitTarget);
        document.querySelector("#host").append(hero);
        const panels = window.frappe.sports_player_profile.create_tabs(
          document.querySelector("#host")
        );
        const container = document.createElement("div");
        panels.details.append(container);
        await window.frappe.sports_player_profile.mount({
          container,
          panels,
          portraitTarget,
          name: "PLAYER-1",
          signal: window.controller.signal,
        });
      });
      for (const section of [
        "documents",
        "biometrics",
        "invoices",
        "receipts",
      ]) {
        assert.match(
          await page.locator(`[data-history="${section}"]`).textContent(),
          /Restricted/
        );
        assert.equal(
          await page.evaluate(
            (s) =>
              window.calls.filter(
                (c) => c.action === "history" && c.args.section === s
              ).length,
            section
          ),
          0
        );
      }
      assert.equal(
        await page
          .getByRole("link", { name: "View private document", exact: true })
          .count(),
        0
      );
      await page
        .getByRole("tab", { name: "Player details", exact: true })
        .focus();
      await page.keyboard.press("ArrowRight");
      assert.equal(
        await page.getByRole("tab", { selected: true }).textContent(),
        "Program enrollments"
      );
      await page.keyboard.press("End");
      assert.equal(
        await page.getByRole("tab", { selected: true }).textContent(),
        "Documents"
      );
      await page.keyboard.press("Home");
      assert.equal(
        await page.getByRole("tab", { selected: true }).textContent(),
        "Player details"
      );
      assert.equal(await page.locator('[role="tabpanel"]:visible').count(), 1);
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth > innerWidth
        ),
        false
      );
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log(
      "PASS desktop/phone central profile: separate currency balances, independently paginated histories, preferences/measurements/private upload, restricted sections without requests/URLs and responsive layout. Actual JS; synthetic API/controls."
    );
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
