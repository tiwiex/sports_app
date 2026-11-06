const DATABASE = "sports-attendance-v1";
const scope = (who) => JSON.stringify([who.user, who.company]);
export const rowKey = (who, session, row) => JSON.stringify([who.user, who.company, session, row]);
const database = () =>
	new Promise((resolve, reject) => {
		const request = indexedDB.open(DATABASE, 1);
		request.onupgradeneeded = () => {
			request.result.createObjectStore("state");
			request.result.createObjectStore("queue", { keyPath: "id" });
		};
		request.onsuccess = () => resolve(request.result);
		request.onerror = () => reject(request.error);
	});
async function transact(stores, mode, run) {
	const db = await database();
	return new Promise((resolve, reject) => {
		const tx = db.transaction(stores, mode);
		let result;
		tx.oncomplete = () => {
			db.close();
			resolve(result);
		};
		tx.onabort = tx.onerror = () => {
			db.close();
			reject(tx.error || Error("Device storage failed"));
		};
		run(tx, (value) => {
			result = value;
		});
	});
}
export async function lastIdentity() {
	return transact(["state"], "readonly", (tx, done) => {
		const request = tx.objectStore("state").get("last");
		request.onsuccess = () => done(request.result);
	});
}
export async function readState(who) {
	return transact(["state", "queue"], "readonly", (tx, done) => {
		const state = tx.objectStore("state").get(scope(who)),
			queue = tx.objectStore("queue").getAll();
		queue.onsuccess = () =>
			done({
				...(state.result || { sessions: [], rosters: {} }),
				queue: queue.result.filter((item) => item.scope === scope(who)),
			});
	});
}
export function saveState(who, value) {
	const { csrf_token, ...identity } = who;
	return transact(["state"], "readwrite", (tx) => {
		const state = tx.objectStore("state");
		state.put(identity, "last");
		state.put(value, scope(who));
	});
}
export function enqueue(who, session, row, status, reason, rebase = false) {
	return transact(["queue"], "readwrite", (tx) => {
		const queue = tx.objectStore("queue"),
			id = rowKey(who, session, row.name),
			request = queue.get(id);
		request.onsuccess = () => {
			const previous = request.result;
			// Keep the original server version unless staff explicitly review/rebase.
			const baseline = previous && !rebase ? previous.baseline : row;
			queue.put({
				id,
				scope: scope(who),
				session,
				name: row.name,
				player_name: row.player_name,
				status,
				reason,
				baseline,
				event_id: crypto.randomUUID(),
				captured_on: new Date().toISOString(),
			});
		};
	});
}
export function acknowledge(events) {
	return transact(["queue"], "readwrite", (tx) => {
		const queue = tx.objectStore("queue");
		for (const event of events) {
			const get = queue.get(event.id);
			get.onsuccess = () => {
				if (get.result?.event_id === event.event_id) queue.delete(event.id);
			};
		}
	});
}
export function recordFailure(events, message) {
	return transact(["queue"], "readwrite", (tx) => {
		const queue = tx.objectStore("queue");
		for (const event of events) {
			const get = queue.get(event.id);
			get.onsuccess = () => {
				if (get.result?.event_id === event.event_id)
					queue.put({ ...get.result, problem: message });
			};
		}
	});
}
export function forget(who) {
	return transact(["state", "queue"], "readwrite", (tx) => {
		const queue = tx.objectStore("queue"),
			request = queue.getAll();
		request.onsuccess = () => {
			if (request.result.some((item) => item.scope === scope(who))) {
				tx.abort();
				return;
			}
			const state = tx.objectStore("state");
			state.delete(scope(who));
			const last = state.get("last");
			last.onsuccess = () => {
				if (last.result?.user === who.user && last.result?.company === who.company)
					state.delete("last");
			};
		};
	});
}
export function minimalRoster(data) {
	const s = data.session;
	return {
		session: Object.fromEntries(
			[
				"name",
				"title",
				"company",
				"session_date",
				"start_time",
				"end_time",
				"timezone",
				"venue",
				"status",
			].map((k) => [k, s[k]])
		),
		rows: data.rows.map((row) =>
			Object.fromEntries(
				["name", "player", "player_name", "status", "modified"].map((k) => [k, row[k]])
			)
		),
		can_mark: !!data.can_mark,
		downloaded: Date.now(),
	};
}
