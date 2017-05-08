#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import threading
import sys_path

from datetime import datetime, timedelta
from flask import render_template, url_for, redirect
from flask_login import UserMixin, login_user, logout_user, login_required
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from common import logging_config
from web_app import app, login_manager
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

class LoginForm(Form):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.password_hash = self.get_password_hash()
        self.id = self.get_id()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        save user name, id and password hash to mysql table
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_password_hash(self):
        """
        try to get password hash from mysql table
        return password_hash/None
        """
        try:
            return None
        except Exception,e:
            return None
        return None

    def get_id(self):
        """
        get user id from mysql table, if not exist, it will generate a uuid for the user.
        """
        if self.username is not None:
            pass
        return unicode(uuid.uuid4())

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                for user_name, profile in user_profiles.iteritems():
                    if profile[1] == user_id:
                        return User(user_name)
        except:
            return None
        return None

SingleAuthUser = User()

@login_manager.user_loader
def load_user(userid):
    return SingleAuthUser

# login route
@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

