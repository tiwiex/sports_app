# Players and their Customers

Open **Boost Console → Sports → Players** on the development site. System Manager and Sports Academy Administrator can use it; a registrar can instead receive **Sports Registrar**. Sports Console alone does not grant private player access. Normal Company/User Permissions apply. The registration service can create the player's Customer and contact; the registrar receives no general Customer creation, financial transaction or accounting role. Existing users are not assigned new roles automatically.

## Register a player

1. Complete Academy Settings, including numbering and a default program. The optional default group is applied to the initial enrollment.
2. Choose **Register Player**. Enter the player's name, a valid unique player email, contact/guardian details, program/group, start date and enrollment status. Programs and groups display their friendly names.
3. Save once. Registration creates a permanently numbered player, their own Individual Customer, a disabled Website User, and the first enrollment together. The Customer uses the player's name, email and phone. Guardian information remains on the player.

No separate Customer setup or payer selection is required. Each player receives a different Customer, including players with matching names or family details; each new player must have a different email. All of a player's enrollments use that player's Customer. Repeating the same registration request returns the existing player and Customer. Validation failures leave no player, User, Customer, contact or enrollment behind.

The Customer's group is the initial program's friendly name, created automatically under ERPNext's existing Customer Group root when needed. An existing compatible leaf category is reused. Further enrollments do not move the Customer into another group. Territory uses ERPNext's default, falling back to an existing Territory matching the academy Company's country; missing territory/root setup raises a configuration error. No category or Customer creation permission is granted to the registrar outside this background operation.

Registration numbers use the configured prefix and digit count. Correcting a name does not change the number, Customer link or registration timestamp. Renaming/merging player IDs or assigning another player's Customer is prohibited. Customer IDs derive from the player ID; their display names are the player names. Customer/contact details are copied at registration; later Customer edits use the operator's ERPNext permissions.

## Maintain the player and enrollment

Search by registration ID or name. Same-name players are allowed after a duplicate-name warning; use registration ID and birth date to distinguish them. Select an ID to open the private profile and its paginated enrollment list. The profile's registration ID link opens the native Sports Player form for contact/name corrections. **New Enrollment** adds a record to the same player and Customer. Selecting an enrollment ID opens the native form for status/date changes. Both interfaces enforce the same server validations and native change history.

Pending and Suspended enrollments are ineligible. Active enrollments are eligible from the start date through an optional end date, inclusive. Withdrawn and Completed enrollments require an end date and are ineligible. This is current enrollment eligibility, not a reconstruction of past status changes. Do not delete/recreate a player to withdraw them. Program/company and group/program must match; used program/group scope cannot move away from its enrollment history.

## Financial scope

The player's Customer is the bridge into ERPNext. Customer links open the existing ERPNext record within the operator's permissions. Registration creates no invoices, payments, receivables or copied balances. Player-attributed invoices, obligations, receipts and reconciliation belong to the billing/payment stories. Attendance, public applications, scholarship records and private attachments remain separate delivery work.

## Future self-service account

Registration prepares a disabled Website User linked to the player and Customer contact. It has the Sports Player role, no Desk or accounting access, and receives no password, welcome email or invitation. Portal activation and access to the player's own records are separate future work. Existing players are not backfilled. Emails already used by a User or player are rejected; email changes after account creation require administrator review.

## User role administration

System Manager can view the native User form's Roles & Permissions editor, including on Administrator. The development Boost repair restores Frappe's standard System Manager permissions; it grants no new role-administration powers to Boost Admin.
