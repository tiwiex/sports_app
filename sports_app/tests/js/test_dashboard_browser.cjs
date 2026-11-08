const assert = require("node:assert/strict"),
  path = require("node:path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
(async () => {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  try {
    for (const width of [1440, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 1100 } }),
        errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await page.setContent(
        '<style>*{box-sizing:border-box}body{font:14px sans-serif;margin:14px}button{padding:8px;cursor:pointer}</style><main id="host"></main>'
      );
      await page.evaluate(() => {
        window.__ = (s) => s;
        window.calls = [];
        window.mode = "full";
        window.frappe = {
          boost_console_views: {},
          provide: () => {},
          call: async (request) => {
            window.calls.push(request);
            if (window.mode === "failure") throw Error("Synthetic failure");
            if (window.mode === "restricted")
              return { message: { restricted: true } };
            const months = Array.from({ length: 12 }, (_, i) => ({
              month: `2026-${String(i + 1).padStart(2, "0")}`,
              billed: i < 10 ? "40000" : "0",
              outstanding: i < 10 ? "32000" : "0",
            }));
            return {
              message: {
                academy_name: "Academy <script>bad</script>",
                company: "Academy",
                today: "2026-11-07",
                year: Number(request.args.year || 2026),
                counts: { players: 6, active: 5, pending: 2, sessions: 4 },
                links: [
                  { view: "sports_app:players", label: "Players" },
                  {
                    view: "sports_app:billing",
                    label: "Scholarships & Billing",
                  },
                ],
                finance:
                  window.mode === "no-finance"
                    ? null
                    : {
                        currency: "NGN",
                        billed: "400000",
                        outstanding: "320000",
                        months,
                      },
                upcoming:
                  window.mode === "empty"
                    ? []
                    : [
                        {
                          name: "SPORTS-SES-1",
                          title: "Training <img src=x>",
                          session_date: "2026-11-08",
                          start_time: "10:00:00",
                          venue: "Main field",
                        },
                      ],
              },
            };
          },
        };
        document.addEventListener("click", (e) => {
          const target = e.target.closest("[data-dashboard-view]");
          if (target) window.destination = target.dataset.dashboardView;
        });
        window.controller = new AbortController();
        window.mount = async () => {
          window.view?.unmount();
          window.view = frappe.boost_console_views["sports_app:overview"]();
          await window.view.mount({
            container: document.querySelector("#host"),
            signal: window.controller.signal,
            watch: (options) => {
              window.watcher = options;
            },
          });
        };
      });
      await page.addScriptTag({
        path: path.resolve(__dirname, "../../public/js/console_overview.js"),
      });
      await page.evaluate(() => window.mount());
      assert.equal(await page.locator(".dash-card").count(), 7);
      assert.equal(await page.locator(".dash-month").count(), 12);
      assert.match(
        await page.locator(".dash-card.red").textContent(),
        /320,000.00/
      );
      assert.equal(await page.locator("#host script,#host img").count(), 0);
      assert.match(
        await page.locator(".dash-hero").textContent(),
        /Academy <script>bad<\/script>/
      );
      await page.getByRole("button", { name: "Players", exact: true }).click();
      assert.equal(
        await page.evaluate(() => window.destination),
        "sports_app:players"
      );
      await page
        .getByLabel("Billing year", { exact: true })
        .selectOption("2025");
      await page.waitForFunction(() =>
        document.querySelector(".dash-panel h4").textContent.includes("2025")
      );
      assert.equal(
        await page.evaluate(() => window.calls.at(-1).args.year),
        "2025"
      );
      await page.screenshot({
        path: `/tmp/sports-dashboard-${width}.png`,
        fullPage: true,
      });
      assert.ok(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth
        )
      );
      await page.evaluate(() => {
        window.mode = "no-finance";
        return window.mount();
      });
      assert.match(
        await page.locator(".dash-panel").first().textContent(),
        /Restricted/
      );
      assert.equal(await page.locator(".dash-chart").count(), 0);
      await page.evaluate(() => {
        window.mode = "empty";
        return window.mount();
      });
      assert.match(
        await page.locator("#host").textContent(),
        /No upcoming sessions/
      );
      await page.evaluate(() => {
        window.mode = "failure";
        return window.mount();
      });
      assert.equal(
        await page.getByRole("button", { name: "Retry dashboard" }).count(),
        1
      );
      await page.evaluate(() => (window.mode = "full"));
      await page.getByRole("button", { name: "Retry dashboard" }).click();
      await page.locator(".dash-chart").waitFor();
      await page.evaluate(() => {
        window.mode = "restricted";
        return window.mount();
      });
      assert.equal(await page.locator(".dash-card").count(), 0);
      assert.match(
        await page.locator("#host").textContent(),
        /authorized Sports role/
      );
      await page.evaluate(() => {
        window.view.unmount();
        document.querySelector("#host").textContent = "New view";
        return window.watcher.refresh();
      });
      assert.equal(await page.locator("#host").textContent(), "New view");
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log(
      "PASS academy dashboard desktop/phone: cards, chart, scope labels, escaped content, host shortcuts, year refresh, restricted/empty/error retry states, no overflow and unmount protection. Synthetic APIs; no financial writes."
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
