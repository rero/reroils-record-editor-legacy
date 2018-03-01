# -*- coding: utf-8 -*-

"""Utilities for reroils-record-editor."""

import copy

from flask import current_app
from invenio_pidstore.resolver import Resolver
from invenio_records.api import Record

from .babel_extractors import translate


def get_schema(schema):
    """Return jsonschemas dictionary."""
    ext = current_app.extensions.get('invenio-jsonschemas')
    keys = current_app.config['REROILS_RECORD_EDITOR_TRANSLATE_JSON_KEYS']
    return translate(ext.get_schema(schema), keys=keys)


def get_schema_url(schema):
    """Return jsonschemas url path."""
    ext = current_app.extensions.get('invenio-jsonschemas')
    return ext.path_to_url(schema)


def resolve(record_type, pid_value):
    """Resolve a pid value for a given record type."""
    config = current_app.config['RECORDS_REST_ENDPOINTS']
    config = config.get(record_type, {})
    pid_type = config.get('pid_type')
    resolver = Resolver(pid_type=pid_type,
                        object_type='rec',
                        getter=Record.get_record)
    return resolver.resolve(pid_value)


def clean_dict_keys(data):
    """Remove key having useless values."""
    # retrun a new list with defined value only
    if isinstance(data, list):
        to_return = []
        for item in data:
            tmp = clean_dict_keys(item)
            if tmp:
                to_return.append(tmp)
        return to_return

    # retrun a new dict with defined value only
    if isinstance(data, dict):
        to_return = {}
        for k, v in data.items():
            tmp = clean_dict_keys(v)
            if tmp:
                to_return[k] = tmp
        return to_return

    return data


def remove_pid(editor_options, pid_value):
    """Remove PID in the editor option for new record."""
    for option in reversed(editor_options):
        if isinstance(option, str):
            if option == pid_value:
                editor_options.remove(option)
        if isinstance(option, dict):
            items = option.get('items')
            if option.get('key') == pid_value:
                editor_options.remove(option)
            elif isinstance(items, list):
                new_items = remove_pid(items, pid_value)
                if new_items:
                    option['items'] = new_items
                else:
                    editor_options.remove(option)
        if isinstance(option, list):
            editor_options = remove_pid(option, pid_value)
    return editor_options
