#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import sys_path
import logging.config

LOGGER_CONF_PATH = sys_path.__parent_dir__ + '/conf/logger.cfg'
logging.config.fileConfig(LOGGER_CONF_PATH)

def rootLogger():
    return logging.getLogger("root")

def commonLogger():
    return logging.getLogger("common")

def dbLogger():
    return logging.getLogger("db")

def webLogger():
    return logging.getLogger("web")

def schedulerLogger():
    return logging.getLogger("scheduler")
