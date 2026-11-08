/* Actual rendered public template, CSS and JS; synthetic APIs, no ERP writes.
 * SPORTS_ACADEMY_HTML points to a development-rendered academy.html fixture.
 */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
(async () => {
  const html = fs.readFileSync(process.env.SPORTS_ACADEMY_HTML, "utf8");
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  try {
    for (const width of [1440, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 950 } }),
        errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await page.route("https://academy.test/**", async (route) => {
        const url = new URL(route.request().url());
        if (url.pathname === "/academy")
          return route.fulfill({ contentType: "text/html", body: html });
        if (url.pathname.endsWith("/academy.js"))
          return route.fulfill({
            contentType: "application/javascript",
            path: path.resolve(__dirname, "../../public/js/academy.js"),
          });
        if (url.pathname.endsWith("/academy.css"))
          return route.fulfill({
            contentType: "text/css",
            path: path.resolve(__dirname, "../../public/css/academy.css"),
          });
        if (url.pathname.includes("check_player_email"))
          return route.fulfill({ json: { message: { available: true } } });
        if (url.pathname.includes("make_payment"))
          return route.fulfill({
            json: {
              message: {
                reference: "ACC-SINV-QA-1",
                token: "synthetic",
                document_type: "Sales Invoice",
                state: "Draft",
                currency: "NGN",
                total: 250000,
                monthly_fee: 40000,
                bank: "Synthetic Bank",
                account_number: "0000000000",
                account_name: "Synthetic Academy",
                charges: [
                  {
                    item_name: "Training fee",
                    qty: 2,
                    rate: 100000,
                    amount: 200000,
                  },
                  {
                    item_name: "Academy kit",
                    qty: 1,
                    rate: 30000,
                    amount: 30000,
                  },
                  {
                    item_name: "<img src=x onerror=alert(1)>",
                    qty: 1,
                    rate: 20000,
                    amount: 20000,
                  },
                ],
              },
            },
          });
        return route.fulfill({ status: 204, body: "" });
      });
      await page.goto("https://academy.test/academy");
      await page
        .getByRole("button", { name: "Find your place", exact: true })
        .click();
      await page
        .getByRole("button", { name: "Proceed to registration" })
        .click();
      for (const [name, value] of Object.entries({
        first_name: "Synthetic",
        last_name: "Applicant",
        birth_date: "2015-01-01",
        contact_email: "player@example.invalid",
        guardian_name: "Synthetic Guardian",
        guardian_phone: "0000000000",
        guardian_email: "guardian@example.invalid",
        home_address: "Synthetic QA address",
      }))
        await page
          .locator('#enrollment-form [name="' + name + '"]')
          .fill(value);
      await page.locator('[name="gender"]').selectOption("Girl");
      await page
        .getByRole("button", { name: "Make Payment", exact: false })
        .click();
      await page
        .getByRole("heading", { name: "Payment", exact: true })
        .waitFor();
      assert.equal(
        await page.locator("#enrollment-charge-rows > div").count(),
        3
      );
      assert.match(
        await page.locator("#enrollment-charge-rows").textContent(),
        /Training fee \(2 ×/
      );
      assert.match(
        await page.locator("#enrollment-charge-rows").textContent(),
        /<img src=x onerror=alert\(1\)>/
      );
      assert.equal(
        await page.locator("#enrollment-charge-rows img").count(),
        0
      );
      assert.match(await page.locator("#fee-total").textContent(), /250,000/);
      assert.equal(
        await page.locator("#payment-reference").textContent(),
        "ACC-SINV-QA-1"
      );
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
      "PASS public enrollment desktop/phone: actual template/CSS/JS, three configured rows, quantity/rate labels, NGN total, invoice reference and escaped Item names; synthetic endpoints, no ERP writes."
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
