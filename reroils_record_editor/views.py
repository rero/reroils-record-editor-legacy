# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 RERO.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""reroils record editor."""

# TODO: This is an example file. Remove it if you do not need it, including
# the templates and static folders as well as the test case.

from __future__ import absolute_import, print_function

import uuid
from urllib.request import urlopen

import six
from dojson.contrib.marc21.utils import create_record, split_stream
from flask import Blueprint, abort, current_app, flash, jsonify, redirect, \
    render_template, request, url_for
from flask_babelex import gettext as _
from flask_login import current_user
from flask_menu import current_menu
from flask_principal import PermissionDenied, RoleNeed
from invenio_access.permissions import DynamicPermission
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_records.api import Record
from reroils_data import minters
from reroils_data.dojson.contrib.unimarctojson import unimarctojson
from reroils_data.utils import remove_pid

from .utils import get_schema, get_schema_url

blueprint = Blueprint(
    'reroils_record_editor',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/editor'
)

record_edit_permission = DynamicPermission(RoleNeed('cataloguer'))


@blueprint.errorhandler(PermissionDenied)
def permission_denied_page(error):
    """Show a personalized error message."""
    if not current_user.is_authenticated:
        return redirect(url_for(
                    current_app.config['ADMIN_LOGIN_ENDPOINT'],
                    next=request.url))
    return render_template(current_app.config['THEME_403_TEMPLATE']), 404


@blueprint.app_template_filter()
def can_edit(user=None):
    """User has editor role."""
    if not user:
        user = current_user
    return user.is_authenticated and record_edit_permission.can()


@blueprint.before_app_first_request
def init_menu():
    """Initialize menu before first request."""
    item = current_menu.submenu('main.cataloging')
    item.register(
        endpoint=None,
        text=_('Cataloging'),
        visible_when=can_edit,
        order=0
    )
    subitem = current_menu.submenu('main.cataloging.new')
    subitem.register(
        endpoint='reroils_record_editor.index',
        text='<i class="fa fa-pencil-square-o fa-fw"></i> %s' % _('New'),
        visible_when=can_edit,
        order=1
    )


@blueprint.route("/new")
@record_edit_permission.require()
def index():
    """Render a basic view."""
    from json import loads
    from pkg_resources import resource_string

    options = current_app.config['REROILS_RECORD_EDITOR_FORM_OPTIONS']
    options_in_bytes = resource_string(*options)
    editor_options = loads(options_in_bytes.decode('utf8'))
    remove_pid(editor_options)

    return render_template(
        "reroils_record_editor/index.html",
        form=editor_options,
        model={'$schema': get_schema_url(
            current_app.config['REROILS_RECORD_EDITOR_JSONSCHEMA']
        )},
        schema=get_schema(
            current_app.config['REROILS_RECORD_EDITOR_JSONSCHEMA']
        )
    )


@blueprint.route("/records/save", methods=['POST'])
@record_edit_permission.require()
def save_record():
    """Save record."""
    record = request.get_json()
    uid = uuid.uuid4()
    pid = minters.bibid_minter(uid, record)

    # clean dirty data provided by angular-schema-form
    from reroils_data.utils import clean_dict_keys
    record = clean_dict_keys(record)

    rec = Record.create(record, id_=uid)

    message = {
        "pid": pid.pid_value
    }

    db.session.commit()
    record_indexer = RecordIndexer()
    record_indexer.index(rec)

    flash(
        'the record %s with uuid %s has been created' % (pid.pid_value, uid),
        'success'
    )

    return jsonify(message)


@blueprint.route("/import/bnf/ean/<int:ean>")
@record_edit_permission.require()
def import_bnf_ean(ean):
    """Import record from BNFr given a isbn 13 without dashes."""
    bnf_url = current_app.config['REROILS_RECORD_EDITOR_IMPORT_BNF_EAN']
    try:
        with urlopen(bnf_url % ean) as response:
            if response.status != 200:
                abort(500)
            # read the xml date from the HTTP response
            xml_data = response.read()

            # create a xml file in memory
            xml_file = six.BytesIO()
            xml_file.write(xml_data)
            xml_file.seek(0)

            # get the record in xml if exists
            # note: the request should returns one record max
            xml_record = next(split_stream(xml_file))

            # convert xml in marc json
            json_data = create_record(xml_record)

            # convert marc json to local json format
            record = unimarctojson.do(json_data)
            return jsonify(record)

    # no record found!
    except StopIteration:
        abort(404)
    # other errors
    except Exception as e:
        import sys
        print(e)
        sys.stdout.flush()
        abort(500)
