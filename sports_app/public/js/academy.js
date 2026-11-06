(() => {
	"use strict";
	const nav = document.getElementById("navigation");
	const menu = document.querySelector(".menu-toggle");
	function closeMenu() {
		nav.classList.remove("is-open");
		menu.setAttribute("aria-expanded", "false");
		menu.setAttribute("aria-label", "Open navigation");
	}
	menu.addEventListener("click", () => {
		const open = menu.getAttribute("aria-expanded") !== "true";
		nav.classList.toggle("is-open", open);
		menu.setAttribute("aria-expanded", String(open));
		menu.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
	});
	nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
	document.addEventListener("keydown", (event) => {
		if (event.key === "Escape" && menu.getAttribute("aria-expanded") === "true") {
			closeMenu();
			menu.focus();
		}
	});
	const tabs = [...document.querySelectorAll('[role="tab"]')];
	function selectTab(tab) {
		tabs.forEach((item) => {
			const active = item === tab;
			item.setAttribute("aria-selected", String(active));
			item.tabIndex = active ? 0 : -1;
			document.getElementById(item.getAttribute("aria-controls")).hidden = !active;
		});
	}
	tabs.forEach((tab, index) => {
		tab.addEventListener("click", () => selectTab(tab));
		tab.addEventListener("keydown", (event) => {
			let next;
			if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
			else if (event.key === "ArrowLeft") next = (index + tabs.length - 1) % tabs.length;
			else if (event.key === "Home") next = 0;
			else if (event.key === "End") next = tabs.length - 1;
			else return;
			event.preventDefault();
			selectTab(tabs[next]);
			tabs[next].focus();
		});
	});
	const photos = [
		{
			src: "/assets/sports_app/images/moyours/football-1.webp",
			alt: "Young footballers competing on the academy pitch",
		},
		{
			src: "/assets/sports_app/images/moyours/football-2.webp",
			alt: "A footballer at Moyours academy",
		},
	];
	let photoIndex = 0;
	function changePhoto(direction) {
		photoIndex = (photoIndex + direction + photos.length) % photos.length;
		const image = document.getElementById("hero-image");
		image.src = photos[photoIndex].src;
		image.alt = photos[photoIndex].alt;
		document.getElementById("slide-count").textContent = `0${photoIndex + 1} / 02`;
	}
	document.getElementById("previous-photo").addEventListener("click", () => changePhoto(-1));
	document.getElementById("next-photo").addEventListener("click", () => changePhoto(1));
	const enrollment = document.getElementById("enrollment-dialog");
	const form = document.getElementById("enrollment-form");
	const result = document.getElementById("enrollment-result");
	const errorMessage = document.getElementById("enrollment-error");
	const paymentEnabled = enrollment.dataset.paymentEnabled === "1";
	let requestKey,
		submitting = false,
		retryPayload = null,
		paymentData = null,
		step = 0;
	const submit = form.querySelector('[type="submit"]');
	const showStep = (value) => {
		step = value;
		document.getElementById("enrollment-welcome").hidden = value !== 0;
		form.hidden = value !== 1;
		document.getElementById("enrollment-payment").hidden = value !== 2;
		result.hidden = value !== 3;
		enrollment.querySelectorAll("[data-step-marker]").forEach((marker) => {
			const n = Number(marker.dataset.stepMarker);
			marker.classList.toggle("is-active", n === value);
			marker.classList.toggle("is-complete", n < value);
			if (n === value) marker.setAttribute("aria-current", "step");
			else marker.removeAttribute("aria-current");
		});
		enrollment.scrollTop = 0;
	};
	function setBusy(busy) {
		submitting = busy;
		enrollment.querySelectorAll("[data-close]").forEach((button) => (button.disabled = busy));
		document.getElementById("payment-made").disabled = busy;
		submit.disabled = busy || Boolean(paymentData);
	}
	const now = new Date();
	form.elements.birth_date.max = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(
		2,
		"0"
	)}-${String(now.getDate()).padStart(2, "0")}`;
	function validateEmergencyContact() {
		const paired =
			Boolean(form.elements.emergency_contact_name.value.trim()) ===
			Boolean(form.elements.emergency_contact_phone.value.trim());
		form.elements.emergency_contact_phone.setCustomValidity(
			paired ? "" : "Enter both the emergency contact name and phone, or leave both blank."
		);
	}
	form.elements.emergency_contact_name.addEventListener("input", validateEmergencyContact);
	form.elements.emergency_contact_phone.addEventListener("input", validateEmergencyContact);
	function resetRegistration() {
		requestKey = crypto.randomUUID();
		retryPayload = null;
		paymentData = null;
		form.reset();
		form.querySelectorAll("input,select,textarea").forEach(
			(field) => (field.disabled = false)
		);
		validateEmergencyContact();
		errorMessage.hidden = true;
		document.getElementById("payment-action-error").hidden = true;
		submit.textContent = paymentEnabled ? "Make Payment ↗" : "Submit registration ↗";
		submit.disabled = false;
		document.getElementById("enrollment-return-payment").hidden = true;
		document.getElementById("enrollment-back").hidden = false;
		showStep(0);
	}
	document.getElementById("enrollment-begin").addEventListener("click", () => showStep(1));
	document.getElementById("enrollment-back").addEventListener("click", () => showStep(0));
	document.getElementById("payment-back-details").addEventListener("click", () => showStep(1));
	document
		.getElementById("enrollment-return-payment")
		.addEventListener("click", () => showStep(2));
	document.getElementById("registration-new").addEventListener("click", resetRegistration);
	document.querySelectorAll("[data-enroll]").forEach((button) =>
		button.addEventListener("click", () => {
			if (submitting) return;
			closeMenu();
			if (!requestKey) {
				resetRegistration();
				if (button.dataset.program) form.elements.program.value = button.dataset.program;
			} else if (paymentData) showStep(paymentData.state === "Draft" ? 2 : 3);
			else showStep(step);
			document.documentElement.classList.add("has-modal");
			enrollment.showModal();
		})
	);
	async function post(method, body) {
		const response = await fetch(`/api/method/sports_app.${method}`, {
			method: "POST",
			credentials: "same-origin",
			headers: {
				"Content-Type": "application/json",
				"X-Frappe-CSRF-Token": document.querySelector('meta[name="csrf-token"]').content,
			},
			body: JSON.stringify(body),
		});
		const data = await response.json();
		if (!response.ok || !data.message)
			throw new Error(response.status === 429 ? "rate" : "submit");
		return data.message;
	}
	function renderPayment(data) {
		const money = (value) =>
			new Intl.NumberFormat("en-NG", {
				style: "currency",
				currency: data.currency,
				minimumFractionDigits: 0,
				maximumFractionDigits: 2,
			}).format(value);
		for (const [id, value] of Object.entries({
			"fee-registration": money(data.registration_fee),
			"fee-jersey": money(data.jersey_fee),
			"fee-total": money(data.total),
			"fee-monthly": money(data.monthly_fee),
			"payment-bank": data.bank,
			"payment-account": data.account_number,
			"payment-beneficiary": data.account_name,
			"payment-reference": data.reference,
		}))
			document.getElementById(id).textContent = value;
		document.getElementById("payment-state").textContent = `${
			data.document_type === "Sales Invoice" ? "Invoice" : "Receipt"
		} state: ${data.state}. Your payment claim will be reviewed by Finance.`;
	}
	function renderReceipt(data) {
		const ref = document.getElementById("registration-reference");
		ref.textContent = data.reference;
		const heading = result.querySelector("h3");
		heading.textContent = paymentEnabled
			? data.settled
				? "Payment completed."
				: "Payment awaiting review."
			: "Registration received.";
		const paragraph = result.querySelector("p");
		paragraph.replaceChildren(
			document.createTextNode("Keep your reference: "),
			ref,
			document.createTextNode(
				paymentEnabled
					? data.settled
						? ". Finance has completed your payment. Admission remains subject to academy review."
						: ". You have reported a transfer. Finance will verify it before completing the invoice payment. Admission remains subject to academy review."
					: ". The academy will review your details. This confirms receipt, not acceptance."
			)
		);
		document.getElementById("final-bank-details").textContent = paymentEnabled
			? `${data.bank} · ${data.account_number} · ${data.account_name}`
			: "";
		showStep(3);
		result.querySelector("[data-close]").focus({ preventScroll: true });
	}
	form.addEventListener("submit", async (event) => {
		event.preventDefault();
		if (submitting || paymentData) return;
		const values = Object.fromEntries(new FormData(form));
		const pathway = values.program,
			website = values.website || "";
		delete values.program;
		delete values.website;
		for (const name of ["medical_consent", "media_consent", "terms_accepted"])
			values[name] = values[name] ? 1 : 0;
		const payload = JSON.stringify({ player: values, pathway, website });
		if (retryPayload && retryPayload !== payload) requestKey = crypto.randomUUID();
		retryPayload = payload;
		setBusy(true);
		errorMessage.hidden = true;
		submit.textContent = "Preparing…";
		try {
			const data = await post(
				paymentEnabled
					? "enrollment_payments.make_payment"
					: "registrations_api.submit_registration",
				{ ...JSON.parse(payload), request_key: requestKey }
			);
			if (paymentEnabled) {
				paymentData = data;
				renderPayment(data);
				form.querySelectorAll("input,select,textarea").forEach(
					(field) => (field.disabled = true)
				);
				document.getElementById("enrollment-return-payment").hidden = false;
				document.getElementById("enrollment-back").hidden = true;
				if (data.state === "Draft") showStep(2);
				else renderReceipt(data);
			} else {
				paymentData = data;
				form.reset();
				renderReceipt(data);
			}
		} catch (error) {
			errorMessage.textContent =
				error.message === "rate"
					? "Too many attempts. Please try again later or contact the academy."
					: "We couldn’t prepare your registration. Check the details and try again, or contact the academy. Retrying unchanged details will not create another invoice.";
			errorMessage.hidden = false;
			errorMessage.focus();
		} finally {
			setBusy(false);
			submit.textContent = paymentData
				? "Receipt already prepared"
				: paymentEnabled
				? "Make Payment ↗"
				: "Submit registration ↗";
		}
	});
	document.getElementById("payment-made").addEventListener("click", async () => {
		if (submitting || !paymentData) return;
		const message = document.getElementById("payment-action-error");
		message.hidden = true;
		setBusy(true);
		try {
			paymentData = await post("enrollment_payments.payment_made", {
				reference: paymentData.reference,
				request_key: requestKey,
			});
			renderReceipt(paymentData);
		} catch (error) {
			message.textContent =
				"We couldn’t request payment review. Please retry or contact the academy with your reference.";
			message.hidden = false;
		} finally {
			setBusy(false);
		}
	});
	document.querySelectorAll("[data-copy]").forEach((button) =>
		button.addEventListener("click", async () => {
			const text = document.getElementById(button.dataset.copy).textContent;
			try {
				await navigator.clipboard.writeText(text);
				document.getElementById("copy-status").textContent = "Copied.";
			} catch {
				document.getElementById("copy-status").textContent =
					"Copy is unavailable. Please select and copy the displayed value.";
			}
		})
	);
	enrollment.addEventListener("cancel", (event) => {
		if (submitting) event.preventDefault();
	});
	const lightbox = document.getElementById("photo-dialog");
	document.querySelectorAll("[data-photo]").forEach((button) =>
		button.addEventListener("click", () => {
			const photo = photos[Number(button.dataset.photo) - 1];
			const image = document.getElementById("expanded-photo");
			image.src = photo.src;
			image.alt = photo.alt;
			document.documentElement.classList.add("has-modal");
			lightbox.showModal();
		})
	);
	document.querySelectorAll("dialog").forEach((dialog) => {
		dialog.addEventListener("close", () => {
			if (!document.querySelector("dialog[open]"))
				document.documentElement.classList.remove("has-modal");
		});
		dialog
			.querySelectorAll("[data-close]")
			.forEach((button) => button.addEventListener("click", () => dialog.close()));
		dialog.addEventListener("click", (event) => {
			if (event.target !== dialog || (dialog === enrollment && submitting)) return;
			const bounds = dialog.getBoundingClientRect();
			if (
				event.clientX < bounds.left ||
				event.clientX > bounds.right ||
				event.clientY < bounds.top ||
				event.clientY > bounds.bottom
			)
				dialog.close();
		});
	});
})();
