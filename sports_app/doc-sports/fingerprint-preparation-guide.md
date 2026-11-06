# Fingerprint registration preparation

Open the [Attendance App](https://moyours.ideltatech.com/sports-attendance), sign in as **Sports Academy Administrator** or **System Manager**, then choose **Fingerprint enrollments**. Existing attendance operators do not automatically receive consent/preparation administration rights.

The separate **Fingerprint enrollments** view contains a searchable table: player name/ID, latest request's status, finger/reference and **View / prepare** action. Players without any request show **Not prepared**; others show **Pending capture**, **Demo captured (simulated)** or **Withdrawn**. Demo status is a separate simulation indicator; real capture remains pending. Search by name/ID and use Previous/Next players (20 per page). The table refreshes after changes. On phones, scroll the table horizontally for all columns. No real Captured/Enrolled status is available without hardware integration.

1. Find an existing player in the table and choose **View / prepare**, or click their enrollment reference. This opens **Fingerprint registration** for that player. Confirm the selected name and ID; same-name players have distinct IDs. Request references remain visible in the form/history. **Back to fingerprint enrollments** returns to the table with its search and page preserved. **Training sessions** returns to attendance.
2. Review existing capture requests. A player may have only one **Pending capture** request at a time.
3. Select the finger intended for later capture. Record who actually supplied the biometric consent, their relationship, the actual notice/consent reference and its date. These fields are staff-entered evidence metadata, not an automated verification of guardian authority or a complete consent policy.
4. Tick the confirmation only when consent was actually supplied, then **Prepare capture request**. Nothing is pre-confirmed. The result stays **Pending capture**; no scanner interaction takes place.
5. To withdraw, provide a reason and choose **Withdraw pending request**. The record becomes **Withdrawn** and retains native change history. A subsequent preparation requires a new explicit consent confirmation; previous records remain visible.

## Demo capture / barcode

The demo includes a fixed decorative fingerprint illustration. When you choose Demo capture, a simulated scan line animates while the demo request runs, then **Demo capture complete** appears after server confirmation. The drawing is identical for every player, always labelled **SIMULATED — NO SCANNER**, and is not a player's fingerprint. Reduced-motion settings disable the moving line; failed requests do not display success. The existing demo barcode/code remains underneath the illustration.

After preparing a request, choose **Demo capture — generate barcode**. The server creates a random reference such as `DEMO-12345678901234567890` and records the operator/time. A CODE128 barcode displays that exact reference. Retrying returns the same code; it cannot be regenerated or changed on that request. A withdrawn request cannot receive a demo capture, and its historical code is labelled withdrawn instead of shown as an active barcode.

The player list shows **Demo captured (simulated)**. The underlying real capture status remains **Pending capture**. This barcode is a demo identifier, not a fingerprint, secret, login token or attendance credential. Scanning/copying it does not currently mark attendance; no barcode check-in or matching endpoint is implemented. The graphical code has not been tested with physical scanner hardware.

Preparation and withdrawal require internet. Consent details stay in component memory and the private server record, not in the offline roster database or service-worker cache. Unchanged retries use the same in-memory request key. After a reload following an uncertain outcome, search/select the player and review their existing request; the server refuses a second pending request.

This records preparation only. It **does not capture a fingerprint, store an image/template, bind a scanner identity, verify a match, or mark biometric attendance**. There is no Enrolled/Captured status or manual override. Withdrawal concerns the preparation request; no provider deletion is performed because no fingerprint was captured.

Before actual capture, select the scanner/provider and validate its SDK/API, device identity, enrollment confirmation, failure/retry behavior, consent/guardian authority and retention/deletion arrangements. Those remain US-007-01 acceptance work. Manual attendance and HTML enrollment remain unchanged.
