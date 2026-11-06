"""Protected Sports documentation with narrow audited story metadata controls."""
from pathlib import Path, PurePosixPath
from html import escape
import base64
import frappe
from frappe import _
from frappe.utils.html_utils import sanitize_html
from sports_app.academy import require_settings_access


def _root():
 return (Path(frappe.get_app_path("sports_app")) / "doc-sports").resolve()


def _file(path, extensions):
 text = str(path or "")
 relative = PurePosixPath(text)
 if not text or "\x00" in text or "\\" in text or relative.is_absolute() or ".." in relative.parts:
  frappe.throw(_("Invalid documentation path."), frappe.PermissionError)
 root = _root()
 target = (root / text).resolve()
 if not target.is_relative_to(root) or target.suffix.lower() not in extensions:
  frappe.throw(_("Only Sports documentation can be opened."), frappe.PermissionError)
 if not target.is_file():
  frappe.throw(_("Documentation file not found."), frappe.DoesNotExistError)
 return target


def _category(path):
 if path in ("REQUIREMENTS.md", "concepts/requirement-baseline.md", "requirements.txt"):
  return "Requirements"
 for prefix, label in (("backlog/user-stories/", "User Stories"), ("backlog/epics/", "Epics"),
  ("build-logs/", "Build Logs"), ("adr/", "Architecture Decisions")):
  if path.startswith(prefix): return label
 return "Guides and Product"


@frappe.whitelist()
def get_documents():
 require_settings_access()
 root = _root()
 rows = []
 for path in sorted(root.rglob("*")):
  if path.suffix.lower() not in (".md", ".txt") or not path.is_file(): continue
  relative = path.relative_to(root).as_posix()
  if not path.resolve().is_relative_to(root) or path.stat().st_size > 512 * 1024: continue
  source = path.read_text(encoding="utf-8")
  title = next((line[2:].strip() for line in source.splitlines() if line.startswith("# ")), path.name)
  from sports_app.story_tracking import metadata
  rows.append({"path": relative, "title": title, "category": _category(relative), "story": metadata(relative, source)})
 return {"documents": rows, "default_document": "REQUIREMENTS.md"}


@frappe.whitelist()
def get_document(path):
 require_settings_access()
 target = _file(path, {".md", ".txt"})
 if target.stat().st_size > 512 * 1024: frappe.throw(_("Documentation file is too large."))
 source = target.read_text(encoding="utf-8")
 html = "<pre>" + escape(source) + "</pre>" if target.suffix.lower() == ".txt" else frappe.utils.md_to_html(source) or ""
 from sports_app.story_tracking import metadata
 relative = target.relative_to(_root()).as_posix()
 return {"path": relative, "html": sanitize_html(html, always_sanitize=True), "story": metadata(relative, source)}


@frappe.whitelist()
def get_asset(path):
 require_settings_access()
 target = _file(path, {".png", ".jpg", ".jpeg"})
 if target.stat().st_size > 2 * 1024 * 1024: frappe.throw(_("Documentation image is too large."))
 mime = "image/png" if target.suffix.lower() == ".png" else "image/jpeg"
 return {"data_url": "data:" + mime + ";base64," + base64.b64encode(target.read_bytes()).decode("ascii")}


@frappe.whitelist(methods=["POST"])
def update_story(path, revision, state=None, priority=None, note=""):
 require_settings_access()
 target = _file(path, {".md"})
 from sports_app.story_tracking import update
 return update(_root(), target.relative_to(_root()).as_posix(), revision, state, priority, note)
