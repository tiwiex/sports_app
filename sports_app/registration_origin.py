"""Request-scoped, server-only provenance for acceptance of an application."""

from contextlib import contextmanager
from contextvars import ContextVar

_origin = ContextVar("sports_registration_origin", default=None)


def current_registration():
	return _origin.get()


@contextmanager
def registration_origin(doc):
	token = _origin.set(doc)
	try:
		yield
	finally:
		_origin.reset(token)
