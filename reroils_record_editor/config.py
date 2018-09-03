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

# from invenio_indexer.api import RecordIndexer
# from invenio_records.api import Record

REROILS_RECORD_EDITOR_BASE_TEMPLATE = 'reroils_record_editor/base.html'
"""Default base template for the demo page."""

REROILS_RECORD_EDITOR_EDITOR_TEMPLATE = 'reroils_record_editor/editor.html'
"""Default editor template."""

REROILS_RECORD_EDITOR_OPTIONS = dict(
    recid=dict(
        api='/api/records',
        search_template='reroils_record_editor/search.html',
        results_template='templates/invenio_search_ui/marc21/default.html',
        schema='records/record-v0.0.1.json',
        record_class='invenio_records.api.Record',
        indexer_class='invenio_indexer.api.RecordIndexer'
        # form_options=('reroils_record_editor.form_options',
        #               'records/record-v0.0.1.json'),
        # form_options_create_exclude=['controll']
    )
)

REROILS_RECORD_EDITOR_TRANSLATE_JSON_KEYS = [
    'title', 'description',
    'validationMessage', 'placeholder'
]
