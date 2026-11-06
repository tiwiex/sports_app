"""Narrow, audited metadata edits for the Sports Markdown backlog."""

import fcntl
import hashlib
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo

import frappe

STATES = (
	"Proposed",
	"Backlog",
	"In analysis",
	"Ready",
	"In progress",
	"In review",
	"In UAT",
	"Done",
	"Blocked",
	"Deferred",
	"Withdrawn",
	"Retrospective",
)
PRIORITIES = ("Must", "Should", "Could", "Won't")
STORY = re.compile(r"^backlog/user-stories/us-\d{3}-\d{2}-[a-z0-9-]+\.md$")


def metadata(path, source):
	if not STORY.fullmatch(str(path)):
		return None

	def field(*names):
		for name in names:
			match = re.search(r"^- " + name + r":\s*(.+)$", source, re.M)
			if match:
				return match.group(1).strip()
		return ""

	state = field("State", "Status")
	priority = field("Priority")
	return {
		"state": state,
		"priority": priority,
		"origin": field("Origin").replace("**", "").split(" — ")[0],
		"revision": hashlib.sha256(source.encode()).hexdigest(),
		"state_options": list(STATES),
		"priority_options": list(PRIORITIES),
	}


def _header(source, names, value):
	for name in names:
		pattern = r"^- " + name + r":[^\n]*$"
		if re.search(pattern, source, re.M):
			return re.sub(pattern, lambda m: "- " + name + ": " + value, source, count=1, flags=re.M)
	# Missing metadata is inserted in the initial metadata block, before narrative.
	lines = source.splitlines(keepends=True)
	position = next((i for i, line in enumerate(lines) if line.startswith("- ")), 2)
	lines.insert(position, "- " + names[0] + ": " + value + "\n")
	return "".join(lines)


def _atomic(path, content):
	fd, name = tempfile.mkstemp(prefix=".story-", dir=path.parent)
	try:
		if path.exists():
			os.fchmod(fd, path.stat().st_mode & 0o777)
		with os.fdopen(fd, "w", encoding="utf-8") as stream:
			stream.write(content)
			stream.flush()
			os.fsync(stream.fileno())
		os.replace(name, path)
	finally:
		if os.path.exists(name):
			os.unlink(name)


def _table_update(source, sid, state, priority):
	lines = source.splitlines(keepends=True)
	headers = None
	for i, line in enumerate(lines):
		if not line.startswith("|"):
			continue
		cells = line.rstrip("\n").split("|")
		if any(cell.strip() == "Story" for cell in cells):
			headers = [cell.strip() for cell in cells]
			continue
		if not headers or not re.search(r"\[" + re.escape(sid) + r"(?:\]|:)", line):
			continue
		if len(cells) != len(headers):
			continue
		for column, value in (("State", state), ("Current state", state), ("Priority", priority)):
			if column in headers and value is not None:
				cells[headers.index(column)] = " " + value + " "
		lines[i] = "|".join(cells) + "\n"
	return "".join(lines)


