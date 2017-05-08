#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import sys_path

from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required

from web_app import app
from common import logging_config
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

# view route
@app.route('/', methods=['GET'])
def index_route():
    """
    Redirect to the dashboard.
    """
    return redirect(url_for('jobs'))

@app.route('/jobs', methods=['GET'])
@login_required
def jobs():
    """
    Show information on all known Jobs.
    """
    return render_template('jobs.html', jobs={})

@app.route('/jobs/import', methods=['POST'])
@login_required
def jobs_import_view():
    """
    Import a Job and redirect to the Jobs page.
    """
    import_job()
    return redirect(url_for('jobs'))
