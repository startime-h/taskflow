#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging

from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand

logger = logging.getLogger(__name__)
version = '0.0.1'

def do_setup():
    setup(
        name='TaskScheduler_Web',
        description='[Web] Programmatically author, schedule and monitor data pipelines',
        license='Apache License 2.0',
        version=version,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'flask>=0.11, <0.12',
            'flask-admin==1.4.1',
            'future>=0.16.0, <0.17',
            'jinja2>=2.7.3, <2.9.0',
        ],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Topic :: System :: Monitoring',
        ],
        author='chenguolin',
        author_email='cgl@1079743846@gmail.com'
    )


if __name__ == "__main__":
    do_setup()
