# -*- coding: utf-8 -*-

"""Utilities for reroils-record-editor."""

from flask import current_app


def get_schema(schema):
    """Return jsonschemas dictionary."""
    ext = current_app.extensions.get('invenio-jsonschemas')
    return ext.get_schema(schema)
