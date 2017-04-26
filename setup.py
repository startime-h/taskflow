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
        name='TaskFlow',
        description='[Web] Programmatically author, schedule and monitor data pipelines',
        license='Apache License 2.0',
        version=version,
        packages=find_packages(),
        include_package_data=True,
        data_files = [
            ('conf', ['conf/db.cfg', 'conf/logger.cfg'])
        ],
        install_requires=[
            'configparser>=3.5.0, <3.6.0',
            'MySQL-python'
        ],
        author='chenguolin',
        author_email='cgl@1079743846@gmail.com'
    )


if __name__ == "__main__":
    do_setup()
