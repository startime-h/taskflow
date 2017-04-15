#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import ast
import pkg_resources
import socket
from functools import wraps
from datetime import datetime, timedelta
import dateutil.parser
import copy
import json

import inspect
from textwrap import dedent
from past.builtins import basestring, unicode
import traceback

from flask import (
    redirect, url_for, request, Markup, Response, current_app, render_template, make_response)
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_admin.babel import lazy_gettext
from flask_admin.tools import iterdecode
from flask_login import flash
from flask._compat import PY2

import jinja2
import markdown
import nvd3

from wtforms import (
    Form, SelectField, TextAreaField, PasswordField, StringField, validators)

from pygments import highlight, lexers
from pygments.formatters import HtmlFormatter

############################################
class HomeView(AdminIndexView):
    @expose("/")
    def index(self):
        pass

