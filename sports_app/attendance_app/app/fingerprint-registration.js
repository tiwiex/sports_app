"use client";
import { useEffect, useRef, useState } from "react";
import { api } from "./api";
import DemoBarcode from "./demo-barcode";
import DemoFingerprint from "./demo-fingerprint";

export default function FingerprintRegistration({ who, online, onClose, playerData, onChanged }) {
	const dialog = useRef(null),
		gate = useRef(false),
		key = useRef(crypto.randomUUID());
	const player = playerData.name,
		selectedLabel = playerData.full_name;
	const [scanning, setScanning] = useState(false);
	const [records, setRecords] = useState([]),
		[error, setError] = useState(""),
		[busy, setBusy] = useState(false),
		[locked, setLocked] = useState(false);
	const [values, setValues] = useState({
		finger: "Right thumb",
		consent_by: "",
		relationship: "Parent / Guardian",
		notice_reference: "",
		consent_date: who.today || new Date().toISOString().slice(0, 10),
	});
	const [confirmed, setConfirmed] = useState(false),
		[reason, setReason] = useState("");
	useEffect(() => {
		dialog.current.showModal();
		run(() => load(player));
	}, []);
	async function run(action) {
		if (gate.current || !online) return;
		gate.current = true;
		setBusy(true);
		setError("");
		try {
			await action();
		} catch (e) {
			setError(e.message);
		} finally {
			gate.current = false;
			setBusy(false);
		}
	}
	async function load(name) {
		setRecords(await api("biometric_preparation.records", { player: name }));
		await onChanged();
	}
	async function prepare(event) {
		event.preventDefault();
		if (!confirmed) return;
		await run(async () => {
			setLocked(true);
			try {
				await api(
					"biometric_preparation.prepare",
					{ player, values, consent_confirmed: 1, request_key: key.current },
					who
				);
				await load(player);
				setLocked(false);
				setConfirmed(false);
				key.current = crypto.randomUUID();
			} catch (e) {
				if ([400, 417, 422].includes(e.status)) {
					setLocked(false);
					key.current = crypto.randomUUID();
				}
				await load(player);
				throw e;
			}
		});
	}
	const pending = records.find((r) => r.status === "Pending capture");
	async function demoCapture() {
		await run(async () => {
			setScanning(true);
			try {
				const duration = window.matchMedia("(prefers-reduced-motion: reduce)").matches
					? 0
					: 1100;
				await Promise.all([
					api("biometric_preparation.demo_capture", { name: pending.name }, who),
					new Promise((resolve) => setTimeout(resolve, duration)),
				]);
				await load(player);
			} finally {
				setScanning(false);
			}
		});
	}
	const change = (field, value) => setValues({ ...values, [field]: value });
	return (
		<dialog
			ref={dialog}
			className="new-session-dialog"
			onCancel={(e) => {
				if (busy) e.preventDefault();
				else onClose();
			}}
			aria-labelledby="fingerprint-title"
		>
			<div className="section-heading">
				<h2 id="fingerprint-title">Fingerprint registration</h2>
				<button
					disabled={busy}
					onClick={onClose}
					aria-label="Close fingerprint registration"
				>
					×
				</button>
			</div>
			<p className="banner">
				Scanner not connected. Prepare a request or generate a clearly labelled demo
				barcode. No fingerprint is scanned, stored or verified, and this does not enable
				biometric attendance.
			</p>
			{!online && (
				<p className="error">
					Connect before preparing or withdrawing fingerprint registration.
				</p>
			)}
			{error && (
				<p className="error" role="alert">
					{error}
				</p>
			)}
			<button type="button" disabled={busy} onClick={onClose}>
				← Back to fingerprint enrollments
			</button>
			{player && (
				<>
					<h3>
						Selected player: {selectedLabel} · {player}
					</h3>
					<section>
						<h3>Capture requests</h3>
						{!records.length && <p className="muted">No preparation recorded.</p>}
						{records.map((r) => (
							<div className="fingerprint-record" key={r.name}>
								<strong>
									{r.name} · {r.status}
								</strong>
								<p>
									{r.finger} · Consent supplied by {r.consent_by} (
									{r.relationship}) · {String(r.consent_date).slice(0, 10)}
								</p>
								<small>Notice/reference: {r.notice_reference}</small>
								{r.demo_reference &&
									(r.status === "Withdrawn" ? (
										<p>Withdrawn demo code: {r.demo_reference}</p>
									) : (
										<DemoBarcode reference={r.demo_reference} />
									))}
								{r.withdrawal_reason && <p>Withdrawn: {r.withdrawal_reason}</p>}
							</div>
						))}
					</section>
					{pending ? (
						<section>
							{!pending.demo_reference && (
								<DemoFingerprint phase={scanning ? "scanning" : "ready"} />
							)}
							<button
								className="primary"
								disabled={busy || !online || !!pending.demo_reference}
								onClick={demoCapture}
							>
								{scanning
									? "Simulating scan…"
									: pending.demo_reference
									? "Demo capture complete (simulated)"
									: "Demo capture — generate barcode"}
							</button>
							<p className="muted">
								Real fingerprint capture remains pending. The generated demo code
								cannot mark attendance.
							</p>
							<label>
								Withdrawal reason
								<input
									maxLength={1000}
									value={reason}
									onChange={(e) => setReason(e.target.value)}
								/>
							</label>
							<button
								disabled={busy || !online || !reason.trim()}
								onClick={() =>
									run(async () => {
										await api(
											"biometric_preparation.withdraw",
											{ name: pending.name, reason },
											who
										);
										await load(player);
										setLocked(false);
										setReason("");
										setConfirmed(false);
										key.current = crypto.randomUUID();
									})
								}
							>
								Withdraw pending request
							</button>
						</section>
					) : (
						<form onSubmit={prepare}>
							<fieldset disabled={busy || locked || !online}>
								<label>
									Finger to capture
									<select
										value={values.finger}
										onChange={(e) => change("finger", e.target.value)}
									>
										{[
											"Right thumb",
											"Left thumb",
											"Right index",
											"Left index",
										].map((f) => (
											<option key={f}>{f}</option>
										))}
									</select>
								</label>
								<label>
									Consent supplied by
									<input
										required
										maxLength={140}
										value={values.consent_by}
										onChange={(e) => change("consent_by", e.target.value)}
									/>
								</label>
								<label>
									Relationship
									<select
										value={values.relationship}
										onChange={(e) => change("relationship", e.target.value)}
									>
										<option>Parent / Guardian</option>
										<option>Player</option>
									</select>
								</label>
								<label>
									Consent notice/reference
									<input
										required
										maxLength={140}
										placeholder="Reference to the actual supplied biometric consent"
										value={values.notice_reference}
										onChange={(e) =>
											change("notice_reference", e.target.value)
										}
									/>
								</label>
								<label>
									Consent date
									<input
										type="date"
										required
										value={values.consent_date}
										onChange={(e) => change("consent_date", e.target.value)}
									/>
								</label>
								<label className="consent-check">
									<input
										type="checkbox"
										checked={confirmed}
										onChange={(e) => setConfirmed(e.target.checked)}
									/>
									I confirm this biometric consent was actually supplied. This
									records preparation only.
								</label>
							</fieldset>
							<button
								type="submit"
								className="primary"
								disabled={busy || !online || !confirmed}
							>
								{busy
									? "Saving…"
									: locked
									? "Retry preparation"
									: "Prepare capture request"}
							</button>
						</form>
					)}
				</>
			)}
		</dialog>
	);
}
