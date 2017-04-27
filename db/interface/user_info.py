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

def select_user_info(user_id, user_name = '', user_email = ''):
    '''
    Select user info record

    @user_id: user id
    @user_name: user name
    @user_email: user email

    return row: success
           []: fail
    '''
    table = table_struct.T_USER_INFO
    cond_map = {
        table_struct.UserInfo.UserId : user_id
    }
    if user_name not in ['', None]:
        cond_map[table_struct.UserInfo.UserName] = user_name
    if user_email not in ['', None]:
        cond_map[table_struct.UserInfo.UserEmail] = user_email
    # do select
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select(table, cond_map)
    if len(rows) == 0:
        logger.error('Select user info get empty rows')
        return list()
    return rows

def add_user_info(user_id, user_name = '', user_email = ''):
    '''
    Add user info record

    @user_id: user id
    @user_name: user name
    @user_email: user email

    return > 0: record id
           -1: Fail
    '''

    pass

if __name__ == '__main__':
    print select_user_info(1)
    print select_user_info(1, 'cgl')
    print select_user_info(1, 'cgl@gmail.com')
