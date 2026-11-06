"""Bounded private enrollment portraits; never accept a guest-supplied file URL."""

import base64
import binascii
import hashlib
import io
import warnings

import frappe
from frappe import _
from PIL import Image, UnidentifiedImageError

MAX_BYTES = 2 * 1024 * 1024


def prepare_image(value):
	if not value:
		return None
	if not isinstance(value, str) or len(value) > (MAX_BYTES * 4 // 3 + 200):
		frappe.throw(_("Choose a player image no larger than 2 MB."))
	try:
		header, encoded = value.split(",", 1)
		if header not in ("data:image/jpeg;base64", "data:image/png;base64", "data:image/webp;base64"):
			raise ValueError
		content = base64.b64decode(encoded, validate=True)
		if len(content) > MAX_BYTES:
			raise ValueError
		with warnings.catch_warnings():
			warnings.simplefilter("error", Image.DecompressionBombWarning)
			with Image.open(io.BytesIO(content)) as source:
				if source.format not in ("JPEG", "PNG", "WEBP") or getattr(source, "is_animated", False):
					raise ValueError
				if source.width * source.height > 20_000_000:
					raise ValueError
				source.load()
				image = source.convert("RGB")
				image.thumbnail((1600, 1600))
				output = io.BytesIO()
				image.save(output, format="JPEG", quality=88)
		content = output.getvalue()
	except (
		ValueError,
		binascii.Error,
		OSError,
		UnidentifiedImageError,
		Image.DecompressionBombError,
		Image.DecompressionBombWarning,
	):
		frappe.throw(_("Choose a valid, non-animated JPEG, PNG or WebP player image (maximum 2 MB)."))
	return {"content": content, "hash": hashlib.sha256(content).hexdigest()}


def save_registration_image(doc, image):
	if not image:
		return
	file = frappe.get_doc(
		doctype="File",
		file_name="player-portrait.jpg",
		content=image["content"],
		is_private=1,
		owner="Administrator",
		attached_to_doctype="Sports Registration",
		attached_to_name=doc.name,
		attached_to_field="player_photo",
	).insert(ignore_permissions=True)
	doc.db_set("player_photo", file.file_url, update_modified=False)


def link_player_image(doc, player):
	url = doc.get("player_photo")
	if not url:
		return
	if not url.startswith("/private/files/") or not frappe.db.exists(
		"File",
		{
			"file_url": url,
			"is_private": 1,
			"attached_to_doctype": "Sports Registration",
			"attached_to_name": doc.name,
		},
	):
		frappe.throw(_("The enrollment image is not a valid private attachment."))
	frappe.get_doc(
		doctype="File",
		file_name="player-portrait.jpg",
		file_url=url,
		is_private=1,
		owner="Administrator",
		attached_to_doctype="Sports Player",
		attached_to_name=player,
		attached_to_field="player_photo",
	).insert(ignore_permissions=True)
	frappe.db.set_value("Sports Player", player, "player_photo", url, update_modified=False)
