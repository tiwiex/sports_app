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
        '<style>*{box-sizing:border-box}body{margin:12px;font:14px sans-serif}main{min-width:0}</style><main id="host"></main>'
      );
      await page.evaluate(() => {
        window.__ = (s) => s;
        window.crypto.randomUUID = () => "bce0831d-a36a-4d51-9174-749c0f42513a";
        window.calls = [];
        window.paid = false;
        window.billed = true;
        window.deny = false;
        window.frappe = {
          msgprint: () => {},
          confirm: (_m, yes) => yes(),
          sports_finance_documents: {
            pdfLink: (_dt, name) => {
              const a = document.createElement("a");
              a.textContent = name + " PDF";
              a.href = "#pdf";
              return a;
            },
          },
        };
        window.call = async (method, args) => {
          window.calls.push({ method, args });
          if (method.endsWith(".overview"))
            return {
              enrollments: 3,
              active: 2,
              billed: "80000",
              outstanding: window.paid ? "0" : "40000",
              months: [
                {
                  month: "2026-11",
                  invoices: 2,
                  billed: "80000",
                  settled: "40000",
                  outstanding: "40000",
                },
              ],
            };
          if (method.endsWith(".pay")) {
            window.paid = true;
            return [
              {
                enrollment: "ENR-1",
                month: "2026-11",
                receipt: "REC-NEW",
                state: "Paid",
              },
            ];
          }
          if (method.endsWith(".reverse")) {
            window.paid = false;
            return [{ receipt: "REC-NEW", state: "Cancelled" }];
          }
          const cells = Array.from({ length: 12 }, (_, i) => ({
            month: `2026-${String(i + 1).padStart(2, "0")}`,
            state: "Not eligible",
          }));
          cells[9] = {
            month: "2026-10",
            state: window.paid
              ? "Paid"
              : window.billed
              ? "Unpaid"
              : "Not billed",
            amount: "40000",
            outstanding: window.paid ? "0" : "40000",
            source_hash: "rev",
            invoice: window.paid || window.billed ? "INV-1" : null,
            receipts: window.paid ? ["REC-NEW"] : [],
          };
          cells[10] = { month: "2026-11", state: "Not due" };
          cells[11] = { month: "2026-12", state: "Future" };
          return {
            rows: [
              {
                enrollment: "ENR-1",
                player: "PLAYER-1",
                player_name: "Sample <Player>",
                program: "Football",
                cells,
              },
            ],
            today: "2026-11-07",
            has_more: false,
            payment_accounts: ["Academy Bank"],
            default_payment_account: "Academy Bank",
            can_pay: !window.deny,
            can_generate: !window.deny,
            can_reverse: !window.deny,
          };
        };
        window.state = { year: "2026", search: "" };
        window.controller = new AbortController();
        window.mount = async (section = "payments") => {
          const p = await frappe.sports_subscription_panel({
            section,
            call: window.call,
            config: { currency: "NGN", current_month: "2026-11" },
            signal: window.controller.signal,
            state: window.state,
            offset: 0,
            refresh: () => window.mount(section),
            reset: () => window.mount(section),
          });
          document.querySelector("#host").replaceChildren(p.element);
        };
      });
      await page.addScriptTag({
        path: path.resolve(
          __dirname,
          "../../public/js/subscription_console.js"
        ),
      });
      await page.evaluate(() => window.mount("overview"));
      assert.match(await page.locator("#host").textContent(), /Outstanding/);
      assert.match(await page.locator("#host").textContent(), /NGN 40,000.00/);
      await page.evaluate(() => window.mount());
      assert.equal(await page.locator(".sports-subscription-card").count(), 4);
      assert.match(
        await page.locator(".sports-subscription-cards").textContent(),
        /Program enrollments3.*Active enrollments2.*Billed this yearNGN 80,000.00.*OutstandingNGN 40,000.00/
      );
      assert.equal(await page.locator("input[data-select-payment]").count(), 1);
      assert.equal(await page.locator("#host player").count(), 0);
      await page
        .getByRole("checkbox", {
          name: "Pay Sample <Player> 2026-10",
          exact: true,
        })
        .check();
      assert.match(
        await page.locator(".selection-summary").textContent(),
        /1 months selected.*40,000/
      );
      assert.equal(await page.locator("[data-subscription-dirty]").count(), 1);
      assert.equal(
        await page.evaluate(
          () => window.calls.filter((c) => c.method.endsWith(".pay")).length
        ),
        0
      );
      assert.equal(
        await page
          .getByRole("button", { name: "Generate invoices", exact: true })
          .count(),
        0
      );
      assert.equal(
        await page.getByLabel("Paid to", { exact: true }).inputValue(),
        "Academy Bank"
      );

      await page
        .getByRole("button", { name: "Save payments", exact: true })
        .click();
      await page
        .getByRole("checkbox", { name: "Reverse REC-NEW", exact: true })
        .waitFor();
      assert.equal(
        await page
          .getByRole("checkbox", { name: "Reverse REC-NEW", exact: true })
          .isChecked(),
        true
      );
      assert.equal(
        await page
          .getByRole("checkbox", { name: "Reverse REC-NEW", exact: true })
          .isDisabled(),
        true
      );
      await page
        .getByLabel("Documents Sample <Player> 2026-10", { exact: true })
        .click();
      await page
        .getByRole("link", { name: "REC-NEW PDF", exact: true })
        .waitFor();
      await page
        .getByLabel("Documents Sample <Player> 2026-10", { exact: true })
        .click();
      assert.match(
        await page.locator(".sports-subscription-card").last().textContent(),
        /OutstandingNGN 0.00/
      );
      const paid = await page.evaluate(() =>
        window.calls.find((c) => c.method.endsWith(".pay"))
      );
      assert.equal(paid.args.rows[0].enrollment, "ENR-1");
      assert.equal(paid.args.rows[0].source_hash, "rev");
      assert.equal(paid.args.rows[0].month, "2026-10");
      assert.equal(
        await page.evaluate(() =>
          window.calls.some((c) => c.method.endsWith(".generate_invoices"))
        ),
        false
      );
      assert.equal(paid.args.reference_no, "");
      await page
        .getByRole("button", { name: "Activate reversal", exact: true })
        .click();
      await page
        .getByRole("checkbox", { name: "Reverse REC-NEW", exact: true })
        .check();
      await page
        .getByLabel("Reversal reason", { exact: true })
        .fill("Duplicate bank confirmation");
      await page
        .getByRole("button", { name: "Reverse selected", exact: true })
        .click();
      await page
        .getByRole("checkbox", {
          name: "Pay Sample <Player> 2026-10",
          exact: true,
        })
        .waitFor();
      assert.deepEqual(
        await page.evaluate(
          () =>
            window.calls.find((c) => c.method.endsWith(".reverse")).args
              .payment_entries
        ),
        ["REC-NEW"]
      );
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth + 1
        ),
        true
      );
      assert.match(
        await page.locator(".sports-subscription-card").last().textContent(),
        /OutstandingNGN 40,000.00/
      );
      await page.getByLabel("Year", { exact: true }).fill("2025");
      await page
        .getByRole("button", { name: "Apply filters", exact: true })
        .click();
      await page.waitForFunction(() =>
        window.calls.some(
          (c) => c.method.endsWith(".overview") && c.args.year === "2025"
        )
      );
      assert.equal(await page.locator(".sports-subscription-card").count(), 4);
      await page.screenshot({
        path: `/tmp/sports-subscriptions-${width}.png`,
        fullPage: true,
      });
      await page.evaluate(() => {
        window.deny = true;
        return window.mount();
      });
      assert.equal(
        await page
          .getByRole("button", { name: "Save payments", exact: true })
          .count(),
        0
      );
      assert.equal(await page.getByRole("checkbox").count(), 0);
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log(
      "PASS subscription overview/grid desktop+phone: escaped names, checkbox staging, payment-only payload, no invoice-generation action, native receipt/PDF state, reasoned reversal, denied controls and responsive overflow; synthetic API only."
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
