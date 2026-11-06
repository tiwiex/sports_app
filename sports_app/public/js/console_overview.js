/* Sports-owned v1 console view. No accounting APIs or private records. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:overview"] = () => ({
	mount({ container, context }) {
		const title = document.createElement("h3");
		title.textContent = __("Sports Academy");
		const description = document.createElement("p");
		description.textContent = __(
			"Authorized administrators can configure the academy, programs and groups through Academy Settings. Review enrollment applications through Enrollments and manage admitted players and program memberships through Players. Enrollment payment claims require a separate Finance review. Use Attendance for training sessions and manual player attendance."
		);
		const company = document.createElement("p");
		company.textContent = context.company
			? __("Current company: {0}", [context.company])
			: __(
					"No default company selected. Academy configuration will establish the operating context."
			  );
		container.replaceChildren(title, description, company);
	},
});
