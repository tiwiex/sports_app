# Players and their Customers

Open **Boost Console → Sports → Players** on the development site. System Manager and Sports Academy Administrator can use it; a registrar can instead receive **Sports Registrar**. Sports Console alone does not grant private player access. Normal Company/User Permissions apply. The registration service can create the player's Customer and contact; the registrar receives no general Customer creation, financial transaction or accounting role. Existing users are not assigned new roles automatically.

## Register a player

1. Complete Academy Settings, including numbering and a default program. The optional default group is applied to the initial enrollment.
2. Choose **Register Player**. Enter the player's first/last names, birth date, gender, a valid unique player email and the required guardian contact/address details, program/group, start date and enrollment status. Programs and groups display their friendly names.
3. Save once. Registration creates a permanently numbered player, their own Individual Customer, a disabled Website User, and the first enrollment together. The Customer uses the player's name, email and phone. Guardian information remains on the player.

No separate Customer setup or payer selection is required. Each player receives a different Customer, including players with matching names or family details; each new player must have a different email. All of a player's enrollments use that player's Customer. Repeating the same registration request returns the existing player and Customer. Validation failures leave no player, User, Customer, contact or enrollment behind.

The Customer's group is the initial program's friendly name, created automatically under ERPNext's existing Customer Group root when needed. An existing compatible leaf category is reused. Further enrollments do not move the Customer into another group. Territory uses ERPNext's default, falling back to an existing Territory matching the academy Company's country; missing territory/root setup raises a configuration error. No category or Customer creation permission is granted to the registrar outside this background operation.

Registration numbers use the configured prefix and digit count. Correcting a name does not change the number, Customer link or registration timestamp. Renaming/merging player IDs or assigning another player's Customer is prohibited. Customer IDs derive from the player ID; their display names are the player names. Customer/contact details are copied at registration; later Customer edits use the operator's ERPNext permissions.

## Maintain the player and enrollment

Search by registration ID or name. Same-name players are allowed after a duplicate-name warning; use registration ID and birth date to distinguish them. Sort by Player ID, Name, Birth date, Company or Registered on using the column headers. Open the Player ID reference menu and choose **View** to open a grouped profile modal while keeping your list and search in place.

The profile groups the player summary, linked accounts, paginated program enrollments, player/guardian/emergency contacts and consent choices. **Open player record** opens the native Sports Player form for corrections. **New program enrollment** appears in the reference menu and profile for operators permitted to create enrollments and update that player; it adds membership to the same player and Customer. Selecting an enrollment ID opens the native form for status/date changes. Both interfaces enforce the same server validations and native change history.

Pending and Suspended enrollments are ineligible. Active enrollments are eligible from the start date through an optional end date, inclusive. Withdrawn and Completed enrollments require an end date and are ineligible. This is current enrollment eligibility, not a reconstruction of past status changes. Do not delete/recreate a player to withdraw them. Program/company and group/program must match; used program/group scope cannot move away from its enrollment history.

## Financial scope

The player's Customer is the bridge into ERPNext. Customer links open the existing ERPNext record within the operator's permissions. Registration creates no invoices, payments, receivables or copied balances. Player-attributed invoices, obligations, receipts and reconciliation belong to the billing/payment stories. Attendance, production application hardening, scholarship records and private attachments remain separate delivery work.

## Future self-service account

Registration prepares a disabled Website User linked to the player and Customer contact. It has the Sports Player role, no Desk or accounting access, and receives no password, welcome email or invitation. Portal activation and access to the player's own records are separate future work. Existing players are not backfilled. Emails already used by a User or player are rejected; email changes after account creation require administrator review.

## User role administration

System Manager can view the native User form's Roles & Permissions editor, including on Administrator. The development Boost repair restores Frappe's standard System Manager permissions; it grants no new role-administration powers to Boost Admin.


## Extended enrollment details

Staff registration and the public demo share the same field definition. Capture preferred position, school, medical notes, guardian relationship/alternative phone/email, home address and an optional emergency contact. Enter both emergency name and phone if using a different contact. First/last names produce the full display name. Required fields are marked in the new dialog; legacy full-name records and existing full-name-only integrations remain supported without a forced backfill.

The player email is unique and creates their future account. Guardian email is separate and may be shared; it is never silently used as the player's login. Guardian details do not create a shared-family Customer. New Customers/Contacts still use the player's name and supplied player email/phone. Address, medical and consent information remains on the private Sports Player record and is not copied into public website content or financial Contact notes.

Medical, photo/video and terms choices start unchecked. Record only guardian-provided choices; media permission is optional. These fields capture the supplied choice, with native change history, and do not represent a complete versioned consent/contract workflow. Public submission now creates a private Sports Registration; staff acceptance invokes this player-registration service. The generic app rejects future birth dates but does not impose the source site's 4–18 age policy; program-specific age eligibility remains later configuration.

In the native form, edit first/last names for structured records; full name is derived. Legacy records with no structured names retain full-name correction. Existing automatically linked User/Customer names are registration snapshots, unchanged by later player-name corrections.

