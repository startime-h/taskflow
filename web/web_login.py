#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import uuid
import sys_path

from datetime import datetime, timedelta
from flask import render_template, url_for, redirect
from flask_login import UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from common import logging_config
from web_app import app, login_manager
from interface import user_info
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

class User(UserMixin):
    def __init__(self, username, password='', email=''):
        self.username = username
        self.password = self.__generate_password_hash__(password)
        self.email = email
        self.id = self.get_id()

    def __generate_password_hash__(self, password):
        try:
            return generate_password_hash(password)
        except Exception,e:
            logger.error('Generate password hash exception:[%s]' % str(e))
            return None

    def __generate_user_id__(self):
        return unicode(uuid.uuid4())

    def get_id(self):
        if not self.has_exist_user():
            return self.__generate_user_id__()
        return user_info.get_user_id(self.username)

    def register_new_user(self):
        self.user_id = self.id
        succ = user_info.register_new_user(self.user_id, self.username, self.password, self.email)
        if succ is False:
            logger.error('Fail Register new user. user name:[%s], email:[%s]' % (self.username, self.email))
        logger.info('Success Register new user. user name:[%s], email:[%s]' % (self.username, self.email))

    def has_exist_user(self):
        return user_info.has_exist_user(self.username)

    def verify_password(self, password):
        store_password_hash = user_info.get_password(self.username)
        if store_password_hash is None:
            logger.error('Fail get user password from mysql. user name:[%s]' % self.username)
            return False
        return check_password_hash(store_password_hash, password)

    @staticmethod
    def get(user_id):
        store_user_name = user_info.get_user_info(user_id)
        if store_user_name is None:
            return None
        return User(store_user_name)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
