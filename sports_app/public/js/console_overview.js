/* Sports-owned v1 console view. No accounting APIs or private records. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:overview"] = () => ({
	mount({ container, context }) {
		const title = document.createElement("h3");
		title.textContent = __("Sports Academy");
		const description = document.createElement("p");
		description.textContent = __("Authorized administrators can configure the academy, programs and groups through Academy Settings. Player registration, billing and attendance are not yet available.");
		const company = document.createElement("p");
		company.textContent = context.company
			? __("Current company: {0}", [context.company])
			: __("No default company selected. Academy configuration will establish the operating context.");
		container.replaceChildren(title, description, company);
	},
});
