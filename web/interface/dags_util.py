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
