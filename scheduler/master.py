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

    def run(self):
        while True:
            logger.info('Start refresh ...')
            # to do
            logger.info('Success refresh ...')
            time.sleep(self.refresh_interval)

if __name__ == '__main__':
    try:
        master = Master()
        master.run()
    except Exception,e:
        logger.error('Master run exception:[%s]' % str(e))
        sys.exit(2)
