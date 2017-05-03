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

def select_all_user_info():
    '''
    Select all user info record

    return row: success
           []: fail
    '''
    table = table_struct.T_USER_INFO
    condition_str = '1=1'
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select_with_condition(table, condition_str)
    if len(rows) == 0:
        logger.error('Select user info get empty rows')
        return list()
    return rows

def select_user_info(user_id, user_name, user_email):
    '''
    Select user info record

    @user_id: user account
    @user_name: user name
    @user_email: user email

    return row: success
           []: fail
    '''
    table = table_struct.T_USER_INFO
    cond_map = {
        table_struct.UserInfo.UserId: user_id,
        table_struct.UserInfo.UserName: user_name,
        table_struct.UserInfo.UserEmail: user_email
    }
    # do select
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select(table, cond_map)
    if len(rows) == 0:
        logger.error('Select user info get empty rows')
        return list()
    return rows[0]

def add_user_info(user_id, user_name, user_email):
    '''
    Add user info record

    @user_id: user id
    @user_name: user name
    @user_email: user email

    return True: sucess
           False: fail
    '''
    # check has in mysql
    row = select_user_info(user_id, user_name, user_email)
    if len(row) != 0:
        return True
    # do insert
    table = table_struct.T_USER_INFO
    cond_map = {
        table_struct.UserInfo.UserId: user_id,
        table_struct.UserInfo.UserName: user_name,
        table_struct.UserInfo.UserEmail: user_email
    }
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.insert(table, cond_map)
    if succ is False:
        logger.error('Insert user info fail.')
        return False
    return True

def update_user_info(row_id, new_user_id, new_user_name, new_user_email):
    '''
    udpate user info record

    @row_id: table row id
    @new_user_id: new user id
    @new_user_name: new user name
    @new_user_email: new user email

    return True: sucess
           False: fail
    '''
    # do update record
    table = table_struct.T_USER_INFO
    new_value_map = {
        table_struct.UserInfo.UserId: new_user_id,
        table_struct.UserInfo.UserName: new_user_name,
        table_struct.UserInfo.UserEmail: new_user_email
    }
    cond_map = {
        table_struct.UserInfo.ID: row_id
    }
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.update(table, new_value_map, cond_map)
    if succ is False:
        logger.error('Update user info fail.')
        return False
    return True

def delete_user_info(cond_map):
    '''
    delete user info record

    @cond_map = {
        user_id: xxx
        ...
    }

    return True: sucess
           False: fail
    '''
    # do delete record
    table = table_struct.T_USER_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.delete(table, cond_map)
    if succ is False:
        logger.error('Delete user info fail.')
        return False
    return True

if __name__ == '__main__':
    rows = select_all_user_info()
    for row in rows: print row
    pass
