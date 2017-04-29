#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import MySQLdb
import MySQLdb.cursors

from common import logging_config
from common import config_parser
import sys_path

logger = logging_config.dbLogger()
logger.setLevel(logging.INFO)

DB_CONF_PATH = sys_path.__grandfather_dir__+ '/conf/db.cfg'

class MysqlWrapper(object):
    def __init__(self):
        self.db_config = config_parser.Config(DB_CONF_PATH)
        if not self._valid_config_(self.db_config):
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

        host = db_config.get_section_key('mysql', 'hostname')
        port = db_config.get_section_key('mysql', 'port')
        user = db_config.get_section_key('mysql', 'user')
        password = db_config.get_section_key('mysql', 'password')
        db = db_config.get_section_key('mysql', 'db')
        charset = 'utf8'
        if db_config.get_section_key('mysql', 'charset'):
            charset = db_config.get_section_key('mysql', 'charset')

        return MySQLdb.connect(host=host, port=int(port), user=user, passwd=password, db=db, \
                charset=charset, cursorclass = MySQLdb.cursors.DictCursor)

    def _execute_sql_(self, sql):
        """
        Exceute sql
        @sql: sql
        """
        self.cursor.execute(sql)

    def _rollback(self):
        """
        rollbock sql
        """
        self.connect.rollback()

    def gen_select_sql(self, table, cond_map, fields):
        try:
            sql = 'select %s from %s' % (fields, table)
            condition = ''
            for key, value in cond_map.items():
                condition += '`%s`=\'%s\' and ' % (key, str(value))
            if condition.endswith(' and '):
                condition = condition[:-5]
            if condition == '':
                condition = '1 = 1'
            sql = sql + ' where %s;' % condition
            return sql
        except Exception, e:
            logger.error('generate select sql exception:[%s]' % str(e))
            return None

    def gen_insert_sql(self, table, cond_map):
        try:
            sql = 'insert into %s' % table
            colums = ''
            values = ''
            for key, value in cond_map.items():
                colums += '`%s`,' % key
                values += '\'%s\',' % value
            colums = '(' + colums.strip(',') + ')'
            values = '(' + values.strip(',') + ')'
            sql = sql + ' %s VALUES %s;' % (colums, values)
            return sql
        except Exception, e:
            logger.error('generate insert sql exception:[%s]' % str(e))
            return None

    def gen_update_sql(self, table, new_cond_map, old_cond_map):
        try:
            sql = 'update %s ' % table
            # set new value
            new_values = ''
            for key, value in new_cond_map.items():
                new_values += '`%s` = \'%s\',' % (key, value)
            sql += 'set ' + new_values.strip(',')
            # set condition
            condition = ''
            for key, value in old_cond_map.items():
                condition += '`%s` = \'%s\' and' % (key, value)
            if condition.endswith(' and'):
                condition = condition[:-4]
            if condition != '':
                sql += ' where %s;' % condition
            return sql
        except Exception, e:
            logger.error('generate update sql exception:[%s]' % str(e))
            return None

    def gen_delete_sql(self, table, cond_map):
        try:
            sql = 'delete from %s ' % table
            condition = ''
            for key, value in cond_map.items():
                condition += '`%s` = \'%s\' and' % (key, value)
            if condition.endswith(' and'):
                condition = condition[:-4]
            if condition != '':
                sql += ' where %s;' % condition
            return sql
        except Exception, e:
            logger.error('generate delete sql exception:[%s]' % str(e))
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
        try:
            if len(cond_map) == 0:
                logger.error('[select] condition map is empty')
                return list()
            sql = self.gen_select_sql(table, cond_map, fields)
            if sql is None:
                return list()
            self._execute_sql_(sql)
            results = list()
            for res in self.cursor.fetchall():
                results.append(res)
            return results
        except Exception, e:
            logger.error('[select] sql exception:[%s]' % (str(e)))
            return list()

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
        try:
            if len(cond_map) == 0:
                logger.error('[insert] condition map is empty')
                return False
            sql = self.gen_insert_sql(table, cond_map)
            if sql is None:
                return False
            self._execute_sql_(sql)
            self.connect.commit()
            return True
        except Exception, e:
            logger.error('[insert] sql exception:[%s]' % (str(e)))
            self._rollback()
            return False

    def update(self, table, new_cond_map, old_cond_map):
        '''
        update table row

        @table: mysql table name
        @new_cond_map = {
            'key': value,
            ...
        }
        @old_cond_map = {
            'key': value,
            ...
        }

        return success:True
               fail: False
        '''
        try:
            if len(new_cond_map) == 0:
                logger.error('[update] new condition map is empty')
                return False
            sql = self.gen_update_sql(table, new_cond_map, old_cond_map)
            self._execute_sql_(sql)
            self.connect.commit()
            return True
        except Exception, e:
            logger.error('[update] sql exception:[%s]' % (str(e)))
            self._rollback()
            return False

    def delete(self, table, cond_map):
        '''
        delete table row

        @table: mysql table name
        @cond_map = {
            'key': value,
            ...
        }

        return success:True
               fail: False
        '''
        try:
            if len(cond_map) == 0:
                logger.error('[delete] condition map is empty')
                return False
            sql = self.gen_delete_sql(table, cond_map)
            self._execute_sql_(sql)
            self.connect.commit()
            return True
        except Exception, e:
            logger.error('[delete] sql exception:[%s]' % (str(e)))
            self.connect.rollback()
            return False
