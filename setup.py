# -*- coding: utf-8 -*-

import os
import sys
import logging
from setuptools import setup, find_packages

setup_status = setup(
    name='TaskFlow',
    description='Programmatically author, schedule and monitor data pipelines',
    license='Apache License 2.0',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    data_files = [
        ('conf', ['conf/db.cfg', 'conf/logger.cfg', 'conf/web.cfg'])
    ],
    install_requires=[
        'MySQL-python>=1.2.5',
        'configparser>=3.5.0',
        'flask>=0.11',
        'flask-login>=0.2.6',
        'flask-admin>=1.4.1',
        'flask-cache>=0.13.1',
        'flask-swagger>=0.2.13',
        'flask-wtf>=0.12',
        'werkzeug>=0.12',
        'wtforms>=2.1',
        'future>=0.16.0',
        'jinja2>=2.7.3',
    ],
    author='chenguolin',
    author_email='cgl@1079743846@gmail.com'
)
