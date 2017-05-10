#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import ConfigParser

import sys_path
import logging_config
logger = logging_config.commonLogger()
logger.setLevel(logging.INFO)

class Config():
    '''
    parser config file
    config_dict = {
        section_1: {},
        section_2: {},
        section_3: {},
    }
    '''

    def __init__(self, config_file):
        try:
            config_reader = ConfigParser.ConfigParser()
            config_reader.read(config_file)
            config_dict = dict()
            for section in config_reader.sections():
                config_dict[section] = dict()
                for option in config_reader.options(section):
                    value = config_reader.get(section, option)
                    config_dict[section][option] = value
            self.config_dict = config_dict
        except Exception,e:
            logger.error('parse config file:[%s] exception:[%s]' % (config_file, str(e)))
            self.config_dict = dict()
            pass

    def has_section(self, section):
        return section in self.config_dict

    def has_section_key(self, section, key):
        return section in self.config_dict and key in self.config_dict[section]

    def add_section(self, section):
        if has_section(section):
            return
        self.config_dict[section] = dict()

    def add_section_key(self, section, key, value):
        if not has_section(section):
            self.config_dict[section] = dict()
        self.config_dict[section][key] = value

    def delete_section(self, section):
        if not has_section(section):
            return
        del self.config_dict[section]

    def delete_section_key(self, section, key):
        if not self.has_section_key(section, key):
            return
        del self.config_dict[section][key]

    def set_section_key(self, section, key, value):
        if self.has_section_key(section, key):
            self.config_dict[section][key] = value
        else:
            self.add_section_key(section, key, value)

    def get_section_key(self, section, key):
        if self.has_section_key(section, key):
            return self.config_dict[section][key]
        return None
