"use client";
import { useEffect, useRef, useState } from "react";
import { api } from "./api";
import FingerprintRegistration from "./fingerprint-registration";

export default function FingerprintEnrollments({ who, online }) {
	const [search, setSearch] = useState(""),
		[rows, setRows] = useState([]),
		[start, setStart] = useState(0),
		[more, setMore] = useState(false);
	const [selected, setSelected] = useState(null),
		[busy, setBusy] = useState(false),
		[error, setError] = useState("");
	const gate = useRef(false);
	async function fetchPlayers(offset) {
		const result = await api("biometric_preparation.list_player_statuses", {
			search,
			start: offset,
		});
		setRows(result.rows);
		setMore(result.has_more);
		setStart(offset);
	}
	async function load(offset) {
		if (gate.current || !online) return;
		gate.current = true;
		setBusy(true);
		setError("");
		try {
			await fetchPlayers(offset);
		} catch (e) {
			setError(e.message);
		} finally {
			gate.current = false;
			setBusy(false);
		}
	}
	useEffect(() => {
		load(0);
	}, []);
	return (
		<section className="card fingerprint-enrollments" aria-label="Fingerprint enrollments">
			<div className="section-heading">
				<h2>Fingerprint enrollments</h2>
				<button disabled={busy || !online} onClick={() => load(start)}>
					Refresh enrollments
				</button>
			</div>
			<p className="muted">
				Player enrollment references and latest capture status. Open a row to view consent,
				prepare registration or run demo capture. No real fingerprint scanner is connected.
			</p>
			{error && (
				<p role="alert" className="error">
					{error}
				</p>
			)}
			{!online && (
				<p className="banner">
					Reconnect to view or manage fingerprint enrollment records.
				</p>
			)}
			<form
				onSubmit={(e) => {
					e.preventDefault();
					load(0);
				}}
			>
				<label>
					Find player by name or ID
					<input
						value={search}
						maxLength={140}
						onChange={(e) => setSearch(e.target.value)}
					/>
				</label>
				<button disabled={busy || !online} type="submit">
					Find players
				</button>
			</form>
			<div className="fingerprint-table">
				<table>
					<thead>
						<tr>
							<th>Player</th>
							<th>Enrollment reference</th>
							<th>Capture status</th>
							<th>Finger</th>
							<th>Demo reference</th>
							<th>Action</th>
						</tr>
					</thead>
					<tbody>
						{rows.map((row) => (
							<tr key={row.name}>
								<td>
									<strong>{row.full_name}</strong>
									<small>{row.name}</small>
								</td>
								<td>
									{row.request_name ? (
										<button
											className="reference-link"
											disabled={busy || !online}
											onClick={() => setSelected(row)}
										>
											{row.request_name}
										</button>
									) : (
										"—"
									)}
								</td>
								<td>
									<span className="badge">
										{row.demo_reference &&
										row.fingerprint_status !== "Withdrawn"
											? "Demo captured (simulated)"
											: row.fingerprint_status}
									</span>
								</td>
								<td>{row.finger || "—"}</td>
								<td>
									<code>{row.demo_reference || "—"}</code>
								</td>
								<td>
									<button
										disabled={busy || !online}
										onClick={() => setSelected(row)}
									>
										View / prepare
									</button>
								</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
			{!rows.length && <p>{busy ? "Loading enrollments…" : "No matching players."}</p>}
			<div className="actions">
				<button
					disabled={busy || !online || start === 0}
					onClick={() => load(Math.max(0, start - 20))}
				>
					Previous players
				</button>
				<button disabled={busy || !online || !more} onClick={() => load(start + 20)}>
					Next players
				</button>
			</div>
			{selected && (
				<FingerprintRegistration
					key={selected.name}
					who={who}
					online={online}
					playerData={selected}
					onClose={() => setSelected(null)}
					onChanged={() => fetchPlayers(start)}
				/>
			)}
		</section>
	);
}
