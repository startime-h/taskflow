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

from flask import Flask, send_from_directory
from flask_login import LoginManager

logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

WEB_CONF_PATH = sys_path.__parent_dir__+ '/conf/web.cfg'

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = "login"

def start():
    web_config = config_parser.Config(WEB_CONF_PATH)

    # app config
    app.debug = web_config.get_section_key('web', 'debug')
    app.secret_key = web_config.get_section_key('web', 'app_secret')
    app.config['LOGIN_DISABLED'] = web_config.get_section_key('web', 'auth_disabled')
    app.config['APP_PASSWORD'] = web_config.get_section_key('web', 'password')
    app.config['AUTH_RATE_LIMIT'] = 30
    app.config['AUTH_ATTEMPTS'] = []
    app.config['APP_HOST'] = web_config.get_section_key('web', 'host')
    app.config['APP_PORT'] = web_config.get_section_key('web', 'port')

    # login manager init app
    login_manager.init_app(app)

    # run flask app
    host = app.config['APP_HOST']
    port = app.config['APP_PORT']
    app.run(host=host, port=port, use_reloader=False)

if __name__ == '__main__':
    try:
        start()
    except Exception,e:
        logger.error('Flask web app run exception:[%s]' % str(e))
        sys.exit(2)
