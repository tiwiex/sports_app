"use client";
import { useEffect, useRef, useState } from "react";
import { api } from "./api";
import NewSession from "./new-session";
import FingerprintEnrollments from "./fingerprint-enrollments";
import {
	lastIdentity,
	readState,
	saveState,
	enqueue,
	acknowledge,
	recordFailure,
	forget,
	minimalRoster,
} from "./store";

const ROOT = "/assets/sports_app/attendance/",
	STATUSES = ["Present", "Late", "Absent", "Excused"];
const login = "/login?redirect-to=" + encodeURIComponent("/sports-attendance");
const fresh = (who) => who?.verified && Date.now() - who.verified < 7 * 86400000;
const day = (timezone) =>
	new Intl.DateTimeFormat("en-CA", {
		timeZone: timezone,
		year: "numeric",
		month: "2-digit",
		day: "2-digit",
	}).format(new Date());

export default function Attendance() {
	const [who, setWho] = useState(null),
		[online, setOnline] = useState(true),
		[loading, setLoading] = useState(true);
	const [state, setState] = useState({ sessions: [], rosters: {}, queue: [] }),
		[trusted, setTrusted] = useState(false);
	const [selected, setSelected] = useState(""),
		[search, setSearch] = useState(""),
		[filter, setFilter] = useState("");
	const [message, setMessage] = useState(""),
		[error, setError] = useState(""),
		[busy, setBusy] = useState(false),
		[conflicts, setConflicts] = useState({}),
		[reasons, setReasons] = useState({}),
		[choices, setChoices] = useState({});
	const [hasMore, setHasMore] = useState(false),
		[start, setStart] = useState(0),
		[install, setInstall] = useState(null);
	const [creating, setCreating] = useState(false);
	const [fingerprint, setFingerprint] = useState(false);
	const gate = useRef(false),
		identity = useRef(null),
		snapshot = useRef(state);
	function showState(next) {
		snapshot.current = next;
		setState(next);
	}
	async function reloadLocal(user = who) {
		const saved = await readState(user);
		showState(saved);
		return saved;
	}
	async function persist(next, user = who) {
		await saveState(user, { sessions: next.sessions, rosters: next.rosters });
		showState(next);
	}
	async function connect() {
		setLoading(true);
		setError("");
		try {
			if (!navigator.onLine) {
				const cached = await lastIdentity();
				if (!fresh(cached))
					throw Error(
						"Connect and sign in to prepare this device for offline attendance."
					);
				identity.current = cached;
				setWho(cached);
				setTrusted(true);
				await reloadLocal(cached);
				setMessage(
					"Offline device mode. Identity and permissions were last verified online; reconnect before syncing."
				);
				return;
			}
			const current = await api("attendance_mobile_api.bootstrap");
			if (!current.authenticated) {
				identity.current = null;
				setWho(null);
				showState({ sessions: [], rosters: {}, queue: [] });
				return;
			}
			current.verified = Date.now();
			identity.current = current;
			setWho(current);
			const saved = await readState(current),
				previous = await lastIdentity();
			setTrusted(previous?.user === current.user && previous?.company === current.company);
			showState(saved);
			const result = await api("attendance_api.list_sessions", {
				status: "",
				start: 0,
			});
			const next = { ...saved, sessions: result.rows };
			showState(next);
			setHasMore(result.has_more);
			setStart(0);
			if (previous?.user === current.user && previous?.company === current.company)
				await persist(next, current);
		} catch (failure) {
			setError(failure.message);
			if (navigator.onLine) {
				identity.current = null;
				setWho(null);
				showState({ sessions: [], rosters: {}, queue: [] });
			}
		} finally {
			setLoading(false);
		}
	}
	useEffect(() => {
		setOnline(navigator.onLine);
		connect();
		const network = () => setOnline(navigator.onLine),
			prompt = (e) => {
				e.preventDefault();
				setInstall(e);
			};
		const changed = () => {
			const current = identity.current;
			if (current)
				readState(current)
					.then(showState)
					.catch(() => {});
		};
		window.addEventListener("online", network);
		window.addEventListener("offline", network);
		window.addEventListener("focus", changed);
		window.addEventListener("beforeinstallprompt", prompt);
		if ("serviceWorker" in navigator)
			navigator.serviceWorker
				.register(ROOT + "sw.js", { scope: ROOT, updateViaCache: "none" })
				.catch(() => {});
		return () => {
			window.removeEventListener("online", network);
			window.removeEventListener("offline", network);
			window.removeEventListener("focus", changed);
			window.removeEventListener("beforeinstallprompt", prompt);
		};
	}, []);
	async function run(action) {
		if (gate.current) return;
		gate.current = true;
		setBusy(true);
		setError("");
		try {
			await action();
		} catch (e) {
			setError(e.message || "Device storage is unavailable. No mark was recorded.");
		} finally {
			gate.current = false;
			setBusy(false);
		}
	}
	async function trust() {
		await run(async () => {
			await persist(snapshot.current);
			setTrusted(true);
			setMessage(
				"Device enabled. Download a session roster before going offline. Use this only on a trusted staff device."
			);
		});
	}
	async function pageSessions(offset) {
		await run(async () => {
			const result = await api("attendance_api.list_sessions", {
				start: offset,
			});
			const next = { ...snapshot.current, sessions: result.rows };
			if (trusted) await persist(next);
			else showState(next);
			setStart(offset);
			setHasMore(result.has_more);
		});
	}
	async function created(name) {
		setCreating(false);
		await pageSessions(0);
		if (trusted) await open(name);
		else
			setMessage(
				`Session ${name} created. Enable this trusted device to download its roster.`
			);
	}
	async function open(name) {
		await run(async () => {
			if (!trusted)
				throw Error("Enable this trusted device before downloading private rosters.");
			if (online) {
				const result = minimalRoster(await api("attendance_api.roster", { name }));
				if (result.session.company !== who.company)
					throw Error("This session belongs to another academy.");
				await persist({
					...snapshot.current,
					rosters: { ...snapshot.current.rosters, [name]: result },
				});
			}
			if (!snapshot.current.rosters[name])
				throw Error("This roster has not been downloaded. Reconnect to download it.");
			setSelected(name);
			setSearch("");
			setFilter("");
			setMessage(
				online
					? "Roster downloaded. Marks save to this device; choose Sync now to send them."
					: "Using downloaded roster. Changes will stay pending until you sync online."
			);
		});
	}
	const roster = state.rosters[selected],
		pending = state.queue.filter((event) => event.session === selected);
	const writable = !!(
		roster?.can_mark &&
		roster.session.status !== "Cancelled" &&
		roster.session.session_date <= day(roster.session.timezone) &&
		(online || fresh(who))
	);
	async function mark(row, status, rebase = false) {
		await run(async () => {
			const current = state.queue.find(
				(event) => event.name === row.name && event.session === selected
			);
			if (!writable)
				throw Error(
					"This session is read-only. Refresh online to check permissions and dates."
				);
			const baseline = current && !rebase ? current.baseline : row;
			const reason = (reasons[row.name] ?? current?.reason ?? "").trim();
			if ((baseline.status !== "Unmarked" || rebase) && !reason)
				throw Error(
					"Enter a correction/review reason before changing recorded attendance."
				);
			await enqueue(who, selected, row, status, reason, rebase);
			await reloadLocal();
			setConflicts((old) => {
				const copy = { ...old };
				delete copy[row.name];
				return copy;
			});
			setMessage("Saved on this device. Pending synchronization.");
		});
	}
	async function useServer(event) {
		await run(async () => {
			await acknowledge([event]);
			await reloadLocal();
			setConflicts((old) => {
				const copy = { ...old };
				delete copy[event.name];
				return copy;
			});
			setMessage(
				"Local choice discarded for this player. The displayed server status is retained."
			);
		});
	}
	async function sync() {
		await run(async () => {
			if (!online)
				throw Error("Reconnect before syncing. Your marks remain on this device.");
			const perform = async () => {
				const queued = (await reloadLocal()).queue;
				if (!queued.length) {
					setMessage("Nothing pending on this device.");
					return;
				}
				let completed = 0;
				for (const name of [...new Set(queued.map((item) => item.session))]) {
					const events = queued.filter((item) => item.session === name);
					for (let i = 0; i < events.length; i += 1000) {
						const batch = events.slice(i, i + 1000);
						try {
							const result = minimalRoster(
								await api(
									"attendance_api.save_attendance",
									{
										name,
										marks: batch.map((item) => ({
											name: item.name,
											status: item.status,
											modified: item.baseline.modified,
											reason: item.reason,
										})),
									},
									who
								)
							);
							await acknowledge(batch);
							const saved = await readState(who);
							await persist({
								...saved,
								rosters: { ...saved.rosters, [name]: result },
							});
							completed += batch.length;
							setConflicts((old) => {
								const copy = { ...old };
								for (const item of batch) delete copy[item.name];
								return copy;
							});
						} catch (failure) {
							// Refresh for review; retain every queued intent on any uncertain failure.
							await recordFailure(batch, failure.message);
							if (failure.kind !== "auth")
								try {
									const latest = minimalRoster(
										await api("attendance_api.roster", { name })
									);
									const saved = await readState(who);
									await persist({
										...saved,
										rosters: { ...saved.rosters, [name]: latest },
									});
								} catch {
									/* Keep the form usable if tab storage is unavailable. */
								}
							setSelected(name);
							setConflicts((old) => ({
								...old,
								...Object.fromEntries(
									batch.map((item) => [item.name, failure.message])
								),
							}));
							throw failure;
						}
					}
				}
				await reloadLocal();
				setMessage(
					`${completed} attendance mark${
						completed === 1 ? "" : "s"
					} synchronized. Server audit time is the sync time.`
				);
			};
			if (navigator.locks)
				await navigator.locks.request(
					"sports-attendance-sync",
					{ ifAvailable: true },
					async (lock) => {
						if (!lock) throw Error("Another tab is syncing. Please wait.");
						await perform();
					}
				);
			else await perform();
		});
	}
	async function forgetDevice() {
		await run(async () => {
			if (state.queue.length)
				throw Error(
					"Sync or explicitly resolve pending marks before forgetting this device."
				);
			if (!window.confirm("Remove this account’s downloaded rosters from this browser?"))
				return;
			await forget(who);
			setTrusted(false);
			showState({ sessions: state.sessions, rosters: {}, queue: [] });
			setSelected("");
			setMessage("Downloaded attendance data removed from this device.");
		});
	}
	const matching =
		roster?.rows.filter((row) => {
			const event = pending.find((item) => item.name === row.name),
				status = event?.status || row.status;
			return (
				`${row.player} ${row.player_name}`.toLowerCase().includes(search.toLowerCase()) &&
				(!filter || (filter === "Pending" ? !!event : status === filter))
			);
		}) || [];
	const count = (status) =>
		roster?.rows.filter(
			(row) => (pending.find((e) => e.name === row.name)?.status || row.status) === status
		).length || 0;
	return (
		<div className="attendance-shell">
			<header className="topbar">
				<a href="/sports-attendance">
					SPORTS <span>/</span> ATTENDANCE
				</a>
				<div className={online ? "connection" : "connection offline"}>
					{online ? "● Online" : "● Offline"}
				</div>
			</header>
			<main>
				<div className="heading">
					<div>
						<span className="eyebrow">EVERY SESSION COUNTS</span>
						<h1>{who?.academy_name || "Training attendance"}</h1>
						<p className="muted">
							{who
								? `${who.user} · ${who.company}`
								: "Sign in with your academy staff account."}
						</p>
					</div>
					{who && (
						<div className="actions">
							<button disabled={busy || !online} onClick={connect}>
								Refresh sign-in
							</button>
							<a className="button" href="/app/boost-console">
								Staff console ↗
							</a>
						</div>
					)}
				</div>
				{error && (
					<p role="alert" className="error">
						{error}
					</p>
				)}
				{message && (
					<p role="status" className="banner">
						{message}
					</p>
				)}
				{!online && (
					<p className="banner">
						Offline · downloaded rosters only. Device marks are not server records
						until synchronized.
					</p>
				)}
				{loading ? (
					<p>Checking staff access…</p>
				) : !who ? (
					<section className="card">
						<h2>Staff access</h2>
						<p>
							Sports Registrar, Sports Academy Administrator or System Manager access
							is required, subject to Company and document permissions.
						</p>
						<a className="button primary" href={login}>
							Sign in to attendance →
						</a>
						<button onClick={connect}>Retry connection</button>
					</section>
				) : (
					<>
						{who.can_prepare_biometrics && (
							<nav className="actions" aria-label="Attendance app sections">
								<button
									aria-pressed={!fingerprint}
									disabled={busy}
									onClick={() => setFingerprint(false)}
								>
									Training sessions
								</button>
								<button
									aria-pressed={fingerprint}
									disabled={busy || !online}
									onClick={() => setFingerprint(true)}
								>
									Fingerprint enrollments
								</button>
							</nav>
						)}
						{fingerprint && who.can_prepare_biometrics ? (
							<FingerprintEnrollments who={who} online={online} />
						) : (
							<>
								{!trusted && (
									<section className="card device">
										<h2>Prepare a trusted staff device</h2>
										<p>
											Downloaded rosters contain player names, IDs and
											attendance. Local data is accessible to others using
											this browser and is not encrypted by this app. Enable
											only on a trusted device. Offline identity is valid for
											seven days after verification; pending marks are
											retained until resolved.
										</p>
										<button
											className="primary"
											disabled={busy || !online}
											onClick={trust}
										>
											Enable offline attendance on this device
										</button>
									</section>
								)}
								<div className="actions">
									<button
										className="primary"
										disabled={busy || !online}
										onClick={() => setCreating(true)}
									>
										New session
									</button>
									<small>
										Create sessions online; finalize or cancel in the staff
										console.
									</small>
								</div>
								{creating && (
									<NewSession
										who={who}
										online={online}
										onClose={() => setCreating(false)}
										onCreated={created}
									/>
								)}
								<section className="syncbar">
									<div>
										<strong>{state.queue.length}</strong> pending on this
										device{" "}
										<small>Saved locally, awaiting server acceptance</small>
									</div>
									<div className="actions">
										<button
											className="primary"
											disabled={busy || !online || !state.queue.length}
											onClick={sync}
										>
											{busy ? "Working…" : "Sync now"}
										</button>
										<button
											disabled={busy || !trusted || !!state.queue.length}
											onClick={forgetDevice}
										>
											Forget this device
										</button>
										{install && (
											<button
												onClick={async () => {
													await install.prompt();
													setInstall(null);
												}}
											>
												Install app
											</button>
										)}
									</div>
								</section>
								{!selected ? (
									<section className="card">
										<div className="section-heading">
											<h2>Training sessions</h2>
											<span className="muted">
												Create sessions here; finalize in the staff console
											</span>
										</div>
										<div className="session-grid">
											{(online
												? state.sessions
												: Object.values(state.rosters).map(
														(data) => data.session
												  )
											).map((session) => (
												<button
													className="session"
													key={session.name}
													disabled={busy || !trusted}
													onClick={() => open(session.name)}
												>
													<span className="eyebrow">
														{session.session_date} ·{" "}
														{String(session.start_time || "").slice(
															0,
															5
														)}
													</span>
													<strong>{session.title}</strong>
													<span>
														{session.program_label ||
															session.venue ||
															session.name}
													</span>
													<span className="session-bottom">
														<span className="badge">
															{session.status}
														</span>
														<span>
															{state.rosters[session.name]
																? "Downloaded"
																: "Download roster"}{" "}
															→
														</span>
													</span>
												</button>
											))}
										</div>
										{!(online
											? state.sessions.length
											: Object.keys(state.rosters).length) && (
											<p className="muted">
												{online
													? "No sessions yet. Choose New session to generate an eligible player roster."
													: "No downloaded rosters. Reconnect to download a session."}
											</p>
										)}
										{online && (
											<div className="actions">
												<button
													disabled={busy || start === 0}
													onClick={() =>
														pageSessions(Math.max(0, start - 20))
													}
												>
													Previous
												</button>
												<button
													disabled={busy || !hasMore}
													onClick={() => pageSessions(start + 20)}
												>
													Next
												</button>
											</div>
										)}
									</section>
								) : (
									roster && (
										<>
											<button
												className="back"
												disabled={busy}
												onClick={() => setSelected("")}
											>
												← All sessions
											</button>
											<section className="card roster">
												<div className="section-heading">
													<div>
														<span className="eyebrow">
															{roster.session.name} ·{" "}
															{roster.session.status}
														</span>
														<h2>{roster.session.title}</h2>
														<p className="muted">
															{roster.session.session_date} ·{" "}
															{roster.session.timezone} ·{" "}
															{roster.session.venue ||
																"Academy training"}
														</p>
														<small>
															Downloaded{" "}
															{new Date(
																roster.downloaded
															).toLocaleString()}
														</small>
													</div>
													<button
														disabled={busy || !online}
														onClick={() => open(selected)}
													>
														Refresh roster
													</button>
												</div>
												{!writable && (
													<p className="banner">
														Read-only: session is future-dated,
														cancelled, or your account lacks marking
														permission. Cached permission is checked
														again by the server on sync.
													</p>
												)}
												<div className="stats">
													{["Unmarked", ...STATUSES].map((status) => (
														<div key={status}>
															<strong>{count(status)}</strong>
															<span>{status}</span>
														</div>
													))}
												</div>
												<div className="filters">
													<label>
														Find player
														<input
															placeholder="Name or player ID"
															value={search}
															onChange={(e) =>
																setSearch(e.target.value)
															}
														/>
													</label>
													<label>
														Show
														<select
															value={filter}
															onChange={(e) =>
																setFilter(e.target.value)
															}
														>
															<option value="">All statuses</option>
															{[
																"Pending",
																"Unmarked",
																...STATUSES,
															].map((status) => (
																<option key={status}>
																	{status}
																</option>
															))}
														</select>
													</label>
												</div>
												<div className="player-list">
													{matching.map((row) => {
														const event = pending.find(
																(item) => item.name === row.name
															),
															current = event?.status || row.status,
															conflict =
																conflicts[row.name] ||
																event?.problem;
														return (
															<article
																className={
																	event
																		? "player-card pending"
																		: "player-card"
																}
																key={row.name}
															>
																<div className="player-top">
																	<div>
																		<h3>{row.player_name}</h3>
																		<small>{row.player}</small>
																	</div>
																	<span
																		className={`badge status-${current.toLowerCase()}`}
																	>
																		{current}
																		{event
																			? " · Pending sync"
																			: ""}
																	</span>
																</div>
																<div
																	className="mark-buttons"
																	role="group"
																	aria-label={`Attendance for ${row.player_name}`}
																>
																	{STATUSES.map((status) => (
																		<button
																			key={status}
																			disabled={
																				busy ||
																				!writable ||
																				!!conflict
																			}
																			aria-pressed={
																				current === status
																			}
																			onClick={() =>
																				mark(row, status)
																			}
																		>
																			{status}
																		</button>
																	))}
																</div>
																<label className="reason">
																	Correction / review reason
																	<input
																		maxLength={1000}
																		placeholder="Required when correcting a recorded mark"
																		value={
																			reasons[row.name] ??
																			event?.reason ??
																			""
																		}
																		onChange={(e) =>
																			setReasons({
																				...reasons,
																				[row.name]:
																					e.target.value,
																			})
																		}
																	/>
																</label>
																{event && (
																	<small>
																		Captured on device:{" "}
																		{new Date(
																			event.captured_on
																		).toLocaleString()}{" "}
																		· Server: {row.status}
																	</small>
																)}
																{conflict && event && (
																	<div className="conflict">
																		<strong>
																			Needs review
																		</strong>
																		<p>{conflict}</p>
																		<p>
																			Your choice:{" "}
																			{event.status}. Latest
																			downloaded server
																			status: {row.status}.
																		</p>
																		<div className="actions">
																			<button
																				disabled={busy}
																				onClick={() =>
																					useServer(
																						event
																					)
																				}
																			>
																				Use server status
																			</button>
																			<select
																				aria-label={`Reviewed status for ${row.player_name}`}
																				value={
																					choices[
																						row.name
																					] ||
																					event.status
																				}
																				onChange={(e) =>
																					setChoices({
																						...choices,
																						[row.name]:
																							e
																								.target
																								.value,
																					})
																				}
																			>
																				{STATUSES.map(
																					(status) => (
																						<option
																							key={
																								status
																							}
																						>
																							{
																								status
																							}
																						</option>
																					)
																				)}
																			</select>
																			<button
																				disabled={
																					busy ||
																					!writable ||
																					!online
																				}
																				onClick={() =>
																					mark(
																						row,
																						choices[
																							row
																								.name
																						] ||
																							event.status,
																						true
																					)
																				}
																			>
																				Queue reviewed
																				correction
																			</button>
																		</div>
																	</div>
																)}
															</article>
														);
													})}
												</div>
												{!matching.length && (
													<p className="muted">
														No players match this filter.
													</p>
												)}
											</section>
										</>
									)
								)}
							</>
						)}
					</>
				)}
			</main>
			<footer>
				Sports attendance · Development prototype{" "}
				<span>Manual marking · Biometrics not connected</span>
			</footer>
		</div>
	);
}
