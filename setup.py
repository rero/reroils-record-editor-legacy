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

"""reroils record editor"""

import os

from setuptools import find_packages, setup
from setuptools.command.egg_info import egg_info

readme = open('README.rst').read()
history = open('CHANGES.rst').read()


class EggInfoWithCompile(egg_info):
    def run(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog()
        option_dict = self.distribution.get_option_dict('compile_catalog')
        if option_dict.get('domain'):
            compiler.domain = [option_dict['domain'][1]]
        else:
            compiler.domain = ['messages']
        compiler.use_fuzzy = True
        compiler.directory = option_dict['directory'][1]
        compiler.run()
        super().run()


tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]


extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=2.6.2',
]

install_requires = [
    'dojson>=1.0',
    'Flask-BabelEx>=0.9.3',
    'invenio-access>=1.0.0',
    'invenio-assets>=1.0.0',
    'invenio-db >= 1.0.0',
    'invenio-indexer >= 1.0.0',
    'invenio-jsonschemas>=1.0.0',
    'invenio-records>=1.0.0',
    'invenio-records-rest>=1.0.1',
    'invenio-search>=1.0.0',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('reroils_record_editor', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    cmdclass={
        'egg_info': EggInfoWithCompile
    },
    name='reroils-record-editor',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio TODO',
    license='GPLv2',
    author='RERO',
    author_email='software@rero.ch',
    url='https://github.com/inveniosoftware/reroils-record-editor',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'reroils_record_editor = reroils_record_editor:ReroilsRecordEditor',
        ],
        'invenio_i18n.translations': [
            'messages = reroils_record_editor',
        ],
        'invenio_jsonschemas.schemas': [
            'record_editor = reroils_record_editor.jsonschemas'
        ],
        'babel.extractors': [
            'json = reroils_record_editor.babel_extractors:extract_json'
        ],
        'invenio_assets.bundles': [
            'reroils_record_editor_editor_js = reroils_record_editor.bundles:editor_js',
            'reroils_record_editor_i18n = reroils_record_editor.bundles:i18n'
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 1 - Planning',
    ],
)
