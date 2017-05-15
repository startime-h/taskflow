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
from db.interface import dag_info
from db import table_struct
import project_info
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

def get_user_project(user_id):
    '''
    get user all dag

    @user_id: user id, default equal 0

    return list/()
    '''
    project_name_list = project_info.get_user_project(user_id)
    if len(project_name_list) == 0:
        return list()
    project_list = list()
    for project_name in project_name_list:
        project_dict = dict()
        project_dict['project'] = project_name
        project_dict['dag_list'] = list()
        cond_map = {
            table_struct.DagInfo.ProjectName: project_name,
            table_struct.DagInfo.Valid: 1
        }
        rows = dag_info.select_dag_info(cond_map)
        dag_name_field = table_struct.DagInfo.DagName
        for dag_dict in rows:
            dag_name = dag_dict[dag_name_field]
            project_dict['dag_list'].append(dag_name)
        project_list.append(project_dict)
    return project_list
