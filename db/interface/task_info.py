#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import sys_path

from common import logging_config
from common import config_parser
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

def update_task_info(new_cond_map, old_cond_map):
    '''
    update task info record

    @new_cond_map = {
        'task_id': ...
        'task_name': ...
        ...
    }
    @old_cond_map = {
        'task_id': ...
        'task_name': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_TASK_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.update(table, new_cond_map, old_cond_map)
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

if __name__ == '__main__':
    rows = select_all_task_info()
    for row in rows: print row
    pass
