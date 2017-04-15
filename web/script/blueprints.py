#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import sys_path

from flask import (
    url_for, Markup, Blueprint, redirect,
)
import markdown

routes = Blueprint('routes', __name__)
@routes.route('/')
def index():
    return redirect(url_for('admin.index'))

@routes.route('/health')
def health():
    """ We can add an array of tests here to check the server's health """
    content = Markup(markdown.markdown("The server is healthy!"))
    return content
