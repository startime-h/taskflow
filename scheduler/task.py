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
from common import sub_process
from db import table_struct
from db.interface import task_info
from db.interface import task_pending_queue

logger = logging_config.schedulerLogger()
logger.setLevel(logging.INFO)

class Task(threading.Thread):
    def __init__(self, simple_task_info, interval=5):
        super(Task, self).__init__()
        self.task_id = simple_task_info[table_struct.TaskPendingQueue.TaskId]
        self.machine_ip = simple_task_info[table_struct.TaskPendingQueue.MachineIp]
        self.interval = interval
        # init
        self.terminated = False
        self._get_full_task_info_()
        self._init_bash_cmd_()
        self._delete_pending_queue_()

    def _get_full_task_info_(self):
        row = task_info.select_task_by_id(self.task_id)
        if len(row) == 0:
            raise Exception("Current task:[%d] get detail info fail." % self.task_id)
        self.full_task_info = row

    def _init_bash_cmd_(self):
        self.retry_times = self.full_task_info.get(table_struct.TaskInfo.RetryTimes) or 1
        run_dir = self.full_task_info.get(table_struct.TaskInfo.RunDir)
        run_user = self.full_task_info.get(table_struct.TaskInfo.RunUser)
        run_cmd = self.full_task_info.get(table_struct.TaskInfo.RunCommand)
        new_cmd = 'cd %s && su - %s -c "%s"' % (run_dir, run_user, run_cmd)
        self.bash_cmd = new_cmd

    def _delete_pending_queue_(self):
        retry_times = self.retry_times
        while retry_times:
            succ = task_pending_queue.delete_pending_task(self.task_id, self.machine_ip)
            if succ: break
            retry_times -= 1

    def _update_task_status_(self):
        new_status = status.TASK_TERMINATED
        if not self.terminated:
            new_status = status.TASK_FAILED
        retry_times = self.retry_times
        while retry_times:
            succ = task_info.update_task_status(self.task_id, new_status)
            if succ: break
            retry_times -= 1

    def run(self):
        logger.info('Start run task:[%d]' % self.task_id)
        retry_times = self.retry_times
        while retry_times:
            # do bash cmd
            print self.bash_cmd
            stdout, stderr = sub_process.run(self.bash_cmd)
            #if stderr.strip() == '':
            self.terminated = True
            print stdout.strip()
            print stderr.strip()
            if self.terminated:break
            retry_times -= 1
        # set task status to Terminated
        self._update_task_status_()
        logger.info('Success run task:[%d]' % self.task_id)
