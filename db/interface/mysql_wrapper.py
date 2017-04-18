#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import warnings
import MySQLdb

import sys_path

FORMAT = '[%(levelname)s] [%(asctime)s] [%(filename)s::%(funcName)s::%(lineno)d] [%(message)s]'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('mysql_wrapper')

class MysqlWrapper(object):
    def __init__(self, mysql_config=MysqlConfig()):
        self.mysql_config = mysql_config
        self.connect = self._db_connect_()

    def _db_connect_():
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
        host = self.mysql_config.hostname
        port = self.mysql_config.port
        user = self.mysql_config.user
        password = self.mysql_config.password
        db = self.mysql_config.db
        charset = self.mysql_config.charset
        return MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)

    def _execute_sql_(sql):
        """
        Exceute sql

        @sql: sql

        """
        try:
            self.cursor = self.connect.cursor()
            self.cursor.execute(sql)
        except Exception, e:
            logger.error('exceute sql:[%s] exception:[%s]' % (sql, str(e)))

    def transaction(sql):
        """
        Transaction sql

        @sql: sql

        """
        try:
            _execute_sql_(sql)
            db.commit()
        except:
            logger.error('transaction sql:[%s] exception:[%s]' % (sql, str(e)))
            db.rollback()

    def add_table(sql):
        """
        Add mysql table

        @sql: sql

        return True/False
        """
        try:
            _execute_sql_(sql)
            return True
        except Exception, e:
            logger.error('add table sql:[%s] exception:[%s]' % (sql, str(e)))
            return False

    def delete_table(sql):
        """
        Delete mysql table

        @db: db connect obj
        @sql: sql

        return True/False
        """
        try:
            _execute_sql_(sql)
            return True
        except Exception, e:
            logger.error('delete table sql:[%s] exception:[%s]' % (sql, str(e)))
            return False

    def select(db, sql):
        """
        Select mysql table

        @db: db connect obj
        @sql: sql

        return results list, return None when exception
        """
        try:
            _execute_sql_(sql)
            results = self.cursor.fetchall()
            return results
        except Exception, e:
            logger.error('table select sql:[%s] exception:[%s]' % (sql, str(e)))
            return None

    def insert(db, sql):
        """
        Insert mysql table

        @sql: sql

        return True/False
        """
        try:
            transaction(sql)
            return True
        except Exception, e:
            logger.error('table insert sql:[%s] exception:[%s]' % (sql, str(e)))
            return False

    def update(sql):
        """
        Update mysql table

        @sql: sql

        return True/False
        """
        try:
            transaction(sql)
            return True
        except Exception, e:
            logger.error('table update sql:[%s] exception:[%s]' % (sql, str(e)))
            return False

    def delete(db, sql):
        """
        Delete mysql table

        @sql: sql

        return True/False
        """
        try:
            transaction(sql)
            return True
        except Exception, e:
            logger.error('table delete sql:[%s] exception:[%s]' % (sql, str(e)))
            return False

