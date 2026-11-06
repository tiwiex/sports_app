/* Browser-page fixture globals created in page.evaluate. */
/* global allowed: writable, calls: writable, enrollments: writable, messages: writable, player: writable, view: writable */
const assert = require("node:assert/strict"),
  fs = require("node:fs"),
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
        '<style>*{box-sizing:border-box}body{margin:12px;font-family:sans-serif}.table{width:100%;border-collapse:collapse}.table td,.table th{padding:10px;border:1px solid #ddd}.table-responsive{overflow:auto;max-width:100%}.modal-fixture{position:fixed;inset:12px;background:white;border:1px solid #aaa;padding:16px;z-index:10000;overflow:auto}.modal-fixture label{display:block}.modal-fixture input{max-width:100%}button{cursor:pointer}</style><main class="ing-console-page"><aside class="ing-console-sidebar">Sports</aside><section class="ing-console-main"><div id="host"></div></section></main>'
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
      await page.evaluate((fields) => {
        window.__ = (s, a = []) => s.replace(/\{(\d+)\}/g, (_, i) => a[i]);
        window.calls = [];
        window.messages = [];
        window.player = {
          name: "PLAYER-QA-1",
          full_name: "Sample Player",
          company: "Academy",
          registered_on: "2026-11-03 11:22:28.343411",
          customer: "CUSTOMER-QA",
          portal_user: "long.player.account@example.invalid",
          first_name: "Sample",
          last_name: "Player",
          contact_email: "sample@example.invalid",
          guardian_name: "Sample Guardian",
          home_address: "First address line\nSecond address line",
          medical_notes:
            "Synthetic long note to verify wrapping and multi-line details.",
          media_consent: 0,
          terms_accepted: 1,
        };
        window.allowed = true;
        window.enrollments = Array.from({ length: 20 }, (_, i) => ({
          name: "ENR-" + i,
          program: "PROGRAM",
          program_name: "Foundation training",
          group: "GROUP",
          group_name: "Junior squad",
          start_date: "2026-01-01",
          end_date: "",
          status: "Active",
          eligible_today: true,
        }));
        window.frappe = {
          boost_console_views: {},
          provide() {},
          router: { slug: (s) => s.toLowerCase().replaceAll(" ", "-") },
          datetime: { get_today: () => "2026-11-03", str_to_user: (s) => s },
          model: { can_read: () => true },
          msgprint: (s) => messages.push(s),
          call: async ({ method, args = {} }) => {
            const action = method.split(".").at(-1);
            calls.push({ action, args });
            if (action === "list_players")
              return {
                message: [
                  { ...player, can_enroll: allowed },
                  {
                    name: "PLAYER-READ",
                    full_name: "Read Only Player",
                    company: "Academy",
                    can_enroll: false,
                  },
                ],
              };
            if (action === "get_player")
              return {
                message: {
                  player: { ...player, name: args.name },
                  enrollments: args.start >= 20 ? [] : enrollments.slice(0, 20),
                  fields,
                  can_enroll: allowed && args.name !== "PLAYER-READ",
                },
              };
            if (action === "save_enrollment") {
              enrollments.unshift({
                ...args.enrollment,
                name: "ENR-NEW",
                program_name: "New friendly program",
                eligible_today: true,
              });
              return { message: "ENR-NEW" };
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
                const h = document.createElement("h2");
                h.textContent = options.title;
                this.el.append(h);
                for (const df of options.fields) {
                  const wrap = document.createElement("div"),
                    field = { df, $wrapper: $(wrap) };
                  if (df.fieldtype !== "HTML") {
                    const label = document.createElement("label");
                    label.textContent = df.label;
                    const input = document.createElement("input");
                    input.name = df.fieldname;
                    input.value = df.default || "";
                    label.append(input);
                    wrap.append(label);
                    field.input = input;
                  }
                  this.fields_dict[df.fieldname] = field;
                  this.el.append(wrap);
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
              async set_value(k, v) {
                this.fields_dict[k].input.value = v;
              }
              async set_values(values) {
                for (const [k, v] of Object.entries(values))
                  if (this.fields_dict[k]?.input)
                    this.fields_dict[k].input.value = v ?? "";
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
      }, JSON.parse(fs.readFileSync(path.join(apps, "sports_app/sports_app/registration_fields.json"), "utf8")));
      await page.addScriptTag({
        path: path.join(apps, "sports_app/sports_app/public/js/players.js"),
      });
      await page.evaluate(async () => {
        window.view = frappe.boost_console_views["sports_app:players"]();
        await view.mount({
          container: document.getElementById("host"),
          signal: new AbortController().signal,
        });
      });
      await page
        .getByRole("button", { name: "Sort by Name", exact: true })
        .click();
      assert.equal(
        await page.evaluate(
          () =>
            calls.filter((c) => c.action === "list_players").at(-1).args.sort_by
        ),
        "full_name"
      );
      await page
        .getByRole("button", {
          name: "Actions for player PLAYER-READ",
          exact: true,
        })
        .click();
      assert.deepEqual(
        await page
          .locator(".sports-player-menu.is-open [role=menuitem]")
          .allTextContents(),
        ["View"]
      );
      await page.keyboard.press("Escape");
      await page
        .getByLabel("Search by registration ID or name", { exact: true })
        .fill("Sample");
      await page.getByRole("button", { name: "Search", exact: true }).click();
      await page
        .getByRole("button", {
          name: "Actions for player PLAYER-QA-1",
          exact: true,
        })
        .focus();
      await page.keyboard.press("ArrowDown");
      assert.deepEqual(
        await page
          .locator(".sports-player-menu.is-open [role=menuitem]")
          .allTextContents(),
        ["View", "New program enrollment"]
      );
      await page.keyboard.press("Enter");
      await page.getByRole("dialog").waitFor();
      assert.equal(await page.locator("#host .ing-console-table").count(), 1);
      assert.equal(
        await page
          .getByLabel("Search by registration ID or name", { exact: true })
          .inputValue(),
        "Sample"
      );
      for (const heading of [
        "Player summary",
        "Linked accounts",
        "Program enrollments",
        "Player details",
        "Parent / guardian",
        "Emergency contact (if different)",
        "Consent choices",
      ])
        assert.equal(
          await page
            .getByRole("heading", { name: heading, exact: true })
            .count(),
          1,
          heading
        );
      assert.equal(
        await page
          .locator(".sports-player-profile .player-grid")
          .first()
          .evaluate(
            (el) => getComputedStyle(el).gridTemplateColumns.split(" ").length
          ),
        width > 640 ? 2 : 1
      );
      assert.equal(
        await page
          .locator(".sports-player-profile")
          .evaluate((el) => el.scrollWidth <= el.clientWidth),
        true
      );
      assert.equal(
        await page
          .locator(".sports-player-profile .player-field")
          .filter({ hasText: "Photo and video permission recorded" })
          .locator("dd")
          .innerText(),
        "No"
      );
      await page
        .getByRole("dialog")
        .screenshot({ path: `/tmp/sports-player-profile-${width}.png` });
      await page
        .getByRole("button", { name: "More enrollments", exact: true })
        .click();
      await page
        .getByText("No program enrollments on this page.", { exact: true })
        .waitFor();
      assert.equal(
        await page.evaluate(
          () => calls.filter((c) => c.action === "get_player").at(-1).args.start
        ),
        20
      );
      await page
        .getByRole("button", { name: "Previous enrollments", exact: true })
        .click();
      await page
        .getByRole("button", { name: "New program enrollment", exact: true })
        .waitFor();
      await page
        .getByRole("button", { name: "New program enrollment", exact: true })
        .click();
      await page.getByLabel("Program", { exact: true }).fill("PROGRAM");
      await page.getByLabel("Status", { exact: true }).fill("Active");
      await page.getByRole("button", { name: "Save", exact: true }).click();
      await page.getByRole("link", { name: "ENR-NEW", exact: true }).waitFor();
      assert.equal(
        await page.evaluate(
          () =>
            calls.filter((c) => c.action === "save_enrollment").at(-1).args
              .player
        ),
        "PLAYER-QA-1"
      );
      assert.equal(
        await page.getByLabel("Payer Customer", { exact: true }).count(),
        0
      );
      await page.getByRole("button", { name: "Close", exact: true }).click();
      await page
        .getByRole("button", {
          name: "Actions for player PLAYER-QA-1",
          exact: true,
        })
        .click();
      await page.evaluate(() => {
        allowed = false;
      });
      await page
        .getByRole("menuitem", { name: "New program enrollment", exact: true })
        .click();
      await page.waitForFunction(() => messages.length === 1);
      assert.equal(await page.getByRole("dialog").count(), 0);
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth
        ),
        true
      );
      await page.evaluate(() => view.unmount());
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log(
      "PASS Players desktop/phone: invoice list/sort, keyboard/reference menu, grouped responsive modal, list/search retention, enrollment pagination/create refresh, consent display, fresh permission check, no payer selector, cleanup (Dialog/API fixture)"
    );
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
