#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging

import sys_path
import sub_process
import logging_config

logger = logging_config.commonLogger()
logger.setLevel(logging.INFO)

def get_hostname():
    '''
    get machine hostname

    return True, hostname
           False, stderr
    '''
    cmd = 'hostname'
    stdout, stderr = sub_process.run(cmd)
    if len(stderr.strip()) != 0:
        logger.error('Get hostname error:[%s]' % stderr.strip())
        return False, stderr
    return True, stdout.strip()

def get_hostip():
    '''
    get machine ip address

    return True, hostname
           False, stderr
    '''
    cmd = 'hostname -i'
    stdout, stderr = sub_process.run(cmd)
    if len(stderr.strip()) != 0:
        logger.error('Get hostname error:[%s]' % stderr.strip())
        return False, stderr
    return True, stdout.strip()
