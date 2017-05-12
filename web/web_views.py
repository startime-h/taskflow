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

# login route
@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dags'))
    page_type='login'
    form = LoginForm()
    return render_template('login.html', page_type=page_type, \
        form=form, alert=request.args.get('alert'))

@app.route('/dologin', methods=['POST'])
def dologin():
    user_name = request.form.get('username', None)
    password = request.form.get('password', None)
    remember_me = request.form.get('remember_me', False)
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
def index():
    return redirect(url_for('dags'))

@app.route('/dags', methods=['GET'])
@login_required
def dags():
    return render_template('all_dags.html', all_dags_active='True')

@app.route('/new_project', methods=['GET'])
@login_required
def new_project():
    return render_template('new_project.html', new_project_active='True')

@app.route('/new_dag', methods=['GET'])
@login_required
def new_dag():
    return render_template('new_dag.html', new_dag_active='True')

@app.route('/permission', methods=['GET'])
@login_required
def permission():
    return render_template('permission.html', permission_active='True')

@app.route('/help', methods=['GET'])
@login_required
def help():
    return render_template('help.html', help_active='True')

# REST api
@app.route('/get_my_dags', methods=['GET'])
@login_required
def get_my_dags():
    return redirect(url_for('dags'))
