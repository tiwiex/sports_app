# Attendance app prototype

Administrators also have a separate **Fingerprint enrollments** table, linking to each player’s **Fingerprint registration** form for [consent and pending capture preparation](fingerprint-preparation-guide.md). No scanner capture, template, identity matching or biometric attendance is available yet.

Open **[Attendance app](https://moyours.ideltatech.com/sports-attendance)**, or use **Boost → Sports → Attendance App → Open attendance app**. This Sports-owned launcher opens the app in a new tab. The existing Attendance screen also retains its toolbar link. Refresh the console after upgrading to load the new menu entry.

1. Sign in using an existing authorized staff account. Sports Registrar, Sports Academy Administrator and System Manager remain the prototype roles, with Company/document permissions. No new roles or public access to players are granted.
2. Choose **New session** while online. Enter the title, program, optional group, date, start/end times and venue. Programs/groups display friendly names; times use the academy timezone. Creation snapshots eligible Active enrollments and opens the new roster on a trusted device. You can also create sessions in Boost; cancellation/finalization remain there. Session and roster creation permissions are required.
3. On a trusted staff device, choose **Enable offline attendance on this device**. Downloaded names/IDs/statuses and locally entered reasons are accessible to others using this browser. The app does not encrypt them; avoid shared/public devices.
4. Select a session while online to download its roster. Before leaving internet coverage, let the app finish preparing its offline shell. Use the installed app icon or keep/bookmark the loaded static app page for offline reopening; the friendly server redirect itself needs internet.
5. Search a name/player ID, filter status and tap Present, Late, Absent or Excused. Choices save locally and show **Pending sync**. They do not change the server until you choose **Sync now** while connected. Corrections to a recorded status require a reason. Future/cancelled/read-only sessions cannot be marked.
6. Reconnect and **Sync now** using the same staff account and academy. If the session expired, sign in again as that operator before retrying. Do not switch accounts to upload another operator's marks.
7. A failed or conflicting batch stays pending, including after reload. Check the downloaded server status. **Use server status** explicitly discards your local choice. **Queue reviewed correction** requires a reason and queues your reviewed choice against the refreshed server version; sync again. Cancelled sessions remain read-only.
8. Resolve all pending marks, then use **Forget this device** to remove this account's downloaded rosters. It is disabled while marks are pending. Logging out of Frappe does not automatically erase device data; forget first when handing the device to another person.

The total counts include pending local choices; they are provisional. Unmarked is not an absence. Finalization in Boost explicitly marks remaining Unmarked players Absent. Other devices may have unsynced choices; coordinate with operators before finalizing. Later changes are reviewed corrections.

Session creation is online only. If its response is interrupted, **Retry session request** uses the original request key. Details stay locked until the outcome is known, including after a tab reload and reopening New session. **Close (keep request)** leaves recovery in the tab; do not clear tab storage while the outcome is uncertain. Validation failures permit corrections. Creation does not enroll new players or change invoices/payments.

Offline identity is valid for seven days from online verification. It does not prove the user is still authorized; the server checks access again at sync. Pending records are retained rather than silently discarded on expiry. Browser storage can be evicted or cleared, so sync promptly. Device capture time is informative; the audit uses server sync time and authenticated operator.

This is a manual attendance prototype. No thumb/face scanning, QR check-in, new biometric records, automatic lateness calculation, coach-assigned-group authorization or public player self-service is implemented. The existing HTML enrollment and finance flows are unchanged.
