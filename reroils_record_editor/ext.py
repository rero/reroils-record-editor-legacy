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

from __future__ import absolute_import, print_function

from flask_babelex import gettext as _

from . import config
# from .views import blueprint
from .views import create_blueprint


class ReroilsRecordEditor(object):
    """Reroils-Record-Editor extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        # TODO: This is an example of translation string with comment. Please
        # remove it.
        # NOTE: This is a note to a translator.
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        opt = app.config['REROILS_RECORD_EDITOR_OPTIONS']
        app.register_blueprint(create_blueprint(opt))
        app.extensions['reroils-record-editor'] = self

    def init_config(self, app):
        """Initialize configuration."""
        # Use theme's base template if theme is installed
        if 'BASE_TEMPLATE' in app.config:
            app.config.setdefault(
                'REROILS_RECORD_EDITOR_BASE_TEMPLATE',
                app.config['BASE_TEMPLATE'],
            )
        for k in dir(config):
            if k.startswith('REROILS_RECORD_EDITOR_'):
                app.config.setdefault(k, getattr(config, k))
