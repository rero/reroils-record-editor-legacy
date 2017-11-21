#!/bin/bash
# -*- coding: utf-8 -*-
echo "Building version: $1"
source /reroils/reroils/bin/activate && \
cd reroils/src && \
git clone https://gitlab.rero.ch/rero21/reroils-record-editor.git && \
cd reroils-record-editor;
pip install -r requirements.txt
pip install .[all]