def update(root, path, revision, state=None, priority=None, note=""):
	"""Called only after management authorization and allowlisted file resolution."""
	if not STORY.fullmatch(path):
		frappe.throw("Only individual Sports user stories can be updated.", frappe.PermissionError)
	if state is None and priority is None:
		frappe.throw("Choose a status or MoSCoW priority.")
	if state is not None and state not in STATES:
		frappe.throw("Select a valid story status.")
	if priority is not None and priority not in PRIORITIES:
		frappe.throw("Select a valid MoSCoW priority.")
	note = str(note or "").strip()
	if len(note) > 1000:
		frappe.throw("Keep the review note within 1,000 characters.")
	target = root / path
	# A stable lock serializes edits and derived-index updates across workers.
	lockpath = root / ".sports-story-edit.lock"
	fd = os.open(lockpath, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
	with os.fdopen(fd, "r+") as lock:
		fcntl.flock(lock, fcntl.LOCK_EX)
		if target.is_symlink() or not target.resolve().is_relative_to(root.resolve()):
			frappe.throw("Invalid story path.", frappe.PermissionError)
		source = target.read_text(encoding="utf-8")
		before = metadata(path, source)
		if not revision or revision != before["revision"]:
			frappe.throw("This story changed. Reopen it before saving your edit.")
		nextstate = state if state is not None else before["state"]
		nextpriority = priority if priority is not None else before["priority"]
		if nextstate == before["state"] and nextpriority == before["priority"]:
			return before
		changed = source
		if state is not None:
			changed = _header(changed, ("State", "Status"), state)
		if priority is not None:
			changed = _header(changed, ("Priority",), priority)
		sid = re.search(r"us-\d{3}-\d{2}", path).group().upper()
		epic = "EPIC-" + sid.split("-")[1]
		now = datetime.now(ZoneInfo("Africa/Lagos"))
		stamp = now.strftime("%Y-%m-%d")
		token = uuid4().hex[:12]
		relative = f"build-logs/{stamp}-{sid.lower()}-review-{token}.md"
		logpath = root / relative

		# Plain-text audit values cannot inject additional Markdown structure.
		def clean(value):
			return (
				str(value or "Not set")
				.replace("\n", " ")
				.replace("\r", " ")
				.replace("|", "/")
				.replace("`", "'")
			)

		audit = f"""# Story review: {sid}

- Date: {now.isoformat()} (Africa/Lagos)
- Story: [{sid}](../{path})
- Actor: {clean(frappe.session.user)}
- Status: {clean(before['state'])} → {clean(nextstate)}
- MoSCoW: {clean(before['priority'])} → {clean(nextpriority)}
- Review note: {clean(note or 'Metadata updated from Sports Development Tools.')}

## Outcome and evidence

An authorized reviewer changed backlog metadata. This audit records the reviewer action; it does not execute tests, implement features, verify hardware or certify acceptance criteria. Existing story acceptance/build evidence remains authoritative. Source/provenance and narrative were preserved; epic/backlog rows were synchronized. No business-data, role or schema changes.
"""
		changed += f"\nReview tracking: [{stamp} status / MoSCoW update](../../{relative}).\n"
		writes = {target: changed, logpath: audit}
		for p in [root / "backlog/README.md", *sorted((root / "backlog/epics").glob(epic + "-*.md"))]:
			if p.exists():
				writes[p] = _table_update(p.read_text(encoding="utf-8"), sid, state, priority)
		# The consolidated snapshot is derived from story headers, including this edit.
		overview = root / "backlog/README.md"
		if overview in writes and "## Delivery-state snapshot" in writes[overview]:
			from collections import Counter

			counts = Counter()
			for p in (root / "backlog/user-stories").glob("us-*.md"):
				data = metadata(
					p.relative_to(root).as_posix(), changed if p == target else p.read_text(encoding="utf-8")
				)
				counts[(data or {}).get("state") or "Not recorded"] += 1
			snapshot = (
				"## Delivery-state snapshot\n\n"
				+ "\n".join(f"- {key}: {value}" for key, value in sorted(counts.items()))
				+ "\n\n"
			)
			writes[overview] = re.sub(
				r"## Delivery-state snapshot\n[\s\S]*?(?=\[Consolidation build log\]|\Z)",
				lambda m: snapshot,
				writes[overview],
			)
		index = root / "build-logs/index.md"
		old = index.read_text(encoding="utf-8")
		row = f"| {stamp} | [{sid} review metadata]({logpath.name}) | Reviewer update / audited |\n"
		writes[index] = old.replace("|---|---|---|\n", "|---|---|---|\n" + row, 1)
		backups = {}
		for p in writes:
			if p.is_symlink() or not p.resolve().is_relative_to(root.resolve()):
				frappe.throw("Invalid documentation target.", frappe.PermissionError)
			backups[p] = p.read_text(encoding="utf-8") if p.exists() else None
		try:
			for p, content in writes.items():
				_atomic(p, content)
		except Exception:
			for p, content in backups.items():
				if content is None:
					p.unlink(missing_ok=True)
				else:
					_atomic(p, content)
			raise
		result = metadata(path, changed)
		result["audit_path"] = relative
		return result
