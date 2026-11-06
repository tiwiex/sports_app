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
            window.saved = args.settings;
            return { message: { ...args.settings, modified: "v2" } };
          },
          ui: {
            FieldGroup: class {
              constructor({ body, fields }) {
                this.body = body;
                this.fields = fields;
                this.fields_dict = {};
              }
              make() {
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
                  this.fields_dict[df.fieldname] = { df, input };
                  input.addEventListener("change", () => df.onchange?.());
                  div.append(label, input, small);
                  this.body.append(div);
                }
              }
              async set_values(values) {
                for (const [key, value] of Object.entries(values))
                  if (this.fields_dict[key])
                    this.fields_dict[key].input.value = value ?? "";
              }
              get_value(key) {
                return this.fields_dict[key].input.value;
              }
              set_value(key, value) {
                this.fields_dict[key].input.value = value;
              }
              get_values() {
                return Object.fromEntries(
                  Object.entries(this.fields_dict).map(([key, value]) => [
                    key,
                    value.input.value,
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
