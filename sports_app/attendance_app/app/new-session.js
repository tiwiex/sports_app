"use client";
import { useEffect, useRef, useState } from "react";
import { api } from "./api";

export default function NewSession({ who, online, onClose, onCreated }) {
	const dialog = useRef(null),
		gate = useRef(false);
	const [config, setConfig] = useState(null),
		[values, setValues] = useState(null),
		[pending, setPending] = useState(null);
	const [busy, setBusy] = useState(false),
		[error, setError] = useState("");
	const key = "sports-attendance-new-session:" + JSON.stringify([who.user, who.company]);
	useEffect(() => {
		dialog.current.showModal();
		let cancelled = false;
		(async () => {
			try {
				const settings = await api("attendance_api.configuration");
				if (settings.company !== who.company)
					throw Error("Academy changed. Refresh sign-in before creating a session.");
				const saved = JSON.parse(sessionStorage.getItem(key) || "null");
				if (cancelled) return;
				setConfig(settings);
				setPending(saved);
				setValues(
					saved?.values || {
						title: "",
						program: "",
						group: "",
						session_date: settings.today,
						start_time: "16:00",
						end_time: "18:00",
						venue: "",
					}
				);
			} catch (failure) {
				if (!cancelled) setError(failure.message);
			}
		})();
		return () => {
			cancelled = true;
		};
	}, []);
	const change = (field, value) =>
		setValues({
			...values,
			[field]: value,
			...(field === "program" ? { group: "" } : {}),
		});
	async function submit(event) {
		event.preventDefault();
		if (gate.current || !online || !config?.can_create) return;
		if (values.start_time >= values.end_time) {
			setError("End time must be after start time on the same day.");
			return;
		}
		gate.current = true;
		setBusy(true);
		setError("");
		try {
			const request = pending || {
				values: { ...values },
				request_key: crypto.randomUUID(),
			};
			sessionStorage.setItem(key, JSON.stringify(request));
			setPending(request);
			const name = await api("attendance_api.create_session", request, who);
			sessionStorage.removeItem(key);
			onCreated(name);
		} catch (failure) {
			if ([400, 417, 422].includes(failure.status) && failure.kind !== "auth") {
				sessionStorage.removeItem(key);
				setPending(null);
				setError(
					"Session validation failed. Check program/group, date and times, then retry."
				);
			} else
				setError(
					(failure.message || "Unable to create the session.") +
						" Retry the same request to recover its existing session; do not start another request."
				);
		} finally {
			gate.current = false;
			setBusy(false);
		}
	}
	return (
		<dialog
			className="new-session-dialog"
			ref={dialog}
			onCancel={(event) => {
				if (busy) event.preventDefault();
				else onClose();
			}}
			aria-labelledby="new-session-title"
		>
			<form onSubmit={submit}>
				<div className="section-heading">
					<h2 id="new-session-title">New training session</h2>
					<button
						type="button"
						disabled={busy}
						onClick={onClose}
						aria-label="Close new session"
					>
						×
					</button>
				</div>
				<p className="muted">
					Create an online session and snapshot its eligible players. Times use{" "}
					{config?.timezone || who.timezone}.
				</p>
				{error && (
					<p role="alert" className="error">
						{error}
					</p>
				)}
				{!online && <p className="banner">Reconnect before creating a session.</p>}
				{pending && (
					<p className="banner">
						Request saved in this tab. Details are locked until its outcome is
						recovered; retrying uses the same reference key.
					</p>
				)}
				{config && !config.can_create && (
					<p className="banner">
						Your account cannot create sessions and roster entries.
					</p>
				)}
				{!values ? (
					<p>Loading permitted programs…</p>
				) : (
					<fieldset disabled={busy || !!pending || !config.can_create}>
						<label>
							Session title *
							<input
								name="title"
								required
								maxLength={140}
								value={values.title}
								onChange={(e) => change("title", e.target.value)}
							/>
						</label>
						<label>
							Program *
							<select
								name="program"
								required
								value={values.program}
								onChange={(e) => change("program", e.target.value)}
							>
								<option value="">Select program</option>
								{config.programs.map((p) => (
									<option key={p.name} value={p.name}>
										{p.program_name}
									</option>
								))}
							</select>
						</label>
						<label>
							Group (optional)
							<select
								name="group"
								value={values.group}
								onChange={(e) => change("group", e.target.value)}
							>
								<option value="">All eligible players in this program</option>
								{config.groups
									.filter((g) => g.program === values.program)
									.map((g) => (
										<option key={g.name} value={g.name}>
											{g.group_name}
										</option>
									))}
							</select>
						</label>
						<label>
							Session date *
							<input
								name="session_date"
								type="date"
								required
								value={values.session_date}
								onChange={(e) => change("session_date", e.target.value)}
							/>
						</label>
						<div className="session-times">
							<label>
								Start time *
								<input
									name="start_time"
									type="time"
									required
									value={values.start_time}
									onChange={(e) => change("start_time", e.target.value)}
								/>
							</label>
							<label>
								End time *
								<input
									name="end_time"
									type="time"
									required
									value={values.end_time}
									onChange={(e) => change("end_time", e.target.value)}
								/>
							</label>
						</div>
						<label>
							Venue
							<input
								name="venue"
								maxLength={140}
								value={values.venue}
								onChange={(e) => change("venue", e.target.value)}
							/>
						</label>
					</fieldset>
				)}
				<div className="actions">
					<button type="button" disabled={busy} onClick={onClose}>
						{pending ? "Close (keep request)" : "Cancel"}
					</button>
					<button
						className="primary"
						type="submit"
						disabled={busy || !online || !values || !config?.can_create}
					>
						{busy ? "Creating…" : pending ? "Retry session request" : "Create session"}
					</button>
				</div>
			</form>
		</dialog>
	);
}
