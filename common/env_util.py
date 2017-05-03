#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging

import sys_path
import logging_config
import sub_process

logger = logging_config.commonLogger()
logger.setLevel(logging.INFO)

def get_hostname():
    '''
    get machine hostname

    return hostname/None
    '''
    cmd = 'hostname'
    stdout, stderr = sub_process.run(cmd)
    if len(stderr.strip()) != 0:
        logger.error('Get hostname error:[%s]' % stderr.strip())
        return None
    return stdout.strip()

def get_hostip():
    '''
    get machine ip address

    return hostname/None
    '''
    cmd = 'hostname -i'
    stdout, stderr = sub_process.run(cmd)
    if len(stderr.strip()) != 0:
        logger.error('Get hostname error:[%s]' % stderr.strip())
        return None
    return stdout.strip()
