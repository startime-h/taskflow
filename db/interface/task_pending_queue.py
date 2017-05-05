#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import time
import datetime
import sys_path

from common import logging_config
from common import config_parser
from scheduler import status
import table_struct
import mysql_wrapper

logger = logging_config.dbLogger()
logger.setLevel(logging.INFO)

def select_pending_tasks(machine_ip, fields = '*'):
    '''
    With by condition map select pending tasks record

    @machine_ip: run machine ip address
    @fields: select fields, default equal *

    return rows/list()
    '''
    table = table_struct.T_TASK_PENDING_QUEUE
    mysql = mysql_wrapper.MysqlWrapper()
    cond_map = {
        table_struct.TaskPendingQueue.MachineIp: machine_ip
    }
    rows = mysql.select(table, cond_map, fields)
    if len(rows) == 0:
        logger.error('Select pending tasks get empty rows')
        return list()
    return rows

def add_pending_task(task_id, machine_ip):
    '''
    Add new pending task record

    @task_id: task id
    @machine_ip: machine ip address

    return True/False
    '''
    table = table_struct.T_TASK_PENDING_QUEUE
    mysql = mysql_wrapper.MysqlWrapper()
    cond_map = {
        table_struct.TaskPendingQueue.TaskId: task_id,
        table_struct.TaskPendingQueue.MachineIp: machine_ip
    }
    succ = mysql.insert(table, cond_map)
    if succ is False:
        logger.error('Add new pending task fail.')
        return False
    return True

def delete_pending_task(task_id, machine_ip):
    '''
    delete pending task record

    @task_id: ...
    @machine_ip: ...

    return True/False
    '''
    table = table_struct.T_TASK_PENDING_QUEUE
    mysql = mysql_wrapper.MysqlWrapper()
    cond_map = {
        table_struct.TaskPendingQueue.TaskId: task_id,
        table_struct.TaskPendingQueue.MachineIp: machine_ip
    }
    succ = mysql.delete(table, cond_map)
    if succ is False:
        logger.error('Delete pending task fail.')
        return False
    return True
