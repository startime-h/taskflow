#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import sys_path

from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm

from web_app import app
from web_login import User
from common import logging_config
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)

class RegisterForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email= StringField('Email Address', validators=[DataRequired()])

class ProjectForm(FlaskForm):
    projectName = StringField('Project Name', validators=[DataRequired()])
    projectDesc = StringField('Project Desc', validators=[DataRequired()])
