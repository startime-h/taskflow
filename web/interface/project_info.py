#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import threading
import sys_path

from common import logging_config
from common import time_util
from db.interface import project_info
from db import table_struct
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

def has_exist_project(project_name):
    '''
    check has exist user name

    @user_name: user name

    return True/False
    '''
    cond_map = {
        table_struct.ProjectInfo.ProjectName: project_name
    }
    rows = project_info.select_project_info(cond_map)
    if len(rows) == 0:
        return False
    return True

def add_new_project(project_name, project_desc, current_user_id):
    '''
    add new project

    @project_name: project name
    @project_desc: project description
    @current_user_id: user id

    return True/False
    '''
    current_time = time_util.get_cur_datetime()
    permission_users = current_user_id
    cond_map = {
        table_struct.ProjectInfo.ProjectName: project_name,
        table_struct.ProjectInfo.ProjectDesc: project_name,
        table_struct.ProjectInfo.CreateUserId: current_user_id,
        table_struct.ProjectInfo.CreateTime: current_time,
        table_struct.ProjectInfo.ProjectDesc: project_desc,
        table_struct.ProjectInfo.PermissionUsers: permission_users
    }
    return project_info.add_project_info(cond_map)