## Website applications

Sports → Enrollments holds public submissions for private review. Acceptance creates the same Player/Customer/User/enrollment records as direct registration and adds a Source registration link. Pending/rejected applications create no Player/User/enrollment. When the applicant uses Make Payment, a prospective Customer and draft Sales Invoice exist before admission; acceptance reuses that Customer. Rejection does not automatically cancel an invoice or refund a receipt. See the [complete PoC workflow](website-prototype.md).

Enrollment invoice references and review states appear in the private registration profile. Finance users open the invoice and use Complete Payment after verifying the full bank credit; the invoice and its allocated receipt submit together, without opening Payment Entry separately. Registrars receive no general finance permissions. Applicant claims remain unposted.

## Confirmed player numbering and public age rule — 6 November 2026

User clarification confirms BA-QNR-001-Q02-07/Q02-08: **MSA + two-digit creation year + hyphen + two-digit creation month + continuous serial**, e.g. `MSA26-08005` followed by `MSA26-09006`. The sequence also continues across year boundaries. The backend uses the academy timezone and a locked Company-scoped counter whose key excludes month, year, editable prefix and application series. Minimum sequence width defaults to three digits and expands naturally; prefix/width remain management settings. On first initialization, seed after the highest existing matching player reference in that Company. Existing prototype IDs of another format stay unchanged and are not interpreted as legacy serials. Existing IDs are immutable; no identity, Customer or finance references are renamed.

The player reference is independent of the configurable **enrollment application** series (`MSA-ENR-.YYYY.-.#####`), accepted Sports Enrollment membership IDs and ERPNext invoice numbering. Current development player defaults are MSA / 3 digits. This supersedes the old prefix-plus-counter-only player ID format for new players.

Public HTML enrollment accepts ages **4 through 18 inclusive**, calculated from calendar birthdays against the academy-local date. Show an inline age error and enforce date bounds in the browser; reject invalid ages in the server-owned public application controller before creating a successful application/invoice. Under-4, 19-or-older and future DOBs are rejected. A February 29 birthday reaches the next age on March 1 in a non-leap year. Enforce on new applications/DOB corrections, without retroactively blocking unchanged historical applications or imposing this public intake policy on ordinary updates to existing player records. Private staff intake policy is not broadened by this web-form refinement.

Provenance: numbering is **Both** (baseline plus questionnaire, now user-confirmed); the explicit 4–18 public restriction is user direction informed by the supplied web-form screenshot, not a claim that the questionnaire stated those exact limits.

[Build evidence](build-logs/2026-11-06-us-003-02-player-series-and-public-age-policy.md).

## Player email preflight and shared guardian identity — 6 November 2026

User refinement: a player email must be unique before public enrollment is submitted, not only when staff accepts it. Normalize player email; reject addresses already used by a User (including email-field aliases such as Administrator), Sports Player or another Pending Sports Registration. Rejected applications release their pending reservation. Browser preflight runs on leaving the player-email field and again before Make Payment/Submit, returning only availability; server validation remains authoritative under the existing settings lock. Preserve token-bound unchanged retries. Show a specific inline error and retain entered details. Review older applications again before financial completion, so a known conflicting email does not start the posting process.

At authorized acceptance/direct player registration, create the player's separate disabled Website User and create or reuse the guardian User. A server-owned **guardian_user** link on Sports Player supports many players to one guardian. Siblings retain separate player emails, Users, Customers and enrollment/finance histories. Player and guardian email on one form must differ. New guardian accounts are disabled Website Users without Desk roles or welcome mail; existing guardian accounts retain their original type, enabled state, roles and profile. Guardian email repetition is permitted; it never becomes a shared payer Customer. Account creation/linkage participates in the same admission transaction and rolls back on failure.

A supplied guardian email is an unverified identity reference, not proof of guardianship or permission to access children. This change does not activate accounts, grant guardian portal permissions, send invitations or implement the parent portal. Existing records are not bulk-backfilled or automatically merged; existing duplicate applications require staff/Finance correction. This user-approved account preparation refines the earlier player-only provisioning decision while leaving portal activation/access as separate scope.

[Build evidence](build-logs/2026-11-06-us-003-01-email-preflight-and-guardian-users.md).


## Import existing players before launch

