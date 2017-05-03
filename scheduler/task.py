#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import logging
import threading
import sys_path

import status
from common import logging_config
from common import config_parser
from db import table_struct
from db.interface import task_info

logger = logging_config.schedulerLogger()
logger.setLevel(logging.INFO)

class Task(threading.Thread):
    def __init__(self, task_id, retry_times=3, interval=5):
        super(Task, self).__init__()
        self.task_id = task_id
        self.retry_times = retry_times
        self.interval = interval
        # init
        self.stop = False
        self.terminated = False

    def _check_once_(self):
        pass

    def _update_task_status_(self):
        new_status = status.TASK_TERMINATED
        if not self.terminated:
            new_status = status.TASK_FAILED
        retry_times = self.retry_times
        while retry_times:
            pass

    def run(self):
        logger.info('Start run task:[%d]' % self.task_id)
        while not self.stop:
            time.sleep(self.interval)
            self._check_once_()
        # set task status to Terminated
        self._update_dag_status_()
        logger.info('Success run task:[%d]' % self.task_id)
