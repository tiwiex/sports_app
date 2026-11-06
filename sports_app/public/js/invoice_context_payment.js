/* Sports owns enrollment settlement; Boost remains an optional console host. */
(() => {
	if (window.__sportsInvoiceContextPayment) return;
	window.__sportsInvoiceContextPayment = true;
	const pending = new Set();
	document.addEventListener(
		"click",
		async (event) => {
			const toggle = event.target.closest(".ing-console-action-menu-toggle");
			if (!toggle) return;
			const menu = toggle.closest(".ing-console-action-menu");
			menu.querySelectorAll("[data-sports-confirm-payment]").forEach((item) =>
				item.closest("li").remove()
			);
			if (menu.classList.contains("is-open")) return;
			const view = menu.querySelector('[data-row-open][data-doctype="Sales Invoice"]');
			if (!view) return;
			const name = view.dataset.name;
			const request = {};
			menu.__sportsPaymentRequest = request;
			try {
				const response = await frappe.call({
					method: "sports_app.enrollment_invoices.completion_access",
					args: { name },
				});
				if (
					!response.message ||
					!menu.isConnected ||
					!menu.classList.contains("is-open") ||
					menu.__sportsPaymentRequest !== request
				)
					return;
				const item = document.createElement("li");
				const button = document.createElement("a");
				button.href = "#";
				button.className = "dropdown-item";
				button.dataset.sportsConfirmPayment = "1";
				button.textContent = __("Confirm Payment");
				button.addEventListener("click", async (click) => {
					click.preventDefault();
					if (pending.has(name)) return;
					pending.add(name);
					try {
						await frappe.call({
							method: "sports_app.enrollment_invoices.complete_payment",
							args: { name },
							freeze: true,
							freeze_message: __("Confirming invoice payment…"),
						});
						item.remove();
						// Refresh the host list without opening a document or Payment Entry form.
						let wrapper = menu;
						while (wrapper && !wrapper.boost_console) wrapper = wrapper.parentElement;
						if (wrapper)
							await wrapper.boost_console.refresh_current_data({
								partial: true,
							});
						frappe.show_alert({
							message: __("Payment confirmed and allocated to this invoice."),
							indicator: "green",
						});
					} finally {
						pending.delete(name);
					}
				});
				item.append(button);
				view.closest("li").after(item);
			} catch (error) {
				// The existing View action remains available if eligibility cannot be loaded.
				console.warn("Sports payment menu unavailable", error.message);
			}
		},
		true
	); // Capture before the host stops propagation on its menu toggle.
})();