1. Configure Company, default program, **Player ID prefix** (for example MSA) and sequence digits in Academy Settings.
2. Clean the legacy roster: one unique player ID and unique player email per player. Repeated guardian emails are allowed. Resolve conflicts with existing Users/players/pending applications before import; existing player accounts are not automatically reused.
3. A permitted academy manager with native Data Import access opens `/app/data-import`, selects **Sports Player → Insert New Records**, and downloads/maps the template. Include the **ID** column and place the exact legacy reference there, such as `MSA17-08005`. Include Player name, Company and unique Player email, plus available profile details. Leave Customer, self-service User, guardian User, request metadata and source registration links unset; the server owns those fields. Follow required fields in the template; do not invent missing player/consent data.
4. Run a small reviewed batch and inspect the native per-row import log. Successful IDs stay unchanged, and matching numeric suffixes advance the continuous Company counter. Failed rows must be corrected, not admitted under replacement identities. Native import handles rows individually; a batch is not all-or-nothing.
5. In Academy Settings, set **Player starting sequence** to the next reconciled number. For example after suffix 125 use `126`. This is a minimum, not a counter reset; a higher previously issued/imported number wins. A different historical prefix/format is retained but needs this explicit sequence setting. The preview illustrates the configured minimum, not a guaranteed next allocation.
6. Create program enrollments through the staff workflow and reconcile roster/account totals before opening public intake. No historical fees, payments or attendance are fabricated by importing a player.

Public applicants and ordinary staff registration cannot supply arbitrary player IDs. Existing IDs cannot be renamed/merged. Changing the player prefix or starting sequence only affects future automatic IDs, independently of application/invoice series. Imported users stay disabled without welcome email/portal activation, consistent with ordinary intake. No actual client roster has been imported by this adjustment.

[Build evidence](build-logs/2026-11-06-us-003-02-legacy-import-and-sequence-floor.md).


## Correct an existing player ID

An academy administrator with write access can open **Players → player ID menu → Change Player ID**, use the same action inside the profile, or open the native Sports Player form. Enter the corrected unused ID and a reason, then select **Change Player ID**. A stale form must be refreshed before saving. IDs may contain 2–140 letters, digits, hyphens or underscores, starting with a letter/digit. Case-only changes and merges are prohibited.

The action updates linked records and attachments while keeping Customer/User accounts and financial documents unchanged. It does not reset numbering; a higher corrected number advances the sequence. Open **ID change history** in the profile to inspect previous/new IDs, reason, operator and timestamp. Existing and retired IDs cannot be reassigned to another player or used to reverse a correction; choose a fresh ID for any subsequent correction. General native Rename remains disabled.

After correction, refresh online attendance/fingerprint lists and downloaded attendance rosters. Keep pending offline changes for explicit sync/conflict review; do not delete their local queue. A changed stale attendance mark is rejected until reviewed against the refreshed roster. Old-ID fingerprint preparation retries are not automatically replayed under the new identity.

The previous immutable-ID guidance has this explicit, audited management exception. During initial setup, importing the correct legacy ID remains preferable to correcting IDs later. No existing real players were renamed when enabling this feature.

[Build evidence](build-logs/2026-11-06-us-003-02-audited-player-id-correction.md).

## Linked histories and development observations

Open **Players → Player ID → View**. Each history has its own More/Previous controls and links to its source records. Invoices, receipts and submitted-invoice outstanding balances follow your existing finance access. Balances stay separate by currency; they exclude draft/cancelled invoices and do not include unallocated advances. A Restricted section means your access does not permit that history, not that the player's balance is zero. Attendance links show permitted session details. Management can also read fingerprint preparation history; demo references are not captured fingerprints.

Use **Edit preferred foot** for a current preference. Use **Add measurement** to record assessment date, height (cm), weight (kg), or both. Values must be at least 0.01; future dates and dates before birth are rejected. History is append-only: record a new observation instead of editing an old measurement.

Management uses **Add private document** for a birth certificate, medical report or other supporting file. Enter a title and optionally the source document date. Choose an unencrypted, inactive PDF (up to 5 MB/100 pages) or JPEG/PNG/WebP image (up to 2 MB). The private archive is created automatically and retains uploader/time provenance. Files cannot be made public, moved, replaced or deleted through ordinary controls. A repeated save with the same request creates one archive, not duplicates. This archive submission does not submit an invoice. A retention/deletion process still needs policy agreement before production medical-document use.

These features create no invoices/payments, activate no player/guardian login, and grant no extra ERPNext finance permissions. [Build log](build-logs/2026-11-06-us-003-03-central-player-record.md).

## Player profile tabs — 6 November 2026

The central profile uses **Player details**, **Program enrollments**, **Invoices & receipts**, **Attendance & fingerprint**, **Measurements**, and **Documents** tabs. Player identity and common actions remain visible above the tab strip. Choose a tab or use arrow/Home/End keys while focusing the tab strip; on phones, scroll the strip horizontally. Only the selected panel is displayed. Same-player membership paging/refresh retains the active tab; a different player starts at Player details. Creating a program enrollment opens Program enrollments. Each history retains its own pagination and existing permission restrictions. This is a Sports-only presentation refinement, with no financial, document-security or public-enrollment behavior change. [Build log](build-logs/2026-11-06-us-003-03-tabbed-player-profile.md).

Player photo placement refinement (6 November 2026): a permitted private portrait appears beside the player name in the persistent header above the tabs, remaining visible across sections. Age and preferred foot stay within Player details. No photo duplication or privacy changes. [Build log](build-logs/2026-11-06-us-003-03-profile-header-photo.md).
