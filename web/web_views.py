#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import sys_path

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user
from flask_login import login_user, logout_user, login_required

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

# login route
@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('my_dags'))
    page_type='login'
    form = LoginForm()
    return render_template('login.html', form=form, \
           page_type = page_type, alert=request.args.get('alert'))

@app.route('/dologin', methods=['POST'])
def dologin():
    user_name = request.form.get('username', None)
    password = request.form.get('password', None)
    remember_me = request.form.get('remember_me', False)
    # check has in mysql
    user = User(user_name, password)
    if not user.has_exist_user():
        return redirect(url_for('/register'))
    if not user.verify_password(password):
        return redirect(url_for('login', alert="Incorrect password"))
    # check success
    login_user(user)
    return redirect(url_for('my_dags'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# register route
@app.route('/register', methods=['GET'])
def register():
    page_type='register'
    form = RegisterForm()
    return render_template('register.html', form=form,
           page_type=page_type, alert=request.args.get('alert'))

@app.route('/doregister', methods=['POST'])
def doregister():
    user_name = request.form.get('username', None)
    password = request.form.get('password', None)
    email = request.form.get('email', None)
    user = User(user_name, password, email)
    if user.has_exist_user():
        return redirect(url_for('register', alert="User already exists"))
    user.register_new_user()
    return redirect(url_for('login'))

# view route
@app.route('/', methods=['GET'])
@login_required
def index_route():
    return redirect(url_for('my_dags'))

@app.route('/my', methods=['GET'])
@login_required
def my_dags():
    return render_template('my_dags.html', my_dags_active='True')

@app.route('/all', methods=['GET'])
@login_required
def all_dags():
    return render_template('all_dags.html', all_dags_active='True')

@app.route('/permission', methods=['GET'])
@login_required
def permission():
    return render_template('permission.html', permission_active='True')

@app.route('/help', methods=['GET'])
@login_required
def help():
    return render_template('help.html', help_active='True')
