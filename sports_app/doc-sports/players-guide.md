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

Search by registration ID or name. Same-name players are allowed after a duplicate-name warning; use registration ID and birth date to distinguish them. Select an ID to open the private profile and its paginated enrollment list. The profile's registration ID link opens the native Sports Player form for contact/name corrections. **New Enrollment** adds a record to the same player and Customer. Selecting an enrollment ID opens the native form for status/date changes. Both interfaces enforce the same server validations and native change history.

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

Sports → Registrations holds public submissions for private review. Acceptance creates the same Player/Customer/User/enrollment records as direct registration and adds a Source registration link. Pending/rejected applications create no Player/User/enrollment. When the applicant uses Make Payment, a prospective Customer and draft Sales Invoice exist before admission; acceptance reuses that Customer. Rejection does not automatically cancel an invoice or refund a receipt. See the [complete PoC workflow](website-prototype.md).

Enrollment invoice references and review states appear in the private registration profile. Finance users open the invoice and use Complete Payment after verifying the full bank credit; the invoice and its allocated receipt submit together, without opening Payment Entry separately. Registrars receive no general finance permissions. Applicant claims remain unposted.
