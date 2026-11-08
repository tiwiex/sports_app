"""Management-only supporting documents, stored under a protected parent record."""

import base64
import binascii
import hashlib
import io

import frappe
from frappe import _
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PyPdfError

from sports_app.academy import can_manage_settings, require_settings_access
from sports_app.player_profile import CAPABILITY, DOCUMENT, player_record, request_identity

MAX_BYTES = 5 * 1024 * 1024


def has_permission(doc, user=None, **kwargs):
	# Returning None retains native role, sharing and User Permission checks for managers.
	return None if can_manage_settings(user) else False


def permission_query(user=None):
	return "" if can_manage_settings(user) else "1=0"


def file_permission_query(user=None):
	# Frappe's generic File list checks readable parent types, but not each parent's
	# Company restrictions. Apply the native protected-document query as well.
	if not frappe.db.exists("DocType", DOCUMENT):
		return ""
	condition = "(`tabFile`.`attached_to_doctype` IS NULL OR `tabFile`.`attached_to_doctype` != 'Sports Player Document')"
	if not can_manage_settings(user) or not frappe.has_permission(DOCUMENT, "read", user=user):
		return condition
	names = frappe.get_list(DOCUMENT, pluck="name", page_length=0, user=user)
	if not names:
		return condition
	allowed = ",".join(frappe.db.escape(name) for name in names)
	return f"({condition} OR `tabFile`.`attached_to_name` IN ({allowed}))"


def prepare_file(data):
	if not isinstance(data, str) or len(data) > MAX_BYTES * 4 // 3 + 200:
		frappe.throw(_("Choose a PDF or image no larger than 5 MB."))
	try:
		header, encoded = data.split(",", 1)
		content = base64.b64decode(encoded, validate=True)
		if not content or len(content) > MAX_BYTES:
			raise ValueError
		if header == "data:application/pdf;base64":
			if not content.startswith(b"%PDF-"):
				raise ValueError
			reader = PdfReader(io.BytesIO(content), strict=True)
			if reader.is_encrypted or not 1 <= len(reader.pages) <= 100:
				raise ValueError
			# Do not retain active PDF actions, embedded files or forms in this prototype.
			root = reader.trailer["/Root"]
			if any(key in root for key in ("/OpenAction", "/AA", "/Names", "/AcroForm")):
				raise ValueError
			for page in reader.pages:
				if page.get("/AA") or page.get("/Annots"):
					raise ValueError
			writer = PdfWriter()
			for page in reader.pages:
				writer.add_page(page)
			sanitized = io.BytesIO()
			writer.write(sanitized)
			content = sanitized.getvalue()
			extension = "pdf"
		else:
			from sports_app.enrollment_images import prepare_image

			image = prepare_image(data)
			content = image["content"]
			extension = "jpg"
	except (ValueError, TypeError, KeyError, binascii.Error, OSError, PyPdfError):
		frappe.throw(
			_(
				"Choose a valid unencrypted PDF without active content, or a JPEG/PNG/WebP image. Images are limited to 2 MB; PDFs to 5 MB and 100 pages."
			)
		)
	return dict(content=content, extension=extension, hash=hashlib.sha256(content).hexdigest())


def protect_file(doc, method=None):
	if doc.attached_to_doctype == "Sports Scholarship Decision":
		frappe.throw(
			_("Scholarship file attachments are not enabled. Record the restricted decision reason instead.")
		)
	previous = doc.get_doc_before_save()
	if doc.attached_to_doctype != DOCUMENT and (not previous or previous.attached_to_doctype != DOCUMENT):
		return
	require_settings_access()
	if not doc.is_private or doc.attached_to_doctype != DOCUMENT or not doc.attached_to_name:
		frappe.throw(
			_("Player supporting documents must remain private and attached to their protected record.")
		)
	if not previous and doc.flags.player_profile_service is not CAPABILITY:
		frappe.throw(
			_("Add supporting files through Add private document in the player profile."),
			frappe.PermissionError,
		)
	parent = frappe.get_doc(DOCUMENT, doc.attached_to_name)
	parent.check_permission("write")
	player_record(parent.player, write=True)
	if previous and any(
		previous.get(key) != doc.get(key)
		for key in ("file_url", "is_private", "attached_to_doctype", "attached_to_name", "owner")
	):
		frappe.throw(
			_("A supporting file cannot be replaced, shared publicly or moved. Add a new document instead.")
		)
	doc.owner = "Administrator"  # File owner shortcuts must not outlive the uploader's management role.
	if doc.file_url and not doc.file_url.startswith("/private/files/"):
		frappe.throw(_("Supporting documents require a private local file."))


@frappe.whitelist(methods=["POST"])
def add_document(
	name: str,
	title: str,
	document_type: str,
	file_data: str,
	request_key: str,
	document_date: str | None = None,
):
	require_settings_access()
	player = player_record(name, write=True)
	prepared = prepare_file(file_data)
	values = dict(
		player=player.name,
		title=title.strip() if isinstance(title, str) else "",
		document_type=document_type,
		document_date=document_date or None,
	)
	digest = request_identity(request_key, {**values, "file_hash": prepared["hash"]})
	previous = frappe.db.get_value(
		DOCUMENT,
		{"request_key": request_key},
		["name", "player", "request_hash"],
		as_dict=True,
		for_update=True,
	)
	if previous:
		frappe.get_doc(DOCUMENT, previous.name).check_permission("read")
		if previous.player != name or previous.request_hash != digest:
			frappe.throw(_("This document request already contains different details."))
		return previous.name
	frappe.db.savepoint("sports_profile_document")
	try:
		doc = frappe.get_doc(
			doctype=DOCUMENT,
			**values,
			company=player.company,
			recorded_on=frappe.utils.now_datetime(),
			recorded_by=frappe.session.user,
			request_key=request_key,
			request_hash=digest,
		)
		doc.flags.player_profile_service = CAPABILITY
		doc.insert()
		file = frappe.get_doc(
			doctype="File",
			file_name="player-document." + prepared["extension"],
			content=prepared["content"],
			is_private=1,
			owner="Administrator",
			attached_to_doctype=DOCUMENT,
			attached_to_name=doc.name,
			attached_to_field="file_url",
		)
		file.flags.player_profile_service = CAPABILITY
		file.insert(ignore_permissions=True)
		doc.db_set("file_url", file.file_url, update_modified=False)
		# Native submitted-parent protection stops File deletion before disk unlink.
		doc.submit()
	except Exception:
		frappe.db.rollback(save_point="sports_profile_document")
		raise
	return doc.name
