/* Browser-page fixture globals created in page.evaluate. */
/* global draw: writable */
const assert = require("node:assert/strict"),
  path = require("node:path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
const apps = path.resolve(__dirname, "../../../..");
(async () => {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  try {
    for (const width of [1440, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 950 } }),
        errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await page.setContent(
        '<style>body{font-family:sans-serif;margin:12px}.fixture{width:292px;background:#153f68;color:white;padding:16px}button{cursor:pointer}.ing-console-nav-item{display:block;width:100%;border:0;background:transparent;text-align:left;color:white;padding:8px}.ing-console-nav-group-title{width:100%}</style><div class="fixture"><div id="menu" class="ing-console-nav-groups"></div></div>'
      );
      await page.addStyleTag({
        path: path.join(
          apps,
          "erp_boost/erp_boost/erp_boost/page/boost_console/boost_console.css"
        ),
      });
      await page.evaluate(() => {
        window.badgeCalls = 0;
        window.badgeCount = 31;
        window.failCounts = false;
        window.badgeEvents = {};
        window.frappe = {
          call: async () => {
            window.badgeCalls++;
            if (window.failCounts) throw new Error("denied");
            return {
              message: {
                "sports_app:players": {
                  count: window.badgeCount,
                  title: "Players — Academy",
                },
              },
            };
          },
          realtime: {
            on: (name, callback) => {
              window.badgeEvents[name] = callback;
            },
          },
        };
        window.draw = (sports) => {
          const native = ["Dashboard", "Sales"]
            .map(
              (label, index) =>
                `<div class="ing-console-nav-group"><button class="ing-console-nav-group-title" data-nav-group="${label}">${label}</button><div class="ing-console-nav-items"><button class="ing-console-nav-item" data-view="core-${index}">${label} item</button></div></div>`
            )
            .join("");
          document.querySelector("#menu").innerHTML =
            native +
            (sports
              ? '<div class="ing-console-nav-group"><button class="ing-console-nav-group-title" data-nav-group="Sports">Sports</button><div class="ing-console-nav-items"><button class="ing-console-nav-item is-active" data-view="sports_app:overview">Sports Academy</button><button class="ing-console-nav-item" data-view="sports_app:players">Players</button></div></div>'
              : "");
          document
            .querySelectorAll("[data-nav-group]")
            .forEach((button) =>
              button.addEventListener("click", () =>
                button.parentElement.classList.toggle("is-collapsed")
              )
            );
        };
        draw(false);
      });
      await page.addScriptTag({
        path: path.join(
          apps,
          "sports_app/sports_app/public/js/console_navigation.js"
        ),
      });
      await page.waitForTimeout(50);
      assert.equal(await page.locator(".sports-console-navigation").count(), 0);
      assert.deepEqual(
        await page.locator("[data-nav-group]").allTextContents(),
        ["Dashboard", "Sales"]
      );
      assert.equal(await page.evaluate(() => window.badgeCalls), 0);
      await page.evaluate(() => draw(true));
      await page.waitForFunction(
        () =>
          document
            .querySelector("#menu")
            .firstElementChild.querySelector("[data-nav-group]").textContent ===
          "Sports"
      );
      assert.deepEqual(
        await page.locator("[data-nav-group]").allTextContents(),
        ["Sports", "Dashboard", "Sales"]
      );
      assert.equal(await page.locator(".sports-nav-extension").count(), 1);
      assert.equal(await page.locator(".sports-nav-core").count(), 2);
      assert.equal(
        await page.locator("#menu > .ing-console-nav-group").count(),
        2
      );
      assert.equal(
        await page.locator(".sports-nav-boost .sports-nav-core").count(),
        2
      );
      await page.waitForFunction(
        () => document.querySelector(".sports-nav-count")?.textContent === "31"
      );
      assert.match(
        await page.locator(".sports-nav-count").getAttribute("aria-label"),
        /Players.*31/
      );
      const calls = await page.evaluate(() => window.badgeCalls);
      await page.waitForTimeout(100);
      assert.equal(await page.evaluate(() => window.badgeCalls), calls);
      await page.evaluate(() => {
        window.badgeCount = 32;
        window.badgeEvents.list_update({ doctype: "Sports Player" });
      });
      await page.waitForFunction(
        () => document.querySelector(".sports-nav-count")?.textContent === "32"
      );
      const boost = page.locator("[data-sports-boost-toggle]");
      assert.equal(await boost.getAttribute("aria-expanded"), "true");
      await boost.click();
      assert.equal(await boost.getAttribute("aria-expanded"), "false");
      assert.equal(await page.locator("[data-view=core-1]").isVisible(), false);
      await boost.click();
      assert.equal(await page.locator("[data-view=core-1]").isVisible(), true);
      await page.locator("[data-nav-group=Sales]").click();
      assert.equal(await page.locator("[data-view=core-1]").isVisible(), false);
      await page.locator("[data-nav-group=Sales]").click();
      const sports = page.locator("[data-nav-group=Sports]"),
        native = page.locator("[data-sports-boost-toggle]");
      assert.notEqual(
        await sports.evaluate((el) => getComputedStyle(el).backgroundColor),
        await native.evaluate((el) => getComputedStyle(el).backgroundColor)
      );
      assert.ok(
        await page
          .locator('[data-view="sports_app:players"]')
          .evaluate(
            (el) =>
              el.getBoundingClientRect().left >
              el
                .closest(".ing-console-nav-group")
                .querySelector("[data-nav-group]")
                .getBoundingClientRect().left
          )
      );
      await sports.click();
      assert.equal(
        await page.locator(".sports-nav-extension.is-collapsed").count(),
        1
      );
      assert.equal(
        await page.locator('[data-view="sports_app:players"]').isVisible(),
        false
      );
      await sports.click();
      await page
        .locator(".fixture")
        .screenshot({ path: `/tmp/sports-console-navigation-${width}.png` });
      await boost.click();
      await page.evaluate(() => draw(true));
      await page.waitForFunction(() =>
        document
          .querySelector("#menu")
          .firstElementChild.classList.contains("sports-nav-extension")
      );
      assert.equal(
        await page
          .locator("[data-sports-boost-toggle]")
          .getAttribute("aria-expanded"),
        "false"
      );
      await page.locator("[data-sports-boost-toggle]").click();
      await page.evaluate(() => {
        const group = document.createElement("div");
        group.className = "ing-console-nav-group";
        group.innerHTML =
          '<button data-nav-group="Other">Other app</button><button data-view="other_app:overview">Other view</button>';
        document.querySelector("#menu").append(group);
      });
      await page.waitForTimeout(40);
      assert.equal(
        await page
          .locator('[data-view="other_app:overview"]')
          .evaluate((el) => el.closest(".sports-nav-boost") === null),
        true
      );
      assert.equal(
        await page.locator('[data-view="sports_app:players"]').count(),
        1
      );
      assert.equal(await page.locator(".sports-nav-boost").count(), 1);
      assert.equal(await page.locator(".sports-nav-count").count(), 1);
      assert.equal(await page.locator(".sports-nav-count").textContent(), "32");
      await page.evaluate(() => {
        window.badgeCount = 0;
        window.dispatchEvent(new Event("focus"));
      });
      await page.waitForFunction(
        () => document.querySelector(".sports-nav-count")?.textContent === "0"
      );
      await page.evaluate(() => {
        window.failCounts = true;
        window.dispatchEvent(new Event("focus"));
      });
      await page.waitForFunction(
        () => !document.querySelector(".sports-nav-count")
      );
      await page.evaluate(() => {
        window.failCounts = false;
        window.dispatchEvent(new Event("focus"));
      });
      await page.waitForFunction(
        () => document.querySelector(".sports-nav-count")?.textContent === "0"
      );
      await page.evaluate(() => draw(false));
      await page.waitForFunction(
        () => !document.querySelector(".sports-console-navigation")
      );
      assert.deepEqual(
        await page.locator("[data-nav-group]").allTextContents(),
        ["Dashboard", "Sales"]
      );
      assert.equal(await page.locator(".sports-nav-boost").count(), 0);
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log(
      "PASS Sports sidebar desktop/phone: Sports-first ordering, distinct group colours, indentation, preserved collapse handlers, dynamic rerender, no duplicates and native-only navigation unchanged. Badges include scoped totals, event updates, zero counts, rerender persistence, error clearing/recovery and no observer fetch loop. Synthetic sidebar; no ERP writes."
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
