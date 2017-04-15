#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging
import socket
import six

import sys_path

from flask import Flask
from flask_admin import Admin, base
from blueprints import routes
from future import standard_library
standard_library.install_aliases()

from script import views

def create_app(config=None, testing=False):
    app = Flask(__name__)
    app.register_blueprint(routes)
    # set config
    with app.app_context():
        # admin
        admin = Admin(app, name='Airflow', static_url_path='/admin', \
                index_view=views.HomeView(endpoint='', url='/admin', name="DAGs"), \
                template_mode='bootstrap3')
        av = admin.add_view

        # set category
        av(views.VersionView(name='Version', category="About"))
        # set menu link
        admin.add_link(base.MenuLink(category='Docs', name='Documentation', \
                url='http://pythonhosted.org/airflow/'))
        admin.add_link(base.MenuLink(category='Docs', name='Github', \
                url='https://github.com/apache/incubator-airflow'))

        # Hack to not add this view to the menu
        admin._menu = admin._menu[:-1]

        @app.context_processor
        def jinja_globals():
            return {
                'hostname': socket.getfqdn(),
            }
        return app

def webserver():
    HEADER =
    """
  ____________       _____________
 ____    |__( )_________  __/__  /________      __
____  /| |_  /__  ___/_  /_ __  /_  __ \_ | /| / /
___  ___ |  / _  /   _  __/ _  / / /_/ /_ |/ |/ /
 _/_/  |_/_/  /_/    /_/    /_/  \____/____/|__/
    """
    logging.info(settings.HEADER)
    app = create_app()
    run_args = [
        'gunicorn',
        '-w', str(num_workers),
        '-k', str(args.workerclass),
        '-t', str(worker_timeout),
        '-b', args.hostname + ':' + str(args.port),
        '-n', 'airflow-webserver',
        '-p', str(pid),
        '-c', 'airflow.www.gunicorn_config'
    ]

    run_args += ["airflow.www.app:cached_app()"]
    gunicorn_master_proc = subprocess.Popen(run_args)

if __name__ == '__main__':
    try:
        webserver()
    except Exception,e:
        logging.error('Start webserver failed!')
        sys.exit(2)
