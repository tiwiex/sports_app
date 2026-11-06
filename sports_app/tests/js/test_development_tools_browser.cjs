/* Browser-page fixture globals created in page.evaluate. */
/* global abort: writable, alerts: writable, baseline: writable, calls: writable, docPath: writable, fail: writable, readerSelectBefore: writable, saveDelay: writable, selectBefore: writable, story: writable, view: writable */
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
        '<style>*{box-sizing:border-box}body{margin:12px;font-family:sans-serif}.table{width:100%;border-collapse:collapse}.table td,.table th{padding:8px;border:1px solid #ddd}.table-responsive{max-width:100%;overflow:auto}.modal-fixture{position:fixed;inset:12px;overflow:auto;background:white;padding:16px;border:1px solid #ccc;z-index:1000}label{display:block}button{cursor:pointer}</style><div id="host"></div>'
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
        window.__ = (s) => s;
        window.calls = [];
        window.fail = false;
        window.alerts = [];
        window.saveDelay = 0;
        window.story = {
          state: "In progress — prototype",
          priority: "Must",
          origin: "Both",
          revision: "v1",
          state_options: [
            "Proposed",
            "In progress",
            "In review",
            "Done",
            "Blocked",
            "Withdrawn",
          ],
          priority_options: ["Must", "Should", "Could", "Won't"],
        };
        window.docPath = "backlog/user-stories/us-003-01-example.md";
        const documents = () => [
          {
            path: docPath,
            title: "US-003-01: Sample intake",
            category: "User Stories",
            story: { ...story },
          },
          {
            path: "discovery/README.md",
            title: "Discovery source register",
            category: "Guides and Product",
            story: null,
          },
        ];
        window.frappe = {
          boost_console_views: {},
          provide() {},
          show_alert: (value) => alerts.push(value),
          call: async ({ method, args }) => {
            const action = method.split(".").at(-1);
            calls.push({ action, args });
            if (action === "get_documents")
              return { message: { documents: documents() } };
            if (action === "get_document")
              return {
                message: {
                  html: '<h1>Sample story</h1><p>Acceptance evidence remains here.</p><a href="../../../discovery/README.md">Discovery</a>',
                  story: args.path === docPath ? { ...story } : null,
                },
              };
            if (action === "update_story") {
              if (saveDelay)
                await new Promise((resolve) => setTimeout(resolve, saveDelay));
              if (fail) throw Error("stale revision");
              const assertRevision = args.revision === story.revision;
              if (!assertRevision) throw Error("stale");
              if (args.state) story.state = args.state;
              if (args.priority) story.priority = args.priority;
              story.revision += "x";
              return { message: { ...story, audit_path: "build-logs/qa.md" } };
            }
            throw Error(action);
          },
          ui: {
            Dialog: class {
              constructor(options) {
                this.el = document.createElement("section");
                this.el.className = "modal-fixture";
                this.el.role = "dialog";
                this.el.innerHTML = '<h2 class="modal-title"></h2>';
                this.$wrapper = $(this.el);
                const wrap = document.createElement("div");
                this.el.append(wrap);
                this.fields_dict = { document: { $wrapper: $(wrap) } };
              }
              show() {
                document.body.append(this.el);
              }
              hide() {
                this.$wrapper.trigger("hide.bs.modal");
                this.$wrapper.trigger("hidden.bs.modal");
                this.el.remove();
              }
            },
          },
        };
      });
      await page.addScriptTag({
        path: path.join(
          apps,
          "sports_app/sports_app/public/js/development_tools.js"
        ),
      });
      await page.evaluate(async () => {
        window.abort = new AbortController();
        window.view = frappe.boost_console_views["sports_app:development"]();
        await view.mount({
          container: document.querySelector("#host"),
          signal: abort.signal,
        });
      });
      const host = page.locator("#host");
      assert.deepEqual(await host.locator("thead th").allTextContents(), [
        "Story",
        "Epic",
        "Title",
        "Origin",
        "Status",
        "MoSCoW",
        "Action",
      ]);
      const row = host.locator("tbody tr").first();
      assert.equal(
        await row
          .locator("td")
          .first()
          .evaluate((el) => getComputedStyle(el).backgroundColor),
        "rgb(254, 243, 199)"
      );
      assert.equal(
        await host.getByRole("button", { name: "Save", exact: true }).count(),
        0
      );
      assert.equal(await row.locator(".sports-moscow-badge").count(), 0);
      assert.equal(await row.locator(".sports-status-badge").count(), 0);
      const openRect = await row
        .getByRole("button", { name: "Open", exact: true })
        .boundingBox();
      const doneRect = await row
        .getByRole("button", { name: "Mark Done", exact: true })
        .boundingBox();
      assert.ok(Math.abs(openRect.y - doneRect.y) < 2);
      assert.ok(doneRect.x >= openRect.x + openRect.width);
      const viewport = host.locator(".sports-doc-table-wrap");
      await row.evaluate((el) => {
        for (let i = 0; i < 50; i++) {
          const clone = el.cloneNode(true);
          clone.dataset.heightFixture = "1";
          el.parentElement.append(clone);
        }
      });
      assert.equal(
        await viewport.evaluate((el) =>
          Math.round(parseFloat(getComputedStyle(el).maxHeight))
        ),
        1045
      );
      assert.ok(
        await viewport.evaluate((el) => el.clientHeight > window.innerHeight)
      );
      await viewport.evaluate((el) => (el.scrollTop = 180));
      assert.ok(
        await viewport.evaluate(
          (el) =>
            Math.abs(
              el.querySelector("th").getBoundingClientRect().top -
                el.getBoundingClientRect().top
            ) < 3
        )
      );
      await viewport.evaluate((el) => {
        el.scrollTop = 0;
        el.querySelectorAll("[data-height-fixture]").forEach((row) =>
          row.remove()
        );
      });
      const colours = [];
      for (const value of ["Must", "Should", "Could", "Won't"]) {
        await host.getByLabel("MoSCoW", { exact: true }).selectOption(value);
        await page.waitForFunction((value) => story.priority === value, value);
        await host
          .getByLabel("MoSCoW", { exact: true })
          .waitFor({ state: "visible" });
        await page.waitForFunction(
          () =>
            !document.querySelector("#host select[aria-label=MoSCoW]").disabled
        );
        colours.push(
          await host
            .getByLabel("MoSCoW", { exact: true })
            .evaluate((el) => getComputedStyle(el).backgroundColor)
        );
      }
      assert.equal(new Set(colours).size, 4);
      await host
        .locator(".sports-doc-table-wrap")
        .screenshot({ path: `/tmp/sports-story-table-${width}.png` });
      await host.getByLabel("MoSCoW", { exact: true }).selectOption("Should");
      await page.waitForFunction(() => story.priority === "Should");
      await page.waitForFunction(
        () =>
          !document.querySelector("#host select[aria-label=MoSCoW]").disabled
      );
      await host
        .getByLabel("Status", { exact: true })
        .selectOption("In review");
      await page.waitForFunction(() => story.state === "In review");
      await page.waitForFunction(
        () =>
          !document.querySelector("#host select[aria-label=Status]").disabled
      );
      await page.evaluate(() => {
        saveDelay = 120;
        window.selectBefore = document.querySelector(
          "#host select[aria-label=MoSCoW]"
        );
        window.baseline = calls.filter(
          (c) => c.action === "update_story"
        ).length;
      });
      await host.getByLabel("MoSCoW", { exact: true }).selectOption("Could");
      assert.equal(
        await host.getByLabel("MoSCoW", { exact: true }).isEnabled(),
        true
      );
      await host.getByLabel("MoSCoW", { exact: true }).selectOption("Should");
      await host.getByLabel("Status", { exact: true }).click();
      await page.waitForFunction(
        () =>
          story.priority === "Should" &&
          calls.filter((c) => c.action === "update_story").length ===
            baseline + 2
      );
      await page.waitForTimeout(180);
      assert.equal(
        await host
          .getByLabel("Status", { exact: true })
          .evaluate((el) => el === document.activeElement),
        true
      );
      await page.keyboard.press("Escape");
      assert.equal(
        await page.evaluate(
          () =>
            selectBefore ===
            document.querySelector("#host select[aria-label=MoSCoW]")
        ),
        true
      );
      assert.equal(
        await host.getByLabel("MoSCoW", { exact: true }).isEnabled(),
        true
      );
      await page.evaluate(() => (saveDelay = 0));
      await host
        .getByRole("button", { name: "Open", exact: true })
        .last()
        .click();
      const dialog = page.getByRole("dialog");
      await dialog.getByLabel("Status", { exact: true }).waitFor();
      assert.equal(
        await dialog.getByLabel("Status", { exact: true }).inputValue(),
        "In review"
      );
      assert.equal(
        await dialog.getByRole("button", { name: "Save", exact: true }).count(),
        0
      );
      assert.equal(
        await dialog
          .locator(".sports-story-label")
          .filter({ hasText: "MoSCoW" })
          .evaluate((el) => getComputedStyle(el).position),
        "absolute"
      );
      assert.equal(
        await dialog
          .locator(".sports-story-label")
          .filter({ hasText: "Status" })
          .evaluate((el) => getComputedStyle(el).position),
        "absolute"
      );
      await page.evaluate(
        () =>
          (window.readerSelectBefore = document.querySelector(
            ".sports-doc-reader select[aria-label=MoSCoW]"
          ))
      );
      await dialog.getByLabel("MoSCoW", { exact: true }).selectOption("Could");
      await page.waitForFunction(() => story.priority === "Could");
      await page.waitForFunction(
        () =>
          !document.querySelector(
            ".sports-doc-reader select[aria-label=MoSCoW]"
          ).disabled
      );
      assert.equal(
        await page.evaluate(
          () =>
            readerSelectBefore ===
            document.querySelector(
              ".sports-doc-reader select[aria-label=MoSCoW]"
            )
        ),
        true
      );
      await dialog
        .getByLabel("Review note (optional)", { exact: true })
        .fill("Reviewed acceptance evidence.");
      await page.evaluate(() => (fail = true));
      await dialog
        .getByRole("button", { name: "Mark Done", exact: true })
        .click();
      await dialog
        .getByRole("status")
        .filter({ hasText: "Update failed" })
        .waitFor();
      assert.equal(await page.evaluate(() => story.state), "In review");
      await dialog
        .getByLabel("Status", { exact: true })
        .selectOption("Blocked");
      await dialog
        .getByRole("status")
        .filter({ hasText: "Update failed" })
        .waitFor();
      assert.equal(
        await dialog.getByLabel("Status", { exact: true }).inputValue(),
        "In review"
      );
      await page.evaluate(() => (fail = false));
      await dialog
        .getByRole("button", { name: "Mark Done", exact: true })
        .click();
      await dialog
        .getByRole("button", { name: "Already Done", exact: true })
        .waitFor();
      assert.equal(
        await host.getByLabel("Status", { exact: true }).inputValue(),
        "Done"
      );
      assert.equal(
        await host
          .locator("tbody tr")
          .first()
          .locator("td")
          .first()
          .evaluate((el) => getComputedStyle(el).backgroundColor),
        "rgb(134, 239, 172)"
      );
      assert.ok(
        await dialog
          .locator(".sports-reader-header")
          .evaluate((el) => parseInt(getComputedStyle(el).paddingTop) >= 16)
      );
      assert.ok(
        await dialog
          .locator(".sports-story-controls.is-reader")
          .evaluate((el) => parseInt(getComputedStyle(el).rowGap) >= 18)
      );
      assert.equal(
        await dialog
          .getByRole("button", { name: "Already Done", exact: true })
          .isDisabled(),
        true
      );
      assert.equal(
        await dialog
          .getByText("Acceptance evidence remains here.", { exact: true })
          .count(),
        1
      );
      await dialog.screenshot({
        path: `/tmp/sports-story-tracking-${width}.png`,
      });
      await page.evaluate(() => view.unmount());
      assert.equal(await page.getByRole("dialog").count(), 0);
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth
        ),
        true
      );
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log(
      "PASS Sports Development Tools desktop/phone: MoSCoW persistence, legacy status, modal review/Mark Done, stale-save feedback, list/modal synchronization, completion disabled, cleanup. Synthetic APIs; no backlog writes."
    );
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
