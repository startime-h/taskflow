#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sys_path
from flask import (url_for, Markup, Blueprint, redirect)

routes = Blueprint('routes', __name__)
@routes.route('/')
def index():
    return redirect(url_for('admin.index'))
