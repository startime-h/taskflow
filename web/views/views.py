#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import ast
import json
import logging

from datetime import datetime, timedelta
from flask import (redirect, url_for, request, Markup, Response, current_app, render_template, make_response)
from flask_admin import BaseView, expose, AdminIndexView

import sys_path

class HomeView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('dags.html')
