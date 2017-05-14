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

def select_user_info(cond_map):
    '''
    Select user info record

    cond_map = {
        user_name: user name
        user_email: user email
        ...
    }

    return row: success
           []: fail
    '''
    table = table_struct.T_USER_INFO
    # do select
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select(table, cond_map)
    if len(rows) == 0:
        logger.error('Select user info get empty rows')
        return dict()
    return rows[0]

def has_user_info(user_name):
    '''
    check has user in mysql table

    @user_name: user name

    return True/False
    '''
    cond_map = {
        table_struct.UserInfo.UserName: user_name
    }
    row = select_user_info(cond_map)
    if len(row.keys()) == 0:
        return False
    return True

def add_user_info(user_name, user_password_hash,user_email, register_time):
    '''
    Add user info record

    @user_name: user name
    @user_password_hash: user password hash
    @user_email: user email
    @register_time: register time

    return True: sucess
           False: fail
    '''
    # do insert
    table = table_struct.T_USER_INFO
    cond_map = {
        table_struct.UserInfo.UserName: user_name,
        table_struct.UserInfo.UserPasswordHash: user_password_hash,
        table_struct.UserInfo.UserEmail: user_email,
        table_struct.UserInfo.RegisterTime: register_time
    }
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.insert(table, cond_map)
    if succ is False:
        logger.error('Insert user info fail.')
        return False
    return True

def select_max_user_id():
    '''
    Select max user id

    return id/None
    '''
    table = table_struct.T_USER_INFO
    # do select
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select(table, cond_map)
    if len(rows) == 0:
        logger.error('Select user info get empty rows')
        return dict()
    return rows[0]

def has_user_info(user_name):
    '''
    check has user in mysql table

    @user_name: user name

    return True/False
    '''
    cond_map = {
        table_struct.UserInfo.UserName: user_name
    }
    row = select_user_info(cond_map)
    if len(row.keys()) == 0:
        return False
    return True

def add_user_info(user_name, user_password_hash,user_email, register_time):
    '''
    Add user info record

    @user_name: user name
    @user_password_hash: user password hash
    @user_email: user email
    @register_time: register time

    return True: sucess
           False: fail
    '''
    # do insert
    table = table_struct.T_USER_INFO
    cond_map = {
        table_struct.UserInfo.UserName: user_name,
        table_struct.UserInfo.UserPasswordHash: user_password_hash,
        table_struct.UserInfo.UserEmail: user_email,
        table_struct.UserInfo.RegisterTime: register_time
    }
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.insert(table, cond_map)
    if succ is False:
        logger.error('Insert user info fail.')
        return False
    return True

def select_max_user_id():
    '''
    Select max user id

    return id/0
    '''
    table = table_struct.T_USER_INFO
    cond_str = '1=1'
    fields = table_struct.UserInfo.ID
    order_field = table_struct.UserInfo.ID
    order_desc = True
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select_with_condition(table, cond_str, fields, order_field, order_desc)
    if len(rows) == 0:
        return 0
    return rows[0][table_struct.UserInfo.ID]
