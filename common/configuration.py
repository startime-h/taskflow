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
#
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import copy
import logging
import six

from builtins import str
from string import Template
from collections import OrderedDict
from configparser import ConfigParser
from exceptions import AirflowConfigException

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '/../config/airflow.cfg')

class AirflowConfigParser(ConfigParser):
    as_command_stdout = {
        ('core', 'sql_alchemy_conn'),
        ('core', 'fernet_key'),
        ('celery', 'broker_url'),
        ('celery', 'celery_result_backend')
    }

    def __init__(self, *args, **kwargs):
        super(ConfigParser, self).__init__(*args, **kwargs)
        self.is_validated = False
        self.__read__(CONFIG_FILE_PATH)

    def __read__(self, filenames):
        ConfigParser.read(self, filenames)
        self.__validate__()

    def __validate__(self):
        if (self.get("core", "executor") != 'SequentialExecutor' and "sqlite" in self.get('core', 'sql_alchemy_conn')):
            raise AirflowConfigException("error: cannot use sqlite with the {}".format(self.get('core', 'executor')))
        elif (self.getboolean("webserver", "authenticate") and self.get("webserver", "owner_mode") not in ['user', 'ldapgroup']):
            raise AirflowConfigException("error: owner_mode option should be either 'user' or 'ldapgroup' when filtering by owner is set")
        elif (self.getboolean("webserver", "authenticate") and self.get("webserver", "owner_mode").lower() == 'ldapgroup' and
                self.get("webserver", "auth_backend") != ('airflow.contrib.auth.backends.ldap_auth')):
            raise AirflowConfigException("error: attempt at using ldapgroup filtering without using the Ldap backend")
        self.is_validated = True

    def __get_env_var_option__(self, section, key):
        # must have format AIRFLOW__{SECTION}__{KEY} (note double underscore)
        env_var = 'AIRFLOW__{S}__{K}'.format(S=section.upper(), K=key.upper())
        if env_var in os.environ:
            return expand_env_var(os.environ[env_var])

    def _get_cmd_option(self, section, key):
        fallback_key = key + '_cmd'
        # if this is a valid command key...
        if (section, key) in AirflowConfigParser.as_command_stdout:
            # if the original key is present, return it no matter what
            if self.has_option(section, key):
                return ConfigParser.get(self, section, key)
            # otherwise, execute the fallback key
            elif self.has_option(section, fallback_key):
                command = self.get(section, fallback_key)
                return run_command(command)

    def get(self, section, key, **kwargs):
        section = str(section).lower()
        key = str(key).lower()

        # first check environment variables
        option = self._get_env_var_option(section, key)
        if option is not None:
            return option

        # ...then the config file
        if self.has_option(section, key):
            return expand_env_var(
                ConfigParser.get(self, section, key, **kwargs))

        # ...then commands
        option = self._get_cmd_option(section, key)
        if option:
            return option

        else:
            logging.warning("section/key [{section}/{key}] not found "
                            "in config".format(**locals()))

            raise AirflowConfigException(
                "section/key [{section}/{key}] not found "
                "in config".format(**locals()))

    def getboolean(self, section, key):
        val = str(self.get(section, key)).lower().strip()
        if '#' in val:
            val = val.split('#')[0].strip()
        if val.lower() in ('t', 'true', '1'):
            return True
        elif val.lower() in ('f', 'false', '0'):
            return False
        else:
            raise AirflowConfigException(
                'The value for configuration option "{}:{}" is not a '
                'boolean (received "{}").'.format(section, key, val))

    def getint(self, section, key):
        return int(self.get(section, key))

    def getfloat(self, section, key):
        return float(self.get(section, key))


    def as_dict(self, display_source=False, display_sensitive=False):
        """
        Returns the current configuration as an OrderedDict of OrderedDicts.
        :param display_source: If False, the option value is returned. If True,
            a tuple of (option_value, source) is returned. Source is either
            'airflow.cfg' or 'default'.
        :type display_source: bool
        :param display_sensitive: If True, the values of options set by env
            vars and bash commands will be displayed. If False, those options
            are shown as '< hidden >'
        :type display_sensitive: bool
        """
        cfg = copy.deepcopy(self._sections)

        # remove __name__ (affects Python 2 only)
        for options in cfg.values():
            options.pop('__name__', None)

        # add source
        if display_source:
            for section in cfg:
                for k, v in cfg[section].items():
                    cfg[section][k] = (v, 'airflow config')

        # add env vars and overwrite because they have priority
        for ev in [ev for ev in os.environ if ev.startswith('AIRFLOW__')]:
            try:
                _, section, key = ev.split('__')
                opt = self._get_env_var_option(section, key)
            except ValueError:
                opt = None
            if opt:
                if (
                        not display_sensitive
                        and ev != 'AIRFLOW__CORE__UNIT_TEST_MODE'):
                    opt = '< hidden >'
                if display_source:
                    opt = (opt, 'env var')
                cfg.setdefault(section.lower(), OrderedDict()).update(
                    {key.lower(): opt})

        # add bash commands
        for (section, key) in AirflowConfigParser.as_command_stdout:
            opt = self._get_cmd_option(section, key)
            if opt:
                if not display_sensitive:
                    opt = '< hidden >'
                if display_source:
                    opt = (opt, 'bash cmd')
                cfg.setdefault(section, OrderedDict()).update({key: opt})

        return cfg

    def load_test_config(self):
        """
        Load the unit test configuration.

        Note: this is not reversible.
        """
        # override any custom settings with defaults
        self.read_string(parameterized_config(DEFAULT_CONFIG))
        # then read test config
        self.read_string(parameterized_config(TEST_CONFIG))
        # then read any "custom" test settings
        self.read(TEST_CONFIG_FILE)

###########################################################################
airflow_conf = None

def get_airflow_config():
    if airflow_conf is None:
        airflow_conf = AirflowConfigParser()
    return airflow_conf
