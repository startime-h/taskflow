#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import logging
import sys_path

from flask import request
from flask_login import login_required
from web_app import app, csrf
from interface import dag_info
from common import logging_config
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

@csrf.exempt
@app.route('/dags/get_projects', methods=['POST'])
@login_required
def get_projects():
    json_data = request.json
    user_id = json_data.get('user_id')
    project_list = dag_info.get_user_project(user_id)
    return json.dumps(project_list)
