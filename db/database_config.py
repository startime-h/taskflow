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
    T_FLOW_USER_INFO = 'flow_user_info'
    T_FLOW_DAG = 'flow_dag'
    T_FLOW_Task = 'flow_task'
    T_FLOW_DAG_HISTORY = 'flow_dag_history'

    # tables struct
    S_FLOW_USER_INFO = table_struct.FlowUserInfo()
    S_FLOW_DAG = table_struct.FlowDag()
    S_FLOW_Task = table_struct.FlowTask()
    S_FLOW_DAG_HISTORY = table_struct.FlowDagHistory()
