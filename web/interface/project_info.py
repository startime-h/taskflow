#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import threading
import sys_path

from common import logging_config, time_util
from db import table_struct
from db.interface import project_info
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

def get_user_project(user_id):
    '''
    get user all project

    @user_id: user id, default equal 0

    return list()/[]
    '''
    rows = project_info.select_all_project_info()
    project_list = list()
    project_name_field = table_struct.ProjectInfo.ProjectName
    permission_users_field = table_struct.ProjectInfo.PermissionUsers
    for project_dict in rows:
        project_name = project_dict[project_name_field]
        permission_users_list = project_dict[permission_users_field].split(',')
        if user_id == 0:
            project_list.append(project_name)
        else:
            if str(user_id) in permission_users_list:
                project_list.append(project_name)
    return project_list
