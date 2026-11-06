// Real Boost watcher and Sports enrollment view; APIs are isolated synthetic fixtures.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
const apps = path.resolve(__dirname, "../../../..");
const boost = fs.readFileSync(
  path.join(
    apps,
    "erp_boost/erp_boost/erp_boost/page/boost_console/boost_console.js"
  ),
  "utf8"
);
(async () => {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  try {
    for (const width of [1440, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      page.setDefaultTimeout(10000);
      const errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await page.setContent(
        '<style>.dropdown-menu{display:none}.is-open .dropdown-menu{display:block}td,th{padding:8px}#host{max-height:350px;overflow:auto}.ing-console-table-wrap{max-width:100%;overflow:auto}</style><main id="host"></main><button id="outside">Outside</button>'
      );
      await page.evaluate(() => {
        const qa = (window.qa = {
          calls: [],
          events: {},
          subs: new Set(),
          rows: [
            {
              name: "R1",
              full_name: "One",
              status: "Pending",
              requested_pathway: "Foundations",
              submitted_on: "2026-11-06",
              can_review: false,
            },
          ],
          hidden: false,
        });
        Object.defineProperty(document, "hidden", {
          get: () => qa.hidden,
          configurable: true,
        });
        window.__ = (text, args = []) =>
          text.replace(/\{(\d+)\}/g, (_, index) => args[index]);
        const realtime = {
          on: (event, cb) => (qa.events[event] ||= new Set()).add(cb),
          off: (event, cb) => qa.events[event]?.delete(cb),
          doctype_subscribe: (dt) => qa.subs.add(dt),
          doctype_unsubscribe: (dt) => qa.subs.delete(dt),
        };
        realtime.socket = { on: realtime.on, off: realtime.off };
        qa.emit = (event, payload) =>
          qa.events[event]?.forEach((cb) => cb(payload));
        window.frappe = {
          pages: { "boost-console": {} },
          realtime,
          boost_console_views: {},
          provide() {},
          router: { slug: (s) => s },
          datetime: { str_to_user: (s) => s },
          call: async (options) => {
            qa.calls.push(options);
            if (qa.hold)
              await new Promise((resolve) => {
                qa.release = resolve;
              });
            return {
              message: qa.rows
                .filter((r) => r.status === options.args.status)
                .sort(
                  (a, b) =>
                    String(a[options.args.sort_by]).localeCompare(
                      String(b[options.args.sort_by])
                    ) * (options.args.sort_order === "desc" ? -1 : 1)
                )
                .slice(options.args.start, options.args.start + 20),
            };
          },
        };
      });
      await page.addScriptTag({
        content:
          boost +
          "\nwindow.BoostTableWatcher = BoostTableWatcher; window.BoostConsoleClass = BoostConsole;",
      });
      await page.addScriptTag({
        path: path.resolve(__dirname, "../../public/js/registrations.js"),
      });
      await page.evaluate(async () => {
        window.qa.abort = new AbortController();
        window.qa.view =
          window.frappe.boost_console_views["sports_app:registrations"]();
        await window.qa.view.mount({
          container: document.getElementById("host"),
          signal: window.qa.abort.signal,
          watch: (opts) => {
            window.qa.watcher = new window.BoostTableWatcher({
              ...opts,
              container: document.getElementById("host"),
              signal: window.qa.abort.signal,
              interval: 5000,
            });
            return window.qa.watcher;
          },
        });
      });
      await page.evaluate(() => {
        window.qa.rows.push({ ...window.qa.rows[0], name: "R2" });
        window.qa.emit("list_update", { doctype: "Sports Registration" });
      });
      await page.waitForFunction(
        () => document.querySelectorAll("tbody tr").length === 2
      );
      // Equal data must not replace the table or dismiss focus.
      await page.evaluate(() => {
        window.qa.original = document.querySelector("table");
        window.qa.watcher.request(0);
      });
      await page.waitForTimeout(150);
      assert.ok(
        await page.evaluate(
          () => window.qa.original === document.querySelector("table")
        )
      );
      const beforeMenu = await page.evaluate(() => window.qa.calls.length);
      await page
        .getByRole("button", { name: "Actions for enrollment R1", exact: true })
        .click();
      await page.evaluate(() => {
        window.qa.rows.push({ ...window.qa.rows[0], name: "R3" });
        window.qa.emit("doc_update", {
          doctype: "Sports Registration",
          name: "R3",
        });
      });
      await page.waitForTimeout(750);
      assert.equal(
        await page.evaluate(() => window.qa.calls.length),
        beforeMenu
      );
      assert.equal(await page.locator(".is-open").count(), 1);
      await page
        .getByRole("button", { name: "Actions for enrollment R1", exact: true })
        .click();
      await page.waitForFunction(
        () => document.querySelectorAll("tbody tr").length === 3
      );
      // Focused filters are preserved until the user is finished.
      await page.evaluate(() =>
        window.qa.rows.push({
          name: "A1",
          full_name: "Accepted",
          status: "Accepted",
        })
      );
      await page
        .getByLabel("Enrollment status", { exact: true })
        .selectOption("Accepted");
      await page.getByLabel("Enrollment status", { exact: true }).focus();
      await page.evaluate(() => {
        window.qa.rows.push({
          name: "A2",
          full_name: "Accepted two",
          status: "Accepted",
        });
        window.qa.emit("list_update", { doctype: "Sports Registration" });
      });
      await page.waitForTimeout(750);
      assert.equal(await page.locator("tbody tr").count(), 1);
      await page.locator("#outside").focus();
      await page.waitForFunction(
        () => document.querySelectorAll("tbody tr").length === 2
      );
      assert.equal(
        await page
          .getByLabel("Enrollment status", { exact: true })
          .inputValue(),
        "Accepted"
      );
      // A modal, hidden tab and disconnected socket never lose queued invalidations.
      await page.evaluate(() => {
        const d = document.createElement("dialog");
        d.id = "qa-dialog";
        document.body.append(d);
        d.showModal();
        window.qa.rows.push({
          name: "A3",
          full_name: "Three",
          status: "Accepted",
        });
        window.qa.watcher.request(0);
      });
      await page.waitForTimeout(200);
      assert.equal(await page.locator("tbody tr").count(), 2);
      await page.evaluate(() => {
        document.getElementById("qa-dialog").close();
        document.getElementById("qa-dialog").remove();
      });
      await page.locator("#outside").focus();
      await page.waitForFunction(
        () => document.querySelectorAll("tbody tr").length === 3
      );
      await page.evaluate(() => {
        window.qa.hidden = true;
        window.qa.rows.push({
          name: "A4",
          full_name: "Four",
          status: "Accepted",
        });
        window.qa.watcher.request(0);
      });
      await page.waitForTimeout(200);
      assert.equal(await page.locator("tbody tr").count(), 3);
      await page.evaluate(() => {
        window.qa.hidden = false;
        document.dispatchEvent(new Event("visibilitychange"));
      });
      await page.waitForFunction(
        () => document.querySelectorAll("tbody tr").length === 4
      );
      // Timer fallback catches updates that did not emit any realtime notification.
      await page.evaluate(() =>
        window.qa.rows.push({
          name: "A5",
          full_name: "Five",
          status: "Accepted",
        })
      );
      await page.waitForFunction(
        () => document.querySelectorAll("tbody tr").length === 5,
        null,
        { timeout: 7000 }
      );
      await page.evaluate(() => {
        window.qa.rows = window.qa.rows.filter((r) => r.name !== "A5");
        window.qa.emit("list_update", { doctype: "Sports Registration" });
      });
      await page.waitForFunction(
        () => document.querySelectorAll("tbody tr").length === 4
      );
      await page.evaluate(() => {
        window.qa.rows.push({
          name: "A5",
          full_name: "Five",
          status: "Accepted",
        });
        window.qa.emit("connect");
      });
      await page.waitForFunction(
        () => document.querySelectorAll("tbody tr").length === 5
      );
      // Abort an in-flight read; late data may not touch the old mounted container.
      await page.evaluate(() => {
        window.qa.hold = true;
        window.qa.watcher.request(0);
      });
      await page.waitForFunction(() => Boolean(window.qa.release));
      await page.evaluate(() => {
        window.qa.abort.abort();
        window.qa.view.unmount();
        window.qa.rows.push({
          name: "A6",
          full_name: "Six",
          status: "Accepted",
        });
        window.qa.release();
      });
      await page.waitForTimeout(100);
      assert.equal(await page.locator("tbody tr").count(), 5);
      assert.ok(
        await page.evaluate(
          () =>
            window.qa.subs.size === 0 &&
            [...Object.values(window.qa.events)].every((set) => set.size === 0)
        )
      );
      // Exercise the real host's finance read path without any installed Sports dependency.
      const finance = await page.evaluate(async () => {
        const view = {
          key: "sales",
          type: "doctype",
          doctype: "Sales Invoice",
        };
        const instance = Object.create(window.BoostConsoleClass.prototype);
        Object.assign(instance, {
          currentView: "sales",
          company: "QA Company",
          currentSearch: "paid",
          viewFilters: { sales: { status: "Paid" } },
          viewPayloadCache: {
            sales: {
              type: "documents",
              payload: { rows: [{ name: "INV1" }] },
              view,
            },
          },
          viewDataCache: {},
          get_current_view: () => view,
          get_document_filters: () => ({
            company: "QA Company",
            status: "Paid",
          }),
          render_documents: (payload) => {
            instance.rendered = payload;
          },
        });
        window.frappe.call = async (options) => {
          instance.request = options;
          return { message: { rows: [{ name: "INV2" }, { name: "INV1" }] } };
        };
        await instance.refresh_live_table(view, { canApply: () => true });
        const applied =
          instance.rendered.rows.length === 2 &&
          instance.request.args.search === "paid" &&
          JSON.parse(instance.request.args.filters).company === "QA Company";
        instance.rendered = null;
        window.frappe.call = async () => {
          instance.currentView = "other";
          return { message: { rows: [{ name: "LATE" }] } };
        };
        await instance.refresh_live_table(view, { canApply: () => true });
        const staleRejected = instance.rendered === null;
        const reportView = {
          key: "ledger",
          type: "report",
          report: "General Ledger",
        };
        const report = Object.create(window.BoostConsoleClass.prototype);
        const oldReport = {
          rows: [{ name: "ENTRY1" }],
          columns: [],
          row_count: 1,
          report_session_key: "old",
        };
        Object.assign(report, {
          currentView: "ledger",
          company: "QA Company",
          viewFilters: {},
          viewPayloadCache: { ledger: { type: "report", payload: oldReport } },
          viewDataCache: {},
          get_current_view: () => reportView,
          get_backend_report_filters: () => ({ company: "QA Company" }),
          report_fetch_limit: () => 200,
          render_report: () => {
            report.rendered = true;
          },
        });
        window.frappe.call = async (options) => {
          report.request = options;
          return { message: { ...oldReport, report_session_key: "new" } };
        };
        await report.refresh_live_table(reportView, { canApply: () => true });
        const metadataOnly =
          !report.rendered &&
          report.viewPayloadCache.ledger.payload.report_session_key === "new";
        window.frappe.call = async (options) => {
          report.request = options;
          return {
            message: {
              ...oldReport,
              rows: [{ name: "ENTRY2" }, { name: "ENTRY1" }],
              row_count: 2,
            },
          };
        };
        await report.refresh_live_table(reportView, { canApply: () => true });
        return (
          applied &&
          staleRejected &&
          metadataOnly &&
          report.rendered &&
          report.request.method === "erp_boost.api.get_boost_console_report" &&
          JSON.parse(report.request.args.filters).company === "QA Company"
        );
      });
      assert.ok(finance);
      assert.deepEqual(errors, []);
      await page.close();
    }
    console.log(
      "PASS desktop/phone: real Boost watcher + Sports enrollment inserts, unchanged DOM, menu/filter/modal deferral, hidden resume, polling fallback, abort/late reply cleanup; finance protected reread and stale-navigation rejection."
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
