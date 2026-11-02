# Build log: Moyours TLS certificate activation

- Date: 2026-11-01 (Africa/Lagos)
- Related story / epic: US-001-01 / EPIC-001; development-site hosting readiness
- Requirement: SPORTS-NFR-009; secure access to the academy development site
- App / branch: Sports documentation / story/us-005-01-enrollment-payment-review; no app runtime changes
- Status: Verified; approved activation completed
- Site: moyours.ideltatech.com

## Intended outcome and starting context

Firefox blocks the site with SSL_ERROR_BAD_CERT_DOMAIN because the presented certificate covers songhai.erpnow.com.ng instead of the Moyours hostname. The user has already run Let's Encrypt.

## Diagnosis and verification

- DNS resolves Moyours to the expected server IPv4 address; no IPv6 DNS address was returned in the check.
- A live Python TLS connection using the normal trust/hostname checks reproduces the hostname mismatch.
- The issued public certificate has CN/SAN moyours.ideltatech.com, was issued on 1 November 2026 and expires on 30 January 2027. Its files are already referenced by the Moyours site configuration and the generated development Nginx configuration. Private-key contents were not read or copied.
- Nginx loads `/etc/nginx/conf.d/frappe-bench-dev.conf`, a regular copied file last updated in July. It has no Moyours virtual host. The current `/home/frappe/frappe-bench-dev/config/nginx.conf` contains the correct HTTPS server and HTTP redirect. The active default TLS virtual host therefore presents the unrelated certificate.
- The current active Nginx configuration passes syntax validation. A staged full configuration substituting the generated development config also passes `nginx -t -c /tmp/moyours-tls-review/nginx.conf`.
- Semantic comparison confirms all existing server blocks and upstreams are preserved. Only the two Moyours server blocks are added. Removed explicit per-server access/error log destinations match the inherited parent defaults. Existing unrelated duplicate-name and OCSP warnings are unchanged.

## Prepared activation and recovery

Review plan: `/tmp/moyours-tls-review/plan.md`. Proposed action: back up the stale active copied file outside the `*.conf` include pattern, replace it with a symlink to the current bench-generated config, validate active `nginx -t`, then gracefully reload Nginx. Restore the original file before any reload if validation fails. After activation, verify the public certificate with hostname checking enabled, the HTTP redirect and the academy page.

Explicit approval was requested because Nginx is shared with other live sites. No certificate reissue, HSTS removal or browser certificate bypass is proposed. At the diagnostic stage, nothing had been installed or reloaded. The user subsequently explicitly approved activation and graceful reload. No financial data, roles, users, app code, DNS records, private keys, commits or pushes changed. Activation and post-reload verification are recorded below.


## Approved activation and observed results

- User explicitly approved backing up and activating the validated development configuration and gracefully reloading shared Nginx.
- Backup retained at `/etc/nginx/conf.d/frappe-bench-dev.conf.bak-moyours-20261101T211814Z`, outside the active `*.conf` include pattern. Original ownership and permissions were preserved.
- Active `/etc/nginx/conf.d/frappe-bench-dev.conf` now links to `/home/frappe/frappe-bench-dev/config/nginx.conf`. The generated configuration itself was unchanged.
- Repeated semantic/staged validation passed before replacement; active `nginx -t` passed afterward. `systemctl reload nginx` succeeded at 21:18 UTC (22:18 Africa/Lagos). Rollback protection was prepared but not needed.
- Public Python TLS handshake passed normal CA trust and hostname verification using TLS 1.3. Presented SAN is `moyours.ideltatech.com`; expiry is 30 January 2027 at 20:08:37 UTC.
- Academy HTTPS returned HTTP 200. HTTP `/academy` returned 301 to its HTTPS URL.
- Headless Chromium with normal certificate validation loaded `/academy` with HTTP 200 and heading “Big dreams. Real opportunity.” Security details confirm Moyours certificate, issuer YE1, TLS 1.3.
- Existing `https://ideltatech.com/proposal/moyours/` also returned HTTP 200 with normal certificate validation after reload.

## Release impact, cleanup and limitations

The correct Moyours HTTPS virtual host is now active. No certificate reissue, DNS changes, browser verification bypass, application restart, business-data changes or temporary QA accounts were required. No private-key contents were accessed. Existing unrelated duplicate-server-name and OCSP warnings remain; this repair does not establish overall infrastructure health. Backup is retained for recovery. No commit or push was performed.
