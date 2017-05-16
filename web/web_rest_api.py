#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import logging
import sys_path

from flask import request
from flask_login import login_required, current_user
from web_app import app, csrf
from interface import project_info, dag_info

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

@csrf.exempt
@app.route('/dags/new_project', methods=['POST'])
@login_required
def new_projects():
    json_data = request.json
    user_id = current_user.get_id()
    project_name = json_data.get('project_name')
    project_desc = json_data.get('project_desc') or ''
    print project_name
    print project_desc
    ret_json = dict()
    if project_info.has_exist_project(project_name):
        ret_json['code'] = '1'
        ret_json['alert_message'] = '项目已经存在.'
        return json.dumps(ret_json)
    elif not project_info.add_new_project(project_name, project_desc, user_id):
        ret_json['code'] = '2'
        ret_json['alert_message'] = '新建项目失败.'
        return json.dumps(ret_json)
    ret_json['code'] = '0'
    ret_json['alert_message'] = '新建项目成功.'
    return json.dumps(ret_json)
