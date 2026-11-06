/* Production Next export + real IndexedDB/worker; synthetic API never posts ERP records. */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
const { createServer } = require("node:http");
const { readFile } = require("node:fs/promises");
const path = require("node:path"),
  assert = require("node:assert/strict");
const ROOT = "/assets/sports_app/attendance/",
  out = path.resolve(__dirname, "../../attendance_app/out");
let user = "staff@example.test",
  lost = false,
  deny = false,
  writes = 0,
  posts = 0;
const session = {
  name: "SESSION-QA",
  title: "Saturday training",
  company: "QA Academy",
  session_date: "2026-01-01",
  start_time: "10:00:00",
  end_time: "12:00:00",
  timezone: "Africa/Lagos",
  venue: "Training ground",
  status: "Scheduled",
};
let rows;
let creation = null,
  creationAttempts = [];
let biometricRecords = [];
let failDemo = false;
const reset = () => {
  rows = [
    {
      name: "ATT-1",
      player: "QA-001",
      player_name: "Sample Player One",
      status: "Unmarked",
      modified: "v1",
    },
    {
      name: "ATT-2",
      player: "QA-002",
      player_name: "Sample Player Two",
      status: "Unmarked",
      modified: "v1",
    },
  ];
  user = "staff@example.test";
  writes = posts = 0;
  lost = deny = false;
};
const result = () => ({ session, rows, can_mark: true });
const server = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, "http://localhost");
    if (url.pathname.startsWith("/api/method/")) {
      res.setHeader("Content-Type", "application/json");
      const method = url.pathname.split(".").at(-1);
      const send = (data) => res.end(JSON.stringify({ message: data }));
      if (method === "bootstrap") {
        send(
          user
            ? {
                authenticated: true,
                user,
                company: "QA Academy",
                academy_name: "QA Sports Academy",
                timezone: "Africa/Lagos",
                today: "2026-11-05",
                csrf_token: "fixture-token",
                can_prepare_biometrics: user === "staff@example.test",
              }
            : { authenticated: false }
        );
        return;
      }
      if (deny) {
        res.writeHead(403);
        res.end(JSON.stringify({ exc_type: "PermissionError" }));
        return;
      }
      if (method === "list_sessions") {
        send({ rows: [session], has_more: false });
        return;
      }
      if (method === "search_players") {
        send([{ name: "QA-001", full_name: "Sample Player One" }]);
        return;
      }
      if (method === "list_player_statuses") {
        send({
          rows: [
            {
              name: "QA-001",
              full_name: "Sample Player One",
              fingerprint_status: biometricRecords[0]?.status || "Not prepared",
              finger: biometricRecords[0]?.finger || "",
              request_name: biometricRecords[0]?.name || "",
              demo_reference: biometricRecords[0]?.demo_reference || null,
            },
            {
              name: "QA-002",
              full_name: "Sample Player Two",
              fingerprint_status: "Not prepared",
              finger: "",
              request_name: "",
            },
          ],
          has_more: false,
        });
        return;
      }
      if (method === "demo_capture") {
        if (failDemo) {
          failDemo = false;
          res.writeHead(503);
          res.end("{}");
          return;
        }
        biometricRecords[0].demo_reference = "DEMO-12345678901234567890";
        send(biometricRecords[0]);
        return;
      }
      if (method === "records") {
        send(biometricRecords);
        return;
      }
      if (method === "prepare" || method === "withdraw") {
        let raw = "";
        for await (const chunk of req) raw += chunk;
        const body = JSON.parse(raw);
        if (method === "prepare") {
          assert.equal(body.consent_confirmed, 1);
          biometricRecords = [
            { name: "BIO-QA-1", status: "Pending capture", ...body.values },
          ];
        } else {
          assert.ok(body.reason);
          biometricRecords[0].status = "Withdrawn";
          biometricRecords[0].withdrawal_reason = body.reason;
        }
        send(biometricRecords[0]);
        return;
      }
      if (method === "configuration") {
        send({
          company: "QA Academy",
          timezone: "Africa/Lagos",
          today: "2026-11-05",
          can_create: !deny,
          programs: [
            { name: "P1", program_name: "Football Development" },
            { name: "P2", program_name: "Foundations" },
          ],
          groups: [
            { name: "G1", group_name: "Under 12", program: "P1" },
            { name: "G2", group_name: "Juniors", program: "P2" },
          ],
        });
        return;
      }
      if (method === "create_session") {
        let raw = "";
        for await (const chunk of req) raw += chunk;
        const body = JSON.parse(raw);
        creationAttempts.push(body);
        if (!creation) {
          creation = body;
          res.writeHead(503);
          res.end("{}");
          return;
        }
        assert.equal(body.request_key, creation.request_key);
        assert.deepEqual(body.values, creation.values);
        send(session.name);
        return;
      }
      if (method === "roster") {
        send(result());
        return;
      }
      if (method === "save_attendance") {
        posts++;
        assert.equal(req.headers["x-frappe-csrf-token"], "fixture-token");
        let raw = "";
        for await (const chunk of req) raw += chunk;
        const body = JSON.parse(raw);
        if (
          body.marks.some((mark) => {
            const row = rows.find((r) => r.name === mark.name);
            return row.status !== mark.status && row.modified !== mark.modified;
          })
        ) {
          res.writeHead(409);
          res.end(JSON.stringify({ exc_type: "TimestampMismatchError" }));
          return;
        }
        for (const mark of body.marks) {
          const row = rows.find((r) => r.name === mark.name);
          if (row.status !== mark.status) {
            row.status = mark.status;
            row.modified = "v" + (++writes + 1);
          }
        }
        if (lost) {
          lost = false;
          res.writeHead(503);
          res.end("{}");
          return;
        }
        send(result());
        return;
      }
      res.writeHead(404);
      res.end("{}");
      return;
    }
    if (!url.pathname.startsWith(ROOT)) {
      res.writeHead(404);
      res.end();
      return;
    }
    const name = path.join(
      out,
      decodeURIComponent(url.pathname.slice(ROOT.length)) || "index.html"
    );
    const content = await readFile(name);
    res.setHeader(
      "Content-Type",
      {
        ".js": "application/javascript",
        ".css": "text/css",
        ".svg": "image/svg+xml",
        ".webmanifest": "application/manifest+json",
      }[path.extname(name)] || "text/html"
    );
    res.end(content);
  } catch (error) {
    res.writeHead(500);
    res.end(String(error));
  }
});

