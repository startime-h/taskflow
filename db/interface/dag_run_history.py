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

def select_all_dag_run_history():
    '''
    Select all dag run history record

    return rows/list()
    '''
    table = table_struct.T_DAG_RUN_HISTORY
    condition_str = '1=1'
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select_with_condition(table, condition_str)
    if len(rows) == 0:
        logger.error('Select all dag run history get empty rows')
        return list()
    return rows

def select_dag_run_history(cond_map, fields = '*'):
    '''
    With by condition map select dag run history record

    @cond_map = {
        'dag_id': ...
        'dag_name': ...
        ...
    }
    @fields: select fields, default equal *

    return rows/list()
    '''
    table = table_struct.T_DAG_RUN_HISTORY
    # do select
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select(table, cond_map, fields)
    if len(rows) == 0:
        logger.error('Select dag run history get empty rows')
        return list()
    return rows

def add_dag_run_history(cond_map):
    '''
    Add new dag run history record

    @cond_map = {
        'dag_id': ...
        'dag_name': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_DAG_RUN_HISTORY
    mysql = mysql_wrapper.MysqlWrapper()
    # do select
    rows = select_dag_run_history(cond_map)
    if len(rows) != 0:
        logger.warn('Has dag run history in mysql.')
        return True
    # do insert
    succ = mysql.insert(table, cond_map)
    if succ is False:
        logger.error('Add dag run history fail.')
        return False
    return True

def update_dag_run_history(new_value_map, cond_map):
    '''
    update dag run history record

    @new_value_map = {
        'dag_id': ...
        'dag_name': ...
        ...
    }
    @cond_map = {
        'dag_id': ...
        'dag_name': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_DAG_RUN_HISTORY
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.update(table, new_value_map, cond_map)
    if succ is False:
        logger.error('Update dag run history fail.')
        return False
    return True

def delete_dag_run_history(cond_map):
    '''
    delete dag run history record

    @cond_map = {
        'dag_id': ...
        'dag_name': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_DAG_RUN_HISTORY
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.delete(table, cond_map)
    if succ is False:
        logger.error('Delete dag run history fail.')
        return False
    return True
