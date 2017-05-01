# -*- coding: utf-8 -*-

import os
import sys
import logging
from setuptools import setup, find_packages, Command

def do_setup():
    setup(
        name='TaskFlow',
        description='[Web] Programmatically author, schedule and monitor data pipelines',
        license='Apache License 2.0',
        version='0.0.1',
        packages=find_packages(),
        include_package_data=True,
        data_files = [
            ('conf', ['conf/db.cfg', 'conf/logger.cfg'])
        ],
        install_requires=[
            'configparser>=3.5.0, <3.6.0',
            'MySQL-python',
            'flask==0.9',
            'flask-login==0.2.6'
        ],
        author='chenguolin',
        author_email='cgl@1079743846@gmail.com'
    )

if __name__ == "__main__":
    do_setup()
