#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import threading
import sys_path

from common import logging_config
from common import time_util
from db.interface import user_info
from db import table_struct
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

def register_new_user(user_id, username, password, email):
    '''
    register new user

    @new_uesr: User object

    return True/False
    '''
    if None in [user_id, username, password, email]:
        return False
    if user_info.has_user_info(username):
        return True
    register_time = time_util.get_cur_datetime()
    if register_time is None:
        return False
    return user_info.add_user_info(user_id, username, password, email, register_time)

def has_exist_user(user_name):
    '''
    check has exist user name

    @user_name: user name

    return True/False
    '''
    return user_info.has_user_info(user_name)

def get_password(user_name):
    '''
    get user password hash

    @user_name: user name

    return str/None
    '''
    cond_map = {
        table_struct.UserInfo.UserName: user_name
    }
    row = user_info.select_user_info(cond_map)
    if len(row.keys()) == 0:
        return None
    return row[table_struct.UserInfo.UserPasswordHash]

def get_user_id(user_name):
    '''
    get user id

    @user_name: user name

    return user_id/None
    '''
    cond_map = {
        table_struct.UserInfo.UserName: user_name
    }
    row = user_info.select_user_info(cond_map)
    if len(row.keys()) == 0:
        return None
    user_id = row[table_struct.UserInfo.UserId]
    return user_id

def get_user_info(user_id):
    '''
    get user info

    @user_id: user id

    return user_name/None
    '''
    cond_map = {
        table_struct.UserInfo.UserId: user_id
    }
    row = user_info.select_user_info(cond_map)
    if len(row.keys()) == 0:
        return None
    user_name = row[table_struct.UserInfo.UserName]
    return user_name
