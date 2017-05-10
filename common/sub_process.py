#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import subprocess

import sys_path
import logging_config
logger = logging_config.commonLogger()
logger.setLevel(logging.INFO)

def run(cmd):
    '''
    Run subprocess wait terminate

    @cmd: run shell command

    return stdout, stderr
    '''
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    child.wait()
    stdout, stderr = child.communicate()
    return stdout, stderr