(async () => {
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const url = `http://127.0.0.1:${server.address().port}${ROOT}index.html`;
  const browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox"],
  });
  try {
    for (const width of [1440, 390]) {
      reset();
      const context = await browser.newContext({
          viewport: { width, height: 1000 },
        }),
        page = await context.newPage();
      const errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await page.goto(url);
      await page
        .getByRole("button", { name: "Enable offline attendance" })
        .click();
      creation = null;
      creationAttempts = [];
      await page
        .getByRole("button", { name: "New session", exact: true })
        .click();
      const form = page.getByRole("dialog");
      await form.locator("[name=title]").fill("Training QA");
      await form.locator("[name=program]").selectOption("P1");
      await form.locator("[name=group]").selectOption("G1");
      await form.locator("[name=program]").selectOption("P2");
      assert.equal(await form.locator("[name=group]").inputValue(), "");
      assert.equal(
        await form.locator("[name=group] option[value=G1]").count(),
        0
      );
      assert.equal(
        await form.evaluate(
          (element) => element.scrollWidth <= element.clientWidth
        ),
        true
      );
      await form.screenshot({
        path: `/tmp/sports-attendance-new-session-${width}.png`,
      });
      await form
        .getByRole("button", { name: "Create session", exact: true })
        .click();
      await form.getByRole("alert").waitFor();
      assert.equal(await form.locator("[name=title]").isDisabled(), true);
      await page.reload();
      await page
        .getByRole("button", { name: "New session", exact: true })
        .click();
      await page
        .getByRole("dialog")
        .getByRole("button", { name: "Retry session request" })
        .click();
      await page.getByRole("heading", { name: "Sample Player One" }).waitFor();
      assert.equal(creationAttempts.length, 2);
      await page.getByRole("button", { name: "All sessions" }).click();
      biometricRecords = [];
      await page
        .getByRole("button", { name: "Fingerprint enrollments", exact: true })
        .click();
      const directory = page.getByRole("region", {
        name: "Fingerprint enrollments",
        exact: true,
      });
      await directory
        .getByRole("button", { name: "Find players", exact: true })
        .click();
      await directory
        .locator("tr")
        .filter({ hasText: "QA-001" })
        .getByText("Not prepared", { exact: true })
        .waitFor();
      await directory
        .getByRole("button", { name: "View / prepare", exact: true })
        .first()
        .click();
      const biometric = page.getByRole("dialog");
      assert.equal(await biometric.locator("table").count(), 0);
      await biometric
        .getByRole("heading", {
          name: "Selected player: Sample Player One · QA-001",
        })
        .waitFor();
      await biometric
        .getByLabel("Consent supplied by")
        .fill("Synthetic QA guardian");
      await biometric
        .getByLabel("Consent notice/reference")
        .fill("Synthetic biometric notice QA");
      const consent = biometric.getByRole("checkbox");
      assert.equal(await consent.isChecked(), false);
      assert.equal(
        await biometric
          .getByRole("button", { name: "Prepare capture request" })
          .isDisabled(),
        true
      );
      await consent.check();
      await biometric.evaluate((element) => {
        element.scrollTop = 0;
      });
      await biometric.screenshot({
        path: `/tmp/sports-fingerprint-preparation-${width}.png`,
      });
      await biometric
        .getByRole("button", { name: "Prepare capture request" })
        .click();
      await biometric
        .getByText("BIO-QA-1 · Pending capture", { exact: true })
        .waitFor();
      await directory
        .locator("tr")
        .filter({ hasText: "QA-001" })
        .getByText("Pending capture", { exact: true })
        .waitFor();
      await biometric
        .getByRole("img", {
          name: "Decorative fingerprint illustration — simulated",
        })
        .waitFor();
      failDemo = true;
      await biometric
        .getByRole("button", { name: "Demo capture — generate barcode" })
        .click();
      await biometric
        .getByRole("alert")
        .filter({ hasText: "server could not accept" })
        .waitFor();
      assert.equal(
        await biometric
          .getByText("Demo capture complete", { exact: true })
          .count(),
        0
      );
      await biometric
        .getByRole("button", { name: "Demo capture — generate barcode" })
        .click();
      const scanning = biometric.locator(".demo-fingerprint.is-scanning");
      await scanning.waitFor();
      assert.equal(
        await biometric
          .getByRole("button", { name: "Simulating scan…", exact: true })
          .isDisabled(),
        true
      );
      await page.emulateMedia({ reducedMotion: "reduce" });
      assert.equal(
        await scanning
          .locator(".demo-scan-line")
          .evaluate((e) => getComputedStyle(e).animationName),
        "none"
      );
      await page.emulateMedia({ reducedMotion: "no-preference" });
      await scanning.screenshot({
        path: `/tmp/sports-demo-fingerprint-scanning-${width}.png`,
      });
      await biometric
        .getByRole("img", { name: "Demo barcode DEMO-12345678901234567890" })
        .waitFor();
      await biometric
        .getByText("Demo capture complete", { exact: true })
        .waitFor();
      await biometric.locator(".demo-fingerprint.is-complete").screenshot({
        path: `/tmp/sports-demo-fingerprint-complete-${width}.png`,
      });
      assert.ok((await biometric.locator("svg rect").count()) > 10);
      await directory
        .locator("tr")
        .filter({ hasText: "QA-001" })
        .getByText("Demo captured (simulated)", { exact: true })
        .waitFor();
      assert.equal(biometricRecords[0].status, "Pending capture");
      await biometric
        .getByRole("img", { name: "Demo barcode DEMO-12345678901234567890" })
        .screenshot({ path: `/tmp/sports-demo-barcode-${width}.png` });
      await biometric.evaluate((element) => {
        element.scrollTop = 0;
      });
      await biometric.screenshot({
        path: `/tmp/sports-fingerprint-status-${width}.png`,
      });
      assert.equal(
        await biometric
          .getByRole("button", { name: "Withdraw pending request" })
          .isDisabled(),
        true
      );
      await biometric
        .getByLabel("Withdrawal reason")
        .fill("Guardian withdrew request");
      await biometric
        .getByRole("button", { name: "Withdraw pending request" })
        .click();
      await biometric
        .getByText("BIO-QA-1 · Withdrawn", { exact: true })
        .waitFor();
      await directory
        .locator("tr")
        .filter({ hasText: "QA-001" })
        .getByText("Withdrawn", { exact: true })
        .waitFor();
      assert.equal(await biometric.getByRole("checkbox").isChecked(), false);
      await biometric
        .getByRole("button", {
          name: "Back to fingerprint enrollments",
          exact: false,
        })
        .click();
      assert.equal(await directory.locator("table").count(), 1);
      await directory
        .getByRole("button", { name: "BIO-QA-1", exact: true })
        .click();
      await biometric
        .getByText("BIO-QA-1 · Withdrawn", { exact: true })
        .waitFor();
      await biometric
        .getByRole("button", { name: "Close fingerprint registration" })
        .click();
      await directory.screenshot({
        path: `/tmp/sports-fingerprint-enrollments-${width}.png`,
      });
      await page
        .getByRole("button", { name: "Training sessions", exact: true })
        .click();
      await page.getByRole("button", { name: /Saturday training/ }).click();
      await page.getByRole("heading", { name: "Sample Player One" }).waitFor();
      const card = (name) =>
        page
          .locator("article")
          .filter({ has: page.getByRole("heading", { name }) });
      await page.evaluate(async () => {
        await navigator.serviceWorker.ready;
      });
      await context.setOffline(true);
      assert.equal(
        await page
          .getByRole("button", { name: "New session", exact: true })
          .isDisabled(),
        true
      );
      await card("Sample Player One")
        .getByRole("button", { name: "Present", exact: true })
        .click();
      await page
        .getByText("Saved on this device. Pending synchronization.", {
          exact: true,
        })
        .waitFor();
      await page.reload();
      await page.getByRole("button", { name: /Saturday training/ }).click();
      await card("Sample Player One")
        .getByText("Present · Pending sync")
        .waitFor();
      assert.equal(
        await page.getByRole("button", { name: "Sync now" }).isDisabled(),
        true
      );
      assert.equal(
        await page
          .getByRole("button", { name: "Forget this device" })
          .isDisabled(),
        true
      );
      await page
        .locator('input[placeholder="Name or player ID"]')
        .fill("QA-001");
      assert.equal(await page.locator("article").count(), 1);
      await page.locator('input[placeholder="Name or player ID"]').fill("");
      await context.setOffline(false);
      await page.evaluate(() =>
        fetch("/api/method/sports_app.attendance_mobile_api.bootstrap", {
          cache: "no-store",
        })
      );
      lost = true;
      await page.getByRole("button", { name: "Sync now" }).click();
      await page
        .getByRole("alert")
        .filter({ hasText: "server could not accept" })
        .waitFor();
      await page.getByRole("button", { name: "Sync now" }).waitFor();
      assert.equal(
        writes,
        1,
        `Sync should have reached server (${posts} POSTs)`
      );
      await page.getByRole("button", { name: "Sync now" }).click();
      await page
        .getByText("1 attendance mark synchronized.", { exact: false })
        .waitFor();
      assert.equal(writes, 1);
      await card("Sample Player Two")
        .getByRole("button", { name: "Late", exact: true })
        .click();
      await page
        .getByText("Saved on this device. Pending synchronization.", {
          exact: true,
        })
        .waitFor();
      rows[1].status = "Absent";
      rows[1].modified = "server-concurrent";
      await page.getByRole("button", { name: "Sync now" }).click();
      await card("Sample Player Two")
        .getByText("Needs review", { exact: true })
        .waitFor();
      await page.reload();
      await page.getByRole("button", { name: /Saturday training/ }).click();
      await card("Sample Player Two")
        .getByText("Needs review", { exact: true })
        .waitFor();
      await card("Sample Player Two")
        .locator("input")
        .fill("Coach verified late arrival");
      await card("Sample Player Two")
        .getByRole("button", { name: "Queue reviewed correction" })
        .click();
      await page.getByRole("button", { name: "Sync now" }).click();
      await page
        .getByText("1 attendance mark synchronized.", { exact: false })
        .waitFor();
      assert.equal(rows[1].status, "Late");
      await card("Sample Player One")
        .locator("input")
        .fill("Operator correction");
      await card("Sample Player One")
        .getByRole("button", { name: "Excused", exact: true })
        .click();
      await page
        .getByText("Saved on this device. Pending synchronization.", {
          exact: true,
        })
        .waitFor();
      const previousPosts = posts;
      user = "different@example.test";
      await page.getByRole("button", { name: "Sync now" }).click();
      await page
        .getByRole("alert")
        .filter({ hasText: "account or academy changed" })
        .waitFor();
      assert.equal(posts, previousPosts);
      user = "staff@example.test";
      deny = true;
      await page.getByRole("button", { name: "Sync now" }).click();
      await page
        .getByRole("alert")
        .filter({ hasText: "access was denied" })
        .waitFor();
      assert.equal(posts, previousPosts);
      deny = false;
      await page.getByRole("button", { name: "Sync now" }).click();
      await page
        .getByText("1 attendance mark synchronized.", { exact: false })
        .waitFor();
      await page.evaluate(() => {
        window.qaOpen = indexedDB.open;
        indexedDB.open = () => {
          throw new DOMException(
            "Device storage unavailable for QA",
            "QuotaExceededError"
          );
        };
      });
      await card("Sample Player One")
        .getByRole("button", { name: "Late", exact: true })
        .click();
      await page
        .getByRole("alert")
        .filter({ hasText: "Device storage unavailable for QA" })
        .waitFor();
      await page.evaluate(() => {
        indexedDB.open = window.qaOpen;
        delete window.qaOpen;
      });
      assert.equal(rows[0].status, "Excused");
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth
        ),
        true
      );
      await page.screenshot({
        path: `/tmp/sports-attendance-app-${width}.png`,
        fullPage: true,
      });
      const privacy = await page.evaluate(async () => {
        const db = await new Promise((resolve) => {
          const r = indexedDB.open("sports-attendance-v1");
          r.onsuccess = () => resolve(r.result);
        });
        const identity = await new Promise((resolve) => {
          const r = db.transaction("state").objectStore("state").get("last");
          r.onsuccess = () => resolve(r.result);
        });
        db.close();
        for (const key of await caches.keys()) {
          for (const request of await (await caches.open(key)).keys()) {
            if (new URL(request.url).pathname.startsWith("/api/")) return false;
          }
        }
        return !("csrf_token" in identity);
      });
      assert.equal(privacy, true);
      assert.deepEqual(errors, []);
      page.on("dialog", (d) => d.accept());
      await page.getByRole("button", { name: "Forget this device" }).click();
      await page
        .getByRole("button", { name: "Enable offline attendance" })
        .waitFor();
      await context.close();
    }
    user = "registrar@example.test";
    const registrar = await browser.newPage();
    await registrar.goto(url);
    await registrar
      .getByRole("button", { name: "New session", exact: true })
      .waitFor();
    assert.equal(
      await registrar
        .getByRole("button", { name: "Fingerprint enrollments", exact: true })
        .count(),
      0
    );
    await registrar.close();
    user = null;
    const guest = await browser.newPage();
    await guest.goto(url);
    await guest.getByRole("link", { name: "Sign in to attendance" }).waitFor();
    assert.equal(await guest.locator("article").count(), 0);
    await guest.close();
    console.log(
      "PASS Next attendance desktop/phone: trusted download, real IndexedDB/worker, offline mark/reload, filtering, lost-response retry, reviewed concurrent correction, wrong-account/permission denial, scoped cache privacy, guest sign-in, forget-device protection. API fixtures; no ERP writes."
    );
  } finally {
    await browser.close();
    server.close();
  }
})().catch((error) => {
  console.error(error);
  server.close();
  process.exitCode = 1;
});
