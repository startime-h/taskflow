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

logger = logging_config.commonLogger()
logger.setLevel(logging.INFO)

def select_project_info(cond_map, fields = '*'):
    '''
    With by condition map select project info record

    @cond_map = {
        'project_id': ...
        ...
    }
    @fields: select fields, default equal *

    return rows/list()
    '''
    table = table_struct.T_PROJECT_INFO
    # do select
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select(table, cond_map, fields)
    if len(rows) == 0:
        logger.error('Select proejct info get empty rows')
        return list()
    return rows

def add_project_info(cond_map):
    '''
    Add new project info record

    @cond_map = {
        'project_id': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_PROJECT_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    # do select
    rows = select_project_info(cond_map)
    if len(rows) != 0:
        logger.warn('Has proejct info in mysql.')
        return True
    # do insert
    succ = mysql.insert(table, cond_map)
    if succ is False:
        logger.error('Add proejct info fail.')
        return False
    return True

def update_project_info(new_cond_map, old_cond_map):
    '''
    update project info record

    @new_cond_map = {
        'project_id': ...
        ...
    }
    @old_cond_map = {
        'project_id': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_PROJECT_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.update(table, new_cond_map, old_cond_map)
    if succ is False:
        logger.error('Update project info fail.')
        return False
    return True

def delete_project_info(cond_map):
    '''
    delete project info record

    @cond_map = {
        'project_id': ...
        ...
    }

    return True/False
    '''
    table = table_struct.T_PROJECT_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.delete(table, cond_map)
    if succ is False:
        logger.error('Delete project info fail.')
        return False
    return True

if __name__ == '__main__':
    '''
    cond_map = {}
    print select_project_info(cond_map)

    cond_map = {
            'project_id': 1
    }
    print select_project_info(cond_map)

    cond_map = {
            'project_id': 1
    }
    print add_project_info(cond_map)
    cond_map = {
            'project_id': 1
    }
    print select_project_info(cond_map)

    cond_map = {
            'project_id': 1,
            'project_name': 'test',
            'create_user_id': 1,
            'create_time': '2017-04-29 10:00:00',
            'permission_users': '1'
    }
    print add_project_info(cond_map)
    cond_map = {
            'project_id': 1
    }
    print select_project_info(cond_map)
    old_cond_map = {
            'project_id': 1
    }
    new_cond_map = {
            'project_id': 100
    }
    print update_project_info(new_cond_map, old_cond_map)
    print select_project_info(old_cond_map)
    print select_project_info(new_cond_map)
    cond_map = {
            'project_id': 100
    }
    print delete_project_info(cond_map)
    print select_project_info(cond_map)
    '''
    pass
