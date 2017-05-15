#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import sys_path

from common import logging_config
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

from web_app import app
from web_login import *
from web_views import *
from web_form import *
from web_rest_api import *

def start():
    '''
    host = 127.0.0.1 only access by localhost
    host = 0.0.0.0 any can access
    '''
    debug = app.debug
    host = app.config['APP_HOST']
    port = int(app.config['APP_PORT'])
    use_reloader = app.config['APP_USE_RELOADER']
    logger.info('Start run flask web app port:[%d]' % port)
    app.run(host=host, debug=debug, port=port, use_reloader=use_reloader)

if __name__ == '__main__':
    try:
        start()
    except Exception,e:
        logger.error('Flask web app run exception:[%s]' % str(e))
        sys.exit(2)
