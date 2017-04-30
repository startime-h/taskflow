#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import sys_path

from common import logging_config
from common import config_parser

logger = logging_config.schedulerLogger()
logger.setLevel(logging.INFO)

class Master(object):
    def __init__(self, refresh_interval=60):
        '''
        default refresh interval equal 60 seconds
        '''
        self.refresh_interval = refresh_interval
        self.dags = list()
        self.stop = False

    def scheduler(self):
        while not self.stop:
            for dag in self.dags:
                pass
            time.sleep(self.refresh_interval)

if __name__ == '__main__':
    try:
        master = Master()
        master.scheduler()
    except Exception,e:
        logger.error('Master run exception:[%s]' % str(e))
        sys.exit(2)
