#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import sys_path

from common import logging_config
from common import config_parser

logger = logging_config.schedulerLogger()
logger.setLevel(logging.INFO)

class Master(object):
    def __init__(self):
        pass

    def run(self):
        while True:
            pass

if __name__ == '__main__':
    try:
        master = Master()
        master.run()
    except Exception,e:
        logger.error('Master run exception:[%s]' % str(e))
        sys.exit(2)
