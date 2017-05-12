#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import threading
import sys_path

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

from common import logging_config
from common import config_parser
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
login_manager = LoginManager()
csrf = CSRFProtect()

def init_app_config(app):
    web_conf_path= sys_path.__parent_dir__ + '/conf/web.cfg'
    web_config = config_parser.Config(web_conf_path)

    # app config
    app.debug = web_config.get_section_key('web', 'debug')
    app.secret_key = web_config.get_section_key('web', 'secret_key')
    app.config['APP_USE_RELOADER'] = web_config.get_section_key('web', 'use_reloader')
    app.config['APP_PASSWORD'] = web_config.get_section_key('web', 'password')
    app.config['APP_HOST'] = web_config.get_section_key('web', 'host')
    app.config['APP_PORT'] = web_config.get_section_key('web', 'port')

def init_login_manager(app):
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'login'
    login_manager.init_app(app)

def init_csrf(app):
    csrf.init_app(app)

# init app config
init_app_config(app)
init_login_manager(app)
init_csrf(app)
