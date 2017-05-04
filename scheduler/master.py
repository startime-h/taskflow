#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import threading
import sys_path

from common import logging_config
from common import config_parser
from db.interface import dag_info

from dag import Dag

logger = logging_config.schedulerLogger()
logger.setLevel(logging.INFO)

class Master():
    def __init__(self, refresh_interval=5):
        '''
        default refresh interval equal 5 seconds
        '''
        self.refresh_interval = refresh_interval
        self.dags = list()

    def _current_datetime_(self, format='%Y-%m-%d %H:%M:%S'):
        return time.strftime(format)

    def _refresh_once_(self):
        current_time = self._current_datetime_()
        self.dags = dag_info.select_need_start_dag(current_time)

    def scheduler(self):
        self._refresh_once_()
        while True:
            for dag_row in self.dags:
                succ = dag_info.update_dag_status_and_starttime(dag_row)
                if not succ:
                    continue
                dag = Dag(dag_row)
                dag.daemon = True
                dag.start()
            logger.info('Start refresh once')
            time.sleep(self.refresh_interval)
            self._refresh_once_()
            logger.info('Success refresh once')

if __name__ == '__main__':
    try:
        master = Master()
        master.scheduler()
    except Exception,e:
        logger.error('Master run exception:[%s]' % str(e))
        sys.exit(2)
