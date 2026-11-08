/* Actual Sports UI; synthetic API/Dialogs, no accounting writes. */
const assert = require("node:assert/strict"),
  path = require("node:path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
(async () => {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  try {
    for (const width of [1440, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } }),
        errors = [];
      page.on("pageerror", (error) => errors.push(error.message));
      await page.setContent(
        '<style>*{box-sizing:border-box}body{margin:12px;font:14px sans-serif}table{border-collapse:collapse;width:100%}th,td{padding:8px;border:1px solid #ddd}.modal-fixture{position:fixed;inset:12px;background:white;padding:12px;overflow:auto;border:1px solid #ccc;z-index:100}label{display:block;padding:6px}input{max-width:100%;display:block}</style><main id="host"></main>'
      );
      await page.evaluate(() => {
        window.__ = (s) => s;
        window.calls = [];
        window.messages = [];
        window.generated = false;
        window.manage = true;
        window.financeReadable = true;
        window.decisionState = 0;
        window.savedPlan = false;
        window.frappe = {
          boost_console_views: {},
          provide() {},
          router: { slug: (s) => s.toLowerCase().replaceAll(" ", "-") },
          msgprint: (s) => window.messages.push(s),
          call: async ({ method, args }) => {
            window.calls.push({ method, args });
            const action = method.split(".").at(-1);
            if (action === "overview")
              return {
                message: {
                  enrollments: 2,
                  active: 1,
                  billed: "40000",
                  outstanding: "40000",
                  months: [],
                },
              };
            if (action === "configuration")
              return {
                message: {
                  company: "Academy",
                  currency: "NGN",
                  current_month: "2026-11",
                  default_monthly_fee: 40000,
                  can_manage: window.manage,
                  can_read_finance: window.financeReadable,
                },
              };
            if (action === "plan_details")
              return {
                message: {
                  item: "NATIVE-SERVICE",
                  monthly_amount: 45000,
                  currency: "NGN",
                },
              };
            if (action === "preview")
              return {
                message: {
                  can_generate: window.manage,
                  rows: [
                    {
                      enrollment: "ENR-1",
                      player_name: "Sample One",
                      player: "PLAYER-1",
                      currency: "NGN",
                      amount: "40000.00",
                      due_date: "2026-11-07",
                      state: window.generated ? "Unpaid" : "Ready to generate",
                      source_hash: "hash1",
                      sales_invoice: window.generated ? "INV-1" : null,
                    },
                    {
                      enrollment: "ENR-2",
                      player: "PLAYER-2",
                      currency: "NGN",
                      amount: "0.00",
                      state: window.generated
                        ? "No invoice required"
                        : "Ready to generate",
                      source_hash: "hash2",
                    },
                    {
                      enrollment: "ENR-3",
                      player: "PLAYER-3",
                      state: "Exception",
                      error: "Suspended enrollment requires review",
                    },
                  ],
                  has_more: false,
                },
              };
            if (action === "generate") {
              window.generated = true;
              return {
                message: [{ obligation: "BILL-1" }, { obligation: "BILL-2" }],
              };
            }
            if (action === "records") {
              const rows =
                args.section === "plans"
                  ? window.savedPlan
                    ? [
                        {
                          name: "PLAN-1",
                          title: "Monthly football",
                          program: "PROG",
                          enabled: 1,
                          currency: "NGN",
                          monthly_amount: 40000,
                          due_day: 7,
                          effective_from: "2026-11-01",
                          joining_policy: "Full fee if active at month start",
                        },
                      ]
                    : []
                  : args.section === "decisions"
                  ? [
                      {
                        name: "DEC-1",
                        enrollment: "ENR-2",
                        player: "PLAYER-2",
                        effective_from: "2026-11-01",
                        docstatus: window.decisionState,
                        modified: "v1",
                      },
                    ]
                  : [
                      {
                        name: "BILL-1",
                        enrollment: "ENR-1",
                        player: "PLAYER-1",
                        billing_month: "2026-11",
                        amount: 40000,
                        currency: "NGN",
                        sales_invoice: "INV-1",
                      },
                    ];
              return { message: { rows, has_more: false } };
            }
            if (action === "save") {
              window.savedPlan = true;
              return { message: "PLAN-1" };
            }
            if (action === "create") return { message: "DEC-1" };
            if (action === "transition") {
              window.decisionState = args.action === "Approve" ? 1 : 2;
              return { message: "DEC-1" };
            }
            if (action === "decision")
              return {
                message: {
                  name: "DEC-1",
                  enrollment: "ENR-2",
                  reason: "Confidential synthetic reason",
                  docstatus: window.decisionState,
                  modified: "v1",
                },
              };
            throw Error(method);
          },
          ui: {
            Dialog: class {
              constructor(options) {
                this.options = options;
                this.el = document.createElement("section");
                this.el.className = "modal-fixture";
                this.el.role = "dialog";
                const h = document.createElement("h3");
                h.textContent = options.title;
                this.el.append(h);
                this.fields = {};
                for (const f of options.fields) {
                  const label = document.createElement("label");
                  label.textContent = f.label;
                  label.hidden = !!f.hidden;
                  const input = document.createElement("input");
                  input.value = f.default ?? "";
                  input.readOnly = !!f.read_only;
                  label.append(input);
                  this.el.append(label);
                  this.fields[f.fieldname] = { f, input };
                  input.addEventListener("change", () => f.onchange?.());
                }
                this.primary = document.createElement("button");
                this.primary.textContent =
                  options.primary_action_label || "Close";
                this.primary.onclick = () => {
                  if (!options.primary_action) {
                    this.hide();
                    return;
                  }
                  const values = {};
                  for (const [key, { f, input }] of Object.entries(
                    this.fields
                  )) {
                    if (f.reqd && !input.value) return;
                    values[key] = input.value;
                  }
                  options.primary_action(values);
                };
                this.el.append(this.primary);
              }
              get_value(key) {
                return this.fields[key].input.value;
              }
              async set_values(values) {
                for (const [key, value] of Object.entries(values))
                  this.fields[key].input.value = value;
              }
              show() {
                document.body.append(this.el);
              }
              hide() {
                this.el.remove();
              }
              get_primary_btn() {
                return {
                  prop: (key, value) => {
                    this.primary[key] = value;
                  },
                };
              }
            },
          },
        };
      });
      await page.addScriptTag({
        path: path.resolve(
          __dirname,
          "../../public/js/subscription_console.js"
        ),
      });
      await page.addScriptTag({
        path: path.resolve(__dirname, "../../public/js/billing.js"),
      });
      await page.evaluate(async () => {
        window.view = frappe.boost_console_views["sports_app:billing"]();
        await window.view.mount({
          container: document.querySelector("#host"),
          signal: new AbortController().signal,
        });
      });
      await page
        .getByRole("button", { name: "Monthly billing", exact: true })
        .click();
      await page.getByLabel("Billing month", { exact: true }).waitFor();
      assert.equal(
        await page.getByLabel("Billing month", { exact: true }).inputValue(),
        "2026-11"
      );
      assert.match(await page.locator("#host").textContent(), /NGN 40,000.00/);
      assert.match(
        await page.locator("#host").textContent(),
        /Suspended enrollment/
      );
      assert.equal(
        await page.evaluate(
          () =>
            window.calls.filter((c) => c.method.endsWith(".generate")).length
        ),
        0
      );
      assert.equal(
        await page
          .getByRole("button", {
            name: "Generate and submit invoices",
            exact: true,
          })
          .count(),
        0
      );
      await page
        .getByRole("button", { name: "Fee plans", exact: true })
        .click();
      await page
        .getByRole("button", { name: "New fee plan", exact: true })
        .click();
      for (const [label, value] of [
        ["Plan name", "Monthly football"],
        ["Program", "PROG"],
        ["Eligibility policy", "Full fee if active at month start"],
        ["Due day (1–28)", "7"],
        ["Service item", "MONTHLY"],
        ["Income account", "INCOME"],
        ["Cost center", "CENTER"],
      ])
        await page.getByLabel(label, { exact: true }).fill(value);
      assert.equal(
        await page.getByLabel("Monthly amount", { exact: true }).inputValue(),
        "40000"
      );
      await page
        .getByLabel("ERPNext Subscription Plan", { exact: true })
        .fill("Native monthly");
      await page
        .getByLabel("ERPNext Subscription Plan", { exact: true })
        .dispatchEvent("change");
      await page.waitForFunction(
        () =>
          document
            .querySelector('[role="dialog"]')
            .textContent.includes("ERPNext Subscription Plan") &&
          window.calls.some((c) => c.method.endsWith("plan_details"))
      );
      assert.equal(
        await page.getByLabel("Monthly amount", { exact: true }).inputValue(),
        "45000"
      );
      assert.equal(
        await page.getByLabel("Service item", { exact: true }).inputValue(),
        "NATIVE-SERVICE"
      );
      await page.getByRole("button", { name: "Save", exact: true }).click();
      await page
        .getByRole("button", { name: "Monthly football", exact: true })
        .waitFor();
      await page
        .getByRole("button", { name: "Scholarship decisions", exact: true })
        .click();
      await page.locator("summary").click();
      await page.getByRole("button", { name: "View", exact: true }).click();
      assert.equal(
        await page.getByLabel("reason", { exact: true }).inputValue(),
        "Confidential synthetic reason"
      );
      await page.getByRole("button", { name: "Close", exact: true }).click();
      await page.getByRole("button", { name: "Approve", exact: true }).click();
      await page.getByRole("button", { name: "Save", exact: true }).click();
      await page.getByText("Approved", { exact: true }).waitFor();
      await page.locator("summary").click();
      await page.getByRole("button", { name: "Revoke", exact: true }).click();
      await page
        .getByLabel("Reason for revocation", { exact: true })
        .fill("Reviewed by academy");
      await page.getByRole("button", { name: "Save", exact: true }).click();
      await page.getByText("Revoked", { exact: true }).waitFor();
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth > innerWidth
        ),
        false
      );
      await page.evaluate(async () => {
        window.view.unmount();
        window.manage = false;
        window.financeReadable = false;
        window.view = frappe.boost_console_views["sports_app:billing"]();
        await window.view.mount({
          container: document.querySelector("#host"),
          signal: new AbortController().signal,
        });
      });
      await page
        .getByRole("button", { name: "Scholarship decisions", exact: true })
        .click();
      assert.equal(
        await page
          .getByRole("button", {
            name: "New scholarship decision",
            exact: true,
          })
          .count(),
        0
      );
      await page.locator("summary").click();
      assert.equal(
        await page
          .getByRole("button", { name: "Approve", exact: true })
          .count(),
        0
      );
      assert.equal(
        await page.getByRole("button", { name: "Revoke", exact: true }).count(),
        0
      );
      await page
        .getByRole("button", { name: "Fee plans", exact: true })
        .click();
      assert.equal(
        await page
          .getByRole("button", { name: "New fee plan", exact: true })
          .count(),
        0
      );
      await page.evaluate(() => window.view.unmount());
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log(
      "PASS Sports billing desktop/phone: automatic billing status/preview without manual generation, NGN amounts, zero due/exceptions, fee-plan dialog, restricted decision view/approve/revoke and finance read-only controls; actual UI with synthetic APIs."
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
