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

"""JS/CSS bundles for theme."""

from __future__ import absolute_import, print_function

import os

from flask_assets import Bundle
from invenio_assets import AngularGettextFilter, GlobBundle, NpmBundle
from pkg_resources import resource_filename


def catalog(domain):
    """Return glob matching path to tranlated messages for a given domain."""
    return os.path.join(
        resource_filename('reroils_record_editor', 'translations'),
        '*',  # language code
        'LC_MESSAGES',
        '{0}.po'.format(domain),
    )

catalog_name = 'reroilsRecordEditorTranslations'

i18n = GlobBundle(
    catalog('messages'),
    filters=AngularGettextFilter(catalog_name=catalog_name),
    output='gen/reroils_record_editor.i18n.%(version)s.js',
)

schema_form_js = NpmBundle(
    'node_modules/angular/angular.js',
    'node_modules/angular-sanitize/angular-sanitize.min.js',
    'node_modules/tv4/tv4.js',
    'node_modules/objectpath/lib/ObjectPath.js',
    'node_modules/angular-schema-form/dist/schema-form.js',
    'node_modules/angular-schema-form/dist/bootstrap-decorator.js',
    npm={
        'angular': '~1.6.9',
        'angular-sanitize': '~1.6.9',
        'tv4': '^1.3.0',
        'objectpath': '^1.2.1',
        'angular-schema-form': '^0.8.13'
    }
)

editor_js = Bundle(
    schema_form_js,
    'js/reroils_record_editor/reroils-editor.js',

    # filters='jsmin',
    output='gen/reroils_record_editor.editor_js.%(version)s.js',
)
