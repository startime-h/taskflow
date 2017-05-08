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
from flask import Flask
from flask_login import LoginManager

logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

WEB_CONF_PATH = sys_path.__parent_dir__ + '/conf/web.cfg'

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = "login"

def init_app_config(app):
    web_config = config_parser.Config(WEB_CONF_PATH)

    # app config
    app.debug = web_config.get_section_key('web', 'debug')
    app.secret_key = web_config.get_section_key('web', 'secret_key')
    app.config['APP_USE_RELOADER'] = web_config.get_section_key('web', 'use_reloader')
    app.config['APP_PASSWORD'] = web_config.get_section_key('web', 'password')
    app.config['APP_HOST'] = web_config.get_section_key('web', 'host')
    app.config['APP_PORT'] = web_config.get_section_key('web', 'port')

    # login manager init app
    login_manager.init_app(app)

# init app config
init_app_config(app)

