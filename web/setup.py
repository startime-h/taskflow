# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand

import imp
import logging
import os
import sys

logger = logging.getLogger(__name__)
version = '0.0.1'

def do_setup():
    setup(
        name='nbflow_web',
        description='[Web] Programmatically author, schedule and monitor data pipelines',
        license='Apache License 2.0',
        version=version,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'alembic>=0.8.3, <0.9',
            'configparser>=3.5.0, <3.6.0',
            'croniter>=0.3.8, <0.4',
            'dill>=0.2.2, <0.3',
            'flask>=0.11, <0.12',
            'flask-admin==1.4.1',
            'flask-cache>=0.13.1, <0.14',
            'flask-login==0.2.11',
            'flask-swagger==0.2.13',
            'flask-wtf==0.12',
            'funcsigs==1.0.0',
            'future>=0.16.0, <0.17',
            'gitpython>=2.0.2',
            'gunicorn>=19.3.0, <19.4.0',
            'jinja2>=2.7.3, <2.9.0',
            'lxml>=3.6.0, <4.0',
            'markdown>=2.5.2, <3.0',
            'pandas>=0.17.1, <1.0.0',
            'psutil>=4.2.0, <5.0.0',
            'pygments>=2.0.1, <3.0',
            'python-daemon>=2.1.1, <2.2',
            'python-dateutil>=2.3, <3',
            'python-nvd3==0.14.2',
            'requests>=2.5.1, <3',
            'setproctitle>=1.1.8, <2',
            'sqlalchemy>=0.9.8',
            'tabulate>=0.7.5, <0.8.0',
            'thrift>=0.9.2, <0.10',
            'zope.deprecation>=4.0, <5.0',
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
