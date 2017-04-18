#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import table_struct
import sys_path

from python_lib.database.mysql_config import MysqlConfig

class DatabaseConfig(MysqlConfig):
    # database config
    hostname = '127.0.0.1'
    port = '3306'
    user = 'root'
    password = '123456'
    db = 'test'
    charset = 'utf-8'

    # tables name
    T_USER_INFO = 'user_info'
    T_PROJECT_INFO = 'project_info'
    T_DAG_INFO = 'dag_info'
    T_TASK_INFO = 'task_info'
    T_MACHINE_INFO = 'machine_info'
    T_DAG_RUN_HISTORY = 'dag_run_history'
    T_TASK_RUN_HISTORY = 'task_run_history'
    T_TASK_PENDING_QUEUE = 'task_pending_queue'

    # tables struct
    S_USER_INFO = table_struct.UserInfo()
    S_PROJECT_INFO = table_struct.ProjectInfo()
    S_DAG_INFO = table_struct.DagInfo()
    S_TASK_INFO = table_struct.TaskInfo()
    S_MACHINE_INFO = table_struct.MachineInfo()
    S_DAG_RUN_HISTORY = table_struct.DagRunHistory()
    S_TASK_RUN_HISTORY = table_struct.TaskRunHistory()
    S_TASK_PENDING_QUEUE = table_struct.TaskPendingQueue()
