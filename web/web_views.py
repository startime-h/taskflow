#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import sys_path

from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user
from flask_login import login_user, logout_user, login_required
from web_app import app
from web_login import User
from web_form import *
from interface import project_info
from interface import dag_info
from common import logging_config
logger = logging_config.webLogger()
logger.setLevel(logging.INFO)

##################       login/register views         #################
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    page_type='register'
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        email = request.form.get('email', None)
        user = User(user_name, password, email)
        if user.has_exist_user():
            return redirect(url_for('register', alert="User already exists"))
        user.register_new_user()
        return redirect(url_for('login'))
    return render_template('register.html', form=form,
           page_type=page_type, alert=request.args.get('alert'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dags'))
    page_type='login'
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        # check has in mysql
        user = User(user_name, password)
        if not user.validate():
            return redirect(url_for('login', alert="Incorrect username or password"))
        if not user.has_exist_user():
            return redirect(url_for('register'))
        if not user.verify_password(password):
            return redirect(url_for('login', alert="Incorrect password"))
        # cache session
        login_user(user, remember=remember_me)
        return redirect(url_for('dags'))
    return render_template('login.html', page_type=page_type, \
        form=form, alert=request.args.get('alert'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

######################       page views         #######################
@app.route('/', methods=['GET'])
@login_required
def index():
    return redirect(url_for('dags'))

@app.route('/dags', methods=['GET'])
@login_required
def dags():
    all_dags_active = 'True'
    user_id = current_user.get_id()
    project_list = dag_info.get_user_project(user_id)
    return render_template('all_dags.html', all_dags_active=all_dags_active, \
           project_list=project_list)

@app.route('/permission', methods=['GET'])
@login_required
def permission():
    permission_active = 'True'
    user_id = current_user.get_id()
    project_list = dag_info.get_user_project(user_id)
    return render_template('permission.html', permission_active=permission_active, \
           project_list=project_list)

@app.route('/help', methods=['GET'])
@login_required
def help():
    help_active = 'True'
    user_id = current_user.get_id()
    project_list = dag_info.get_user_project(user_id)
    return render_template('help.html', help_active=help_active, \
           project_list=project_list)
