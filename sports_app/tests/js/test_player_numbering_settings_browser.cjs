/* Actual Sports settings view with synthetic FieldGroup/API; no ERP writes. */
const assert = require("node:assert/strict");
const path = require("node:path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
(async () => {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  try {
    for (const width of [1440, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 950 } });
      const errors = [];
      page.on("pageerror", (error) => errors.push(error.message));
      await page.setContent(
        '<style>*{box-sizing:border-box}body{font-family:sans-serif;margin:12px}label,input,select{display:block;width:100%}.field{margin:12px 0}small{display:block;overflow-wrap:anywhere}.table-responsive{overflow:auto}table{max-width:100%}</style><main id="host"></main>'
      );
      await page.evaluate(() => {
        window.__ = (s, args = []) =>
          s.replace(/\{(\d+)\}/g, (_, i) => args[i]);
        window.saved = null;
        const configuration = {
          settings: {
            academy_name: "Academy",
            company: "Academy",
            currency: "NGN",
            timezone: "Africa/Lagos",
            registration_prefix: "MSA",
            registration_digits: 3,
            player_starting_sequence: "1",
            default_program: "P",
            modified: "v1",
            enrollment_items: [
              {
                item_code: "EXISTING",
                item_name: "Academy kit",
                qty: 2,
                rate: 15000,
                amount: 30000,
              },
            ],
          },
          companies: [{ name: "Academy" }],
          timezones: ["Africa/Lagos"],
          programs: [],
          groups: [],
        };
        window.frappe = {
          boost_console_views: {},
          provide() {},
          show_alert() {},
          call: async ({ method, args }) => {
            if (method.endsWith("get_configuration"))
              return { message: configuration };
            if (method.endsWith("save_program")) {
              configuration.programs.push({
                ...args.program,
                name: "NEW-PROGRAM",
              });
              return { message: "NEW-PROGRAM" };
            }
            window.saved = args.settings;
            return { message: { ...args.settings, modified: "v2" } };
          },
          ui: {
            Dialog: class {
              constructor(options) {
                this.options = options;
                this.el = document.createElement("div");
                this.el.role = "dialog";
                this.inputs = {};
                for (const df of options.fields) {
                  const label = document.createElement("label"),
                    input = document.createElement("input");
                  label.textContent = df.label;
                  label.append(input);
                  this.el.append(label);
                  this.inputs[df.fieldname] = input;
                }
                this.primary = document.createElement("button");
                this.primary.textContent = "Save";
                this.primary.onclick = () =>
                  options.primary_action(
                    Object.fromEntries(
                      Object.entries(this.inputs).map(([key, input]) => [
                        key,
                        input.value,
                      ])
                    )
                  );
                this.el.append(this.primary);
              }
              set_values(values) {
                for (const [key, value] of Object.entries(values))
                  if (this.inputs[key]) this.inputs[key].value = value ?? "";
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
            FieldGroup: class {
              constructor({ body, fields }) {
                this.body = body;
                this.fields = fields;
                this.fields_dict = {};
                window.settingsForm = this;
              }
              make() {
                const wrapper = document.createElement("div"),
                  page = document.createElement("div");
                wrapper.className = "form-layout";
                page.className = "form-page";
                wrapper.append(page);
                this.body.append(wrapper);
                this.wrapper = [wrapper];
                this.page = [page];
                for (const df of this.fields) {
                  const div = document.createElement("div");
                  div.className = "field";
                  const label = document.createElement("label");
                  label.textContent = df.label;
                  label.htmlFor = df.fieldname;
                  const input = document.createElement("input");
                  input.id = df.fieldname;
                  input.name = df.fieldname;
                  input.value = df.default ?? "";
                  const small = document.createElement("small");
                  small.textContent = df.description || "";
                  this.fields_dict[df.fieldname] = {
                    df,
                    input,
                    $wrapper: [div],
                    get_value: () =>
                      df.fieldtype === "Table"
                        ? this.fields_dict[df.fieldname].value || []
                        : input.value,
                  };
                  input.addEventListener("change", () => df.onchange?.());
                  div.append(label, input, small);
                  this.page[0].append(div);
                }
              }
              async set_values(values) {
                for (const [key, value] of Object.entries(values))
                  if (this.fields_dict[key]) {
                    this.fields_dict[key].input.value = value ?? "";
                    this.fields_dict[key].value = value;
                  }
              }
              get_value(key) {
                return this.fields_dict[key].get_value();
              }
              set_value(key, value) {
                this.fields_dict[key].input.value = value;
              }
              get_values(ignore_errors) {
                if (
                  !ignore_errors &&
                  Object.values(this.fields_dict).some(
                    (field) => field.df.reqd && !field.input.value
                  )
                )
                  return null;
                return Object.fromEntries(
                  Object.entries(this.fields_dict).map(([key, value]) => [
                    key,
                    value.get_value(),
                  ])
                );
              }
            },
          },
        };
      });
      await page.addScriptTag({
        path: path.resolve(__dirname, "../../public/js/academy_settings.js"),
      });
      await page.evaluate(async () => {
        const view = window.frappe.boost_console_views["sports_app:settings"]();
        await view.mount({
          container: document.querySelector("#host"),
          signal: new AbortController().signal,
        });
      });
      assert.equal(await page.getByRole("tab").count(), 6);
      assert.equal(await page.getByRole("tabpanel").count(), 1);
      await page.getByRole("tab", { name: "Player IDs", exact: true }).click();
      assert.equal(
        await page.locator('[name="player_starting_sequence"]').inputValue(),
        "1"
      );
      await page.locator('[name="player_starting_sequence"]').fill("126");
      await page
        .locator('[name="player_starting_sequence"]')
        .dispatchEvent("change");
      assert.equal(
        await page
          .getByText("Registration example: MSAYY-MM126 (preview only)")
          .count(),
        1
      );
      await page.locator('[name="registration_prefix"]').fill("CLUB");
      await page
        .locator('[name="registration_prefix"]')
        .dispatchEvent("change");
      await page
        .getByRole("tab", { name: "Website payments", exact: true })
        .click();
      await page.evaluate(() => {
        const field = window.settingsForm.fields_dict.enrollment_items;
        field.value.push({
          item_code: "EXTRA",
          qty: 1.5,
          rate: 2000,
          item_name: "Extra charge",
          amount: 3000,
        });
      });
      await page
        .locator('[name="payment_review_emails"]')
        .fill("review@example.invalid");
      await page.getByRole("tab", { name: "General", exact: true }).click();
      await page.locator('[name="academy_name"]').fill("Updated Academy");
      await page
        .getByRole("tab", { name: "Monthly fees", exact: true })
        .click();
      await page.locator('[name="default_monthly_fee"]').fill("40000");
      await page
        .getByRole("tab", { name: "Programs & groups", exact: true })
        .click();
      assert.equal(
        await page
          .getByRole("button", { name: "New Program", exact: true })
          .isVisible(),
        true
      );
      await page
        .getByRole("button", { name: "New Program", exact: true })
        .click();
      await page
        .getByRole("dialog")
        .getByLabel("Program name", { exact: true })
        .fill("New program");
      await page
        .getByRole("dialog")
        .getByLabel("Sport", { exact: true })
        .fill("Football");
      await page.getByRole("button", { name: "Save", exact: true }).click();
      await page.getByText("New program", { exact: true }).waitFor();
      assert.equal(
        await page.getByRole("tab", { selected: true }).textContent(),
        "Programs & groups"
      );
      assert.equal(
        await page.locator('[name="player_starting_sequence"]').inputValue(),
        "126"
      );
      await page
        .getByRole("tab", { name: "Enrollment defaults", exact: true })
        .click();
      assert.equal(
        await page.locator('[name="default_program"]').inputValue(),
        "P"
      );
      await page
        .getByRole("button", { name: "Save Settings", exact: true })
        .click();
      assert.equal(
        await page.evaluate(() => window.saved.player_starting_sequence),
        "126"
      );
      assert.equal(
        await page.evaluate(() => window.saved.registration_prefix),
        "CLUB"
      );
      assert.equal(await page.evaluate(() => window.saved.modified), "v1");
      assert.deepEqual(
        await page.evaluate(() => window.saved.enrollment_items),
        [
          { item_code: "EXISTING", qty: 2, rate: 15000 },
          { item_code: "EXTRA", qty: 1.5, rate: 2000 },
        ]
      );
      assert.equal(
        await page.evaluate(() => window.saved.academy_name),
        "Updated Academy"
      );
      assert.equal(
        await page.evaluate(() => window.saved.payment_review_emails),
        "review@example.invalid"
      );
      assert.equal(
        await page.evaluate(() => window.saved.default_monthly_fee),
        "40000"
      );
      await page
        .getByRole("tab", { name: "Monthly fees", exact: true })
        .click();
      await page.locator('[name="automatic_monthly_billing"]').fill("1");

      await page
        .locator('[name="monthly_billing_user"]')
        .fill("finance@example.invalid");
      await page
        .getByRole("button", { name: "Save Settings", exact: true })
        .click();
      assert.equal(
        await page.evaluate(() => window.saved.automatic_monthly_billing),
        "1"
      );

      assert.equal(
        await page.evaluate(() => window.saved.monthly_billing_user),
        "finance@example.invalid"
      );
      await page.getByRole("tab", { name: "General", exact: true }).focus();
      await page.keyboard.press("End");
      assert.equal(
        await page.getByRole("tab", { selected: true }).textContent(),
        "Programs & groups"
      );
      await page.keyboard.press("Home");
      await page.keyboard.press("ArrowRight");
      assert.equal(
        await page.getByRole("tab", { selected: true }).textContent(),
        "Player IDs"
      );
      assert.equal(
        await page.locator('[name="player_starting_sequence"]').inputValue(),
        "126"
      );
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth > innerWidth
        ),
        false
      );
      await page.getByRole("tab", { name: "General", exact: true }).click();
      await page.locator('[name="academy_name"]').fill("");
      await page
        .getByRole("tab", { name: "Monthly fees", exact: true })
        .click();
      await page
        .getByRole("button", { name: "Save Settings", exact: true })
        .click();
      assert.equal(
        await page.getByRole("tab", { selected: true }).textContent(),
        "General"
      );
      assert.equal(
        await page.evaluate(() => window.saved.academy_name),
        "Updated Academy"
      );
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log(
      "PASS actual Sports numbering settings at desktop/phone: floor field, prefix/digits preview and save payload. Synthetic controls/API; no ERP writes."
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
