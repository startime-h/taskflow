#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import sys_path

from common import logging_config
from common import config_parser
from scheduler import status
import table_struct
import mysql_wrapper

logger = logging_config.dbLogger()
logger.setLevel(logging.INFO)

def select_all_task_info():
    '''
    Select all task info record

    return rows/list()
    '''
    table = table_struct.T_TASK_INFO
    condition_str = '1=1'
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select_with_condition(table, condition_str)
    if len(rows) == 0:
        logger.error('Select all task info get empty rows')
        return list()
    return rows

def select_task_by_id(task_id, fields = '*'):
    '''
    Select task by task id

    @task_id: task id

    return row/list()
    '''
    table = table_struct.T_TASK_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    cond_map = {
        table_struct.TaskInfo.TaskId: task_id
    }
    rows = mysql.select(table, cond_map, fields)
    if len(rows) == 0:
        logger.error('Select task info get empty rows')
        return list()
    return rows[0]

def select_task_info(cond_map, fields = '*'):
    '''
    With by condition map select task info record

    @cond_map = {
        'task_id': ...
        'task_name': ...
        ...
    }
    @fields: select fields, default equal *

    return rows/list()
    '''
    table = table_struct.T_TASK_INFO
    # do select
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select(table, cond_map, fields)
    if len(rows) == 0:
        logger.error('Select task info get empty rows')
        return list()
    return rows

def add_task_info(cond_map):
    '''
    Add new task info record

    @cond_map = {
        'task_id': ...
        'task_name': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_TASK_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    # do select
    rows = select_task_info(cond_map)
    if len(rows) != 0:
        logger.warn('Has task info in mysql.')
        return True
    # do insert
    succ = mysql.insert(table, cond_map)
    if succ is False:
        logger.error('Add task info fail.')
        return False
    return True

def update_task_info(new_value_map, cond_map):
    '''
    update task info record

    @new_value_map = {
        'task_id': ...
        'task_name': ...
        ...
    }
    @cond_map = {
        'task_id': ...
        'task_name': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_TASK_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.update(table, new_value_map, cond_map)
    if succ is False:
        logger.error('Update task info fail.')
        return False
    return True

def delete_task_info(cond_map):
    '''
    delete task info record

    @cond_map = {
        'task_id': ...
        'task_name': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_TASK_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.delete(table, cond_map)
    if succ is False:
        logger.error('Delete task info fail.')
        return False
    return True

def select_dag_running_task(dag_id):
    '''
    select dag all running task

    @dag_id: dag id

    return rows/list()
    '''
    table = table_struct.T_TASK_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    cond_map = {
            table_struct.TaskInfo.DagId: dag_id,
            table_struct.TaskInfo.TaskStatus: status.TASK_RUNNING
    }
    rows = mysql.select(table, cond_map, fields)
    if len(rows) == 0:
        logger.error('dag:[%d] select running tasks get empty.' % dag_id)
        return list()
    return rows

def update_dag_all_tasks_status(dag_id, new_status):
    '''
    update dag all task status

    @dag_id: dag id
    @new_status: new task status

    return True/False
    '''
    cond_map = {
        table_struct.TaskInfo.DagId: dag_id
    }
    new_value_map = {
        table_struct.TaskInfo.TaskStatus: new_status
    }
    return update_task_info(new_value_map, cond_map)

def get_task_run_machine(task_id):
    '''
    select task run machine ip address

    @task_id: task id

    return machine_ip/None
    '''
    cond_map = {
        table_struct.TaskInfo.TaskId: task_id
    }
    rows = select_task_info(cond_map)
    if len(rows) == 0:
        logger.error('task:[%d] not found in mysql.' % task_id)
        return None
    row = rows[0]
    return row[table_struct.TaskInfo.RunMachine]

def update_task_status(task_id, new_status):
    '''
    update task status

    @task_id: task id
    @new_status: new status

    return True/False
    '''
    cond_map = {
        table_struct.TaskInfo.TaskId: task_id
    }
    new_value_map = {
        table_struct.TaskInfo.TaskStatus: new_status
    }
    return update_task_info(new_value_map, cond_map)
