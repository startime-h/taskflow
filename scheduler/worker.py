#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import sys_path

from common import logging_config
from common import config_parser
from common import env_util
from db.interface import task_pending_queue

logger = logging_config.schedulerLogger()
logger.setLevel(logging.INFO)

class Worker(object):
    def __init__(self, refresh_interval=5):
        '''
        default refresh interval equal 5 seconds
        '''
        self.refresh_interval = refresh_interval
        self.tasks = list()
        self._get_worker_ip_()

    def _get_worker_ip_(self):
        self.worker_ip = env_util.get_hostip()
        if self.worker_ip is None:
            raise Exception("Current worker get ip address fail.")

    def _refresh_once_(self):
        self.tasks = task_pending_queue.select_pending_tasks(self.worker_ip)

    def scheduler(self):
        while True:
            for task_id in self.tasks:
                print task_id
            logger.info('Start refresh once')
            time.sleep(self.refresh_interval)
            self._refresh_once_()
            logger.info('Success refresh once')

if __name__ == '__main__':
    try:
        worker = Worker()
        worker.scheduler()
    except Exception,e:
        logger.error('Worker run exception:[%s]' % str(e))
        sys.exit(2)
