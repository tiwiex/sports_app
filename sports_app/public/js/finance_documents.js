/* Sports-owned finance links and deliberate, permission-checked receipt delivery. */
frappe.provide("frappe.sports_finance_documents");
frappe.sports_finance_documents = {
	pdfLink(doctype, name) {
		const a = document.createElement("a");
		a.textContent = name;
		a.href =
			"/api/method/frappe.utils.print_format.download_pdf?" +
			new URLSearchParams({
				doctype,
				name,
				format:
					doctype === "Sales Invoice"
						? "Sports Academy Invoice"
						: "Sports Academy Receipt",
			});
		a.target = "_blank";
		a.rel = "noopener noreferrer";
		a.title = __("Open PDF");
		a.style.cssText =
			"color:var(--blue-600,#1769aa);text-decoration:underline;text-underline-offset:3px;font-weight:600;display:inline-flex;align-items:center;gap:6px";
		const icon = document.createElement("small");
		icon.textContent = "PDF ↗";
		icon.setAttribute("aria-hidden", "true");
		a.append(icon);
		a.addEventListener("click", (event) => {
			if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
			event.preventDefault();
			this.openPdf(doctype, name, a.href);
		});
		return a;
	},
	openPdf(doctype, name, url) {
		const href = url || this.pdfLink(doctype, name).href;
		const dialog = new frappe.ui.Dialog({
			title: __("PDF preview") + " · " + name,
			size: "extra-large",
			fields: [{ fieldname: "preview", fieldtype: "HTML" }],
		});
		const wrapper = dialog.fields_dict.preview.$wrapper;
		const frame = document.createElement("iframe");
		frame.src = href;
		frame.title = __("PDF preview");
		frame.style.cssText =
			"width:100%;height:72vh;border:1px solid var(--border-color,#ddd);border-radius:8px";
		const download = document.createElement("a");
		download.href = href;
		download.target = "_blank";
		download.rel = "noopener noreferrer";
		download.textContent = __("Open / download PDF ↗");
		download.className = "btn btn-default btn-sm";
		download.style.marginBottom = "12px";
		const help = document.createElement("p");
		help.textContent = __(
			"If your browser cannot display the PDF here, use Open / download PDF."
		);
		help.className = "text-muted";
		wrapper.empty();
		wrapper.append(download, help, frame);
		dialog.show();
		dialog.$wrapper?.on("hidden.bs.modal", () => {
			frame.src = "about:blank";
		});
	},
	elapsed(seconds) {
		if (seconds == null || !Number.isFinite(Number(seconds))) return "—";
		const n = Math.max(0, Number(seconds));
		if (n < 60) return __("Less than a minute ago");
		const count = Math.floor(n / (n < 3600 ? 60 : n < 86400 ? 3600 : 86400));
		return `${count} ${
			n < 3600
				? count === 1
					? __("minute")
					: __("minutes")
				: n < 86400
				? count === 1
					? __("hour")
					: __("hours")
				: count === 1
				? __("day")
				: __("days")
		} ${__("ago")}`;
	},
	ageCell(seconds, signal) {
		const el = document.createElement("span"),
			started = Date.now();
		const update = () => {
			el.textContent = this.elapsed(
				seconds == null ? null : Number(seconds) + (Date.now() - started) / 1000
			);
		};
		update();
		const timer = setInterval(() => {
			if (!el.isConnected || signal?.aborted) clearInterval(timer);
			else update();
		}, 30000);
		signal?.addEventListener("abort", () => clearInterval(timer), {
			once: true,
		});
		return el;
	},
	async emailReceipt(player, receipt) {
		try {
			const info = (
				await frappe.call({
					method: "sports_app.receipt_delivery.context",
					args: { name: player, receipt },
				})
			).message;
			const request_key = crypto.randomUUID();
			let sending = false,
				dialog;
			dialog = new frappe.ui.Dialog({
				title: __("Email receipt"),
				fields: [
					{
						fieldname: "recipient",
						label: __("Recipient email"),
						fieldtype: "Data",
						options: "Email",
						reqd: 1,
						default: info.recipient,
						description: __(
							"Review the recipient before sending. The posted receipt PDF will be attached."
						),
					},
				],
				primary_action_label: __("Send receipt"),
				async primary_action(values) {
					if (sending) return;
					sending = true;
					dialog.get_primary_btn().prop("disabled", true);
					try {
						await frappe.call({
							method: "sports_app.receipt_delivery.send",
							args: {
								name: player,
								receipt,
								recipient: values.recipient,
								request_key,
							},
						});
						dialog.hide();
						frappe.msgprint(
							__(
								"Receipt email queued. Delivery status is available in ERPNext Email Queue."
							)
						);
					} catch (error) {
						console.warn("Sports receipt email was not queued", error);
					} finally {
						sending = false;
						dialog.get_primary_btn().prop("disabled", false);
					}
				},
			});
			dialog.show();
		} catch (error) {
			console.warn("Could not open Sports receipt delivery", error);
		}
	},
	receiptLink(player, row, signal) {
		const wrap = document.createElement("span");
		wrap.style.cssText = "display:inline-flex;align-items:center;gap:8px";
		wrap.append(this.pdfLink("Payment Entry", row.name));
		if (row.can_email_receipt) {
			const menu = document.createElement("details"),
				toggle = document.createElement("summary"),
				item = document.createElement("button");
			toggle.textContent = "▾";
			toggle.setAttribute("aria-label", __("Receipt actions"));
			toggle.style.cursor = "pointer";
			item.type = "button";
			item.textContent = __("Email receipt");
			item.className = "btn btn-default btn-sm";
			item.style.cssText =
				"position:fixed;z-index:10000;background:var(--card-bg,#fff);box-shadow:0 5px 16px #0002;padding:10px 16px";
			item.onclick = () => {
				menu.open = false;
				this.emailReceipt(player, row.name);
			};
			menu.addEventListener("toggle", () => {
				if (menu.open) {
					const r = toggle.getBoundingClientRect();
					item.style.left = `${Math.max(8, Math.min(r.left, innerWidth - 180))}px`;
					item.style.top = `${Math.max(8, Math.min(r.bottom + 4, innerHeight - 60))}px`;
				}
			});
			menu.addEventListener("keydown", (event) => {
				if (event.key === "Escape") {
					menu.open = false;
					toggle.focus();
				}
			});
			document.addEventListener(
				"click",
				(event) => {
					if (!menu.contains(event.target)) menu.open = false;
				},
				{ signal }
			);
			menu.append(toggle, item);
			wrap.append(menu);
		}
		return wrap;
	},
};
