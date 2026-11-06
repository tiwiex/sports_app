export async function api(method, args = {}, identity = null) {
	let token;
	if (identity) {
		const who = await api("attendance_mobile_api.bootstrap");
		if (!who.authenticated || who.user !== identity.user || who.company !== identity.company) {
			const error = new Error(
				"Your signed-in account or academy changed. Sign in with the original account before syncing."
			);
			error.kind = "auth";
			throw error;
		}
		token = who.csrf_token;
	}
	const query = identity ? "" : "?" + new URLSearchParams(args);
	const response = await fetch(`/api/method/sports_app.${method}${query}`, {
		method: identity ? "POST" : "GET",
		credentials: "same-origin",
		cache: "no-store",
		...(identity
			? {
					headers: {
						"Content-Type": "application/json",
						"X-Frappe-CSRF-Token": token,
					},
					body: JSON.stringify(args),
			  }
			: {}),
	});
	const data = await response.json().catch(() => ({}));
	if (!response.ok || data.exc) {
		const error = new Error(
			data.exc_type === "TimestampMismatchError"
				? "Attendance changed on the server. Review the latest status before retrying."
				: [401, 403].includes(response.status)
				? "Your session expired or attendance access was denied. Sign in again; local marks remain saved."
				: "The server could not accept this request. Local marks remain saved; check the session and your permissions before retrying."
		);
		error.kind =
			data.exc_type === "TimestampMismatchError"
				? "conflict"
				: [401, 403].includes(response.status)
				? "auth"
				: "server";
		error.status = response.status;
		throw error;
	}
	return data.message;
}
