#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging
import socket

from flask import Flask
from flask_admin import Admin, base
from future import standard_library
standard_library.install_aliases()
from views.blueprints import routes
from views import views

def create_app(config=None, testing=False):
    # create app
    app = Flask(__name__)
    app.register_blueprint(routes)
    # set config
    with app.app_context():
        # create admin
        admin = Admin(app, name='Airflow', static_url_path='/admin', \
                index_view=views.HomeView(endpoint='', url='/admin', name="DAGs"), \
                template_mode='bootstrap3')
        av = admin.add_view
        # set category
        '''
        av(views.VersionView(name='Version', category="About"))
        # set menu link
        admin.add_link(base.MenuLink(category='Docs', name='Documentation', \
                url='http://pythonhosted.org/airflow/'))
        admin.add_link(base.MenuLink(category='Docs', name='Github', \
                url='https://github.com/apache/incubator-airflow'))
        '''
        return app

if __name__ == '__main__':
    try:
        app = create_app()
        print app
        app.run(port=5000)
    except Exception,e:
        logging.error('Start webserver failed!')
        sys.exit(2)
