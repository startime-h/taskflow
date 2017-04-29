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

def update_dag_info(new_cond_map, old_cond_map):
    '''
    update dag info record

    @new_cond_map = {
        'dag_id': ...
        'dag_name': ...
        ...
    }
    @old_cond_map = {
        'dag_id': ...
        'dag_name': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_DAG_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.update(table, new_cond_map, old_cond_map)
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

if __name__ == '__main__':
    pass
