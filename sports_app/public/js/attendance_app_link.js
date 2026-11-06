/* Sports-owned attendance launcher using the optional host's v1 provider API. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:attendance_app"] = () => ({
	mount({ container }) {
		const card = document.createElement("section");
		card.className = "card p-4";
		const title = document.createElement("h3");
		title.textContent = __("Attendance App");
		const description = document.createElement("p");
		description.textContent = __(
			"Open the dedicated attendance app to download session rosters, mark players offline and synchronize when connected. Create and finalize sessions under Sports → Attendance."
		);
		const link = document.createElement("a");
		link.href = "/sports-attendance";
		link.target = "_blank";
		link.rel = "noopener";
		link.className = "btn btn-primary";
		link.textContent = __("Open attendance app ↗");
		const hint = document.createElement("p");
		hint.className = "text-muted mt-3";
		hint.textContent = __(
			"Opens in a new tab using your existing staff sign-in. Enable offline attendance only on a trusted device."
		);
		card.append(title, description, link, hint);
		container.replaceChildren(card);
	},
});
