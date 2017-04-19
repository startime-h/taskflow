#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import MySQLdb

from common import logging_config
from common import config_parser
import sys_path

logger = logging_config.commonLogger()
logger.setLevel(logging.INFO)

DB_CONF_PATH = sys_path.__grandfather_dir__+ '/conf/db.cfg'

class MysqlWrapper(object):
    def __init__(self):
        self.db_config = config_parser.Config(DB_CONF_PATH)
        if not _valid_config_(self.db_config):
            logger.error('Invalid db config')
            sys.exit(2)
        self.connect = self._db_connect_(self.db_config)
        self.cursor = self.connect.cursor()

    def _valid_config_(self, db_config):
        if not db_config.has_section_key('mysql', 'hostname') or \
            not db_config.has_section_key('mysql', 'port') or \
            not db_config.has_section_key('mysql', 'user') or \
            not db_config.has_section_key('mysql', 'password') or \
            not db_config.has_section_key('mysql', 'db'):
            return False
        return True

    def _db_connect_(self, db_config):
        """
        Create db connect obj

        @host: mysql host
        @port: mysql host port
        @user: connect mysql user
        @passwd: connect mysql password
        @db: mysql db
        @charset: connect charset, default equal utf-8

        return connect obj
        """
        logger.info('start connect to mysql db ...')

        host = db_config.get_section_key('mysql', 'hostname')
        port = db_config.get_section_key('mysql', 'port')
        user = db_config.get_section_key('mysql', 'user')
        password = db_config.get_section_key('mysql', 'password')
        db = db_config.get_section_key('mysql', 'db')
        charset = 'utf-8'
        if db_config.get_section_key('mysql', 'charset'):
            charset = db_config.get_section_key('mysql', 'charset')

        logger.info('success connect to mysql db. host:[%s] port:[%s] user:[%s] password:[%s] db:[%s]') \
                % (host, port, user, password, db)
        return MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)

    def _execute_sql_(self, sql):
        """
        Exceute sql
        @sql: sql

        """
        try:
            self.cursor.execute(sql)
        except Exception, e:
            logger.error('exceute sql:[%s] exception:[%s]' % (sql, str(e)))

    def gen_select_sql(self, table, cond_map, fields):
        try:
            sql = 'select %s from %s' % (fields, table)
            condition = ''
            for key, value in cond_map.items():
                condition += '`%s`=\'%s\' and ' % (key, str(value))
            if condition.endswith(' and '):
                condition = condition[:-5]
            if condition == '':
                condition = 'where 1 = 1'
            sql = sql + ' %s;' % condition
            return sql
        except Exception, e:
            logger.error('generate select sql exception:[%s]' % str(e))
            return None

    def gen_insert_sql(self, table, cond_map):
        try:
            sql = 'insert into %s' % (fields, table)
            colums = ''
            values = ''
            for key, value in cond_map.items():
                colums += '`%s`,' % key
                valus += '\'%s\',' % value
            colums = '(' + colums.strip(',') + ')'
            values = '(' + values.strip(',') + ')'
            sql = sql + ' %s VALUES %s;' % (colums, values)
            return sql
        except Exception, e:
            logger.error('generate insert sql exception:[%s]' % str(e))
            return None

    def select(self, table, cond_map, fields = '*'):
        '''
        select table fields

        @table: mysql table name
        @cond_map = {
            'key': value,
            ...
        }
        @fields: select fields, such as 'user_id, user_name'
                 default '*', select all fields

        return success:results
               fail: None
        '''
        logger.info('start to select mysql table ...')
        try:
            sql = self.gen_select_sql(table, cond_map, fields)
            if sql is None:
                return None
            self._execute_sql_(sql)
            results = self.cursor.fetchall()
            return results
        except Exception, e:
            logger.error('[select] sql:[%s] exception:[%s]' % (sql, str(e)))
        logger.info('success to select mysql table')

    def insert(self, table, cond_map):
        '''
        insert row to table

        @table: mysql table name
        @cond_map = {
            'key': value,
            ...
        }

        return success:True
               fail: False
        '''
        logger.info('start to insert mysql table ...')
        try:
            sql = self.gen_insert_sql(table, cond_map, fields)
            if sql is None:
                return None
            self._execute_sql_(sql)
            self.connect.commit()
            return True
        except Exception, e:
            logger.error('[insert] sql:[%s] exception:[%s]' % (sql, str(e)))
            self.connect.rollback()
            return False
        logger.info('success to insert mysql table')
