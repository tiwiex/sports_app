# Configure an academy

Open the shared console at `/app/boost-console`, expand **Sports**, and select **Academy Settings**.

System Managers can configure the academy. For a configuration-only operator, assign **Sports Academy Administrator** and restrict their allowed Company records with standard Frappe User Permissions. Both supported administrator roles receive read-only Company/Currency master access for configuration, with company User Permissions still enforced. The Sports role grants no accounting transaction permissions. Basic **Sports Console** users can open Sports but cannot view or change settings.

## First setup

1. Select the academy's existing ERPNext Company. Only permitted companies are listed.
2. Use **New Program** to add a program name, sport and company. Sports are free text, so swimming, tennis, football or another sport can be configured without code changes.
3. Use **New Group** to add a group under an enabled program. The company follows the program.
4. Enter academy name, fee currency and timezone. Select an enabled default program and, optionally, a default group belonging to it.
5. Set a registration prefix of 2–20 uppercase letters, digits or hyphens, starting with a letter; choose 4–10 digits. The displayed example is a preview and does not allocate a player ID. Existing IDs will never be renumbered by changing these defaults.
6. Select Pending or Active as the default enrollment status. If monthly fees are enabled, enter a positive default monthly fee. Otherwise explicitly disable monthly fees.
7. Select **Save Settings**. Refreshing the view reads the saved configuration.

Programs and groups can be edited from the same screen. Choose replacement defaults before disabling or moving a default program/group. A program with groups cannot be moved to another company. Saving settings with an unrelated or disabled default is rejected.

One academy configuration per Frappe site is supported by this story. Program/group records have explicit company scope; this does not implement multiple independent academy configurations on one site.

## Scope of these defaults

Saving settings does not register a player, allocate a registration number, generate an invoice, collect payment or publish website branding. The monthly fee is a configuration default for future fee plans. Effective pricing, proration, tax/account mappings and invoicing remain in the fee-plan and billing stories. The public website is US-001-02.

The demo site's business defaults are left for academy staff to select. Verification uses temporary fixtures and restores the original state afterward.

## Installation and access

Sports App requires ERPNext for Company/currency masters. Boost is optional for native setup; the Sports menu requires the compatible Boost console provider host. Standard install/migrate hooks create the two Sports roles and synchronize the optional host's Page roles. Existing users are not assigned new roles automatically.

For a controlled schema-only development update after source changes, run role setup before model sync, then console setup and cache clearing. This story used that sequence on the backed-up `moyours.ideltatech.com` site rather than running unrelated historical migrations.

Native DocType forms remain available to authorized administrators for support. The same server validations apply to native forms, REST writes and the Sports console endpoints.
