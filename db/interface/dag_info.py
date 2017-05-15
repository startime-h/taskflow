#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import datetime
import sys_path

from common import logging_config
from common import config_parser
from scheduler import status
import table_struct
import mysql_wrapper

logger = logging_config.dbLogger()
logger.setLevel(logging.INFO)

def select_all_dag_info():
    '''
    Select all dag info record

    return rows/list()
    '''
    table = table_struct.T_DAG_INFO
    condition_str = '1=1'
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select_with_condition(table, condition_str)
    if len(rows) == 0:
        logger.error('Select all dag info get empty rows')
        return list()
    return rows

def select_dag_info(cond_map, fields = '*'):
    '''
    With by condition map select dag info record

    @cond_map = {
        'dag_id': ...
        'dag_name': ...
        ...
    }
    @fields: select fields, default equal *

    return rows/list()
    '''
    table = table_struct.T_DAG_INFO
    # do select
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select(table, cond_map, fields)
    if len(rows) == 0:
        logger.error('Select dag info get empty rows')
        return list()
    return rows

def select_dag_info_with_condition(cond_str, fields = '*'):
    '''
    With by condition string select dag info record

    @cond_str: condition string
    @fields: select fields, default equal *

    return rows/list()
    '''
    table = table_struct.T_DAG_INFO
    # do select
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select_with_condition(table, cond_str, fields)
    if len(rows) == 0:
        logger.error('Select dag info get empty rows')
        return list()
    return rows

def add_dag_info(cond_map):
    '''
    Add new dag info record

    @cond_map = {
        'dag_id': ...
        'dag_name': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_DAG_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    # do select
    rows = select_dag_info(cond_map)
    if len(rows) != 0:
        logger.warn('Has dag info in mysql.')
        return True
    # do insert
    succ = mysql.insert(table, cond_map)
    if succ is False:
        logger.error('Add dag info fail.')
        return False
    return True

def update_dag_info(new_value_map, cond_map):
    '''
    update dag info record

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
    table = table_struct.T_DAG_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.update(table, new_value_map, cond_map)
    if succ is False:
        logger.error('Update dag info fail.')
        return False
    return True

def delete_dag_info(cond_map):
    '''
    delete dag info record

    @cond_map = {
        'dag_id': ...
        'dag_name': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_DAG_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.delete(table, cond_map)
    if succ is False:
        logger.error('Delete dag info fail.')
        return False
    return True

def select_need_start_dag(current_time):
    '''
    Select all need start dag info

    return rows/list()
    '''
    table = table_struct.T_DAG_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    condition_str = '(%s = 1 and %s != \'%s\' and %s != \'%s\' and %s <= \'%s\') \
            or (%s = 1 and %s = \'%s\' and %s = 1 and %s <= \'%s\')'% \
            (table_struct.DagInfo.Valid, able_struct.DagInfo.DagStatus, status.DAG_RUNNING, \
             table_struct.DagInfo.DagStatus, status.DAG_FAILED, table_struct.DagInfo.NextStartTime, \
             current_time, table_struct.DagInfo.Valid, table_struct.DagInfo.DagStatus, \
             status.DAG_FAILED, table_struct.DagInfo.SkipFailed, table_struct.DagInfo.NextStartTime, current_time)
    return select_dag_info_with_condition(condition_str)

def update_dag_status_and_starttime(new_value_map):
    '''
    update dag status and next start time

    @cond_map = {
        'id' ...
    }

    return True/False
    '''
    cond_map = {
        table_struct.DagInfo.ID: new_value_map[table_struct.DagInfo.ID]
    }
    # udpate status
    new_value_map[table_struct.DagInfo.DagStatus] = status.DAG_RUNNING
    # udpate next starttime
    scheduler_interval = new_value_map[table_struct.DagInfo.SchedulerInterval]
    next_starttime = int(time.time()) + scheduler_interval
    next_starttime = datetime.datetime.fromtimestamp(next_starttime).strftime('%Y-%m-%d %H:%M:%S')
    new_value_map[table_struct.DagInfo.NextStartTime] = next_starttime
    # do update
    return update_dag_info(new_value_map, cond_map)

def update_dag_status(row_id, new_status):
    '''
    update dag status to terminated

    @row_id: record id
    @new_status: new DAG status

    return True/False
    '''
    cond_map = {
        table_struct.DagInfo.ID: row_id
    }
    new_value_map = {
        table_struct.DagInfo.DagStatus: new_status
    }
    return update_dag_info(new_value_map, cond_map)
