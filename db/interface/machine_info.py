#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import sys_path

from common import logging_config
from common import config_parser
import table_struct
import mysql_wrapper

logger = logging_config.commonLogger()
logger.setLevel(logging.INFO)

def select_machine_info(machine_name, machine_ip):
    '''
    Select machine info record

    @machin_name: machine name
    @machin_ip: machine ip address

    return rows: success
           []: fail
    '''
    table = table_struct.T_MACHINE_INFO
    cond_map = {
        table_struct.MachineInfo.MachineName: machine_name,
        table_struct.MachineInfo.MachineIP: machine_ip
    }
    # do select
    mysql = mysql_wrapper.MysqlWrapper()
    rows = mysql.select(table, cond_map)
    if len(rows) == 0:
        logger.error('Select machine info get empty rows')
        return list()
    return rows[0]

def add_machine_info(machine_name, machine_ip):
    '''
    Add machine info record

    @machin_name: machine name
    @machin_ip: machine ip address

    return True: sucess
           False: fail
    '''
    # check has in mysql
    row = select_machine_info(machine_name, machine_ip)
    if len(row) != 0:
        return True
    # do insert
    table = table_struct.T_MACHINE_INFO
    cond_map = {
        table_struct.MachineInfo.MachineName: machine_name,
        table_struct.MachineInfo.MachineIP: machine_ip
    }
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.insert(table, cond_map)
    if succ is False:
        logger.error('Insert machine info fail.')
        return False
    return True

def update_machine_info(new_cond_map, old_cond_map):
    '''
    udpate machine info record

    @new_cond_map = {
        'machine_name': ...
        'machine_ip': ...
    }
    @old_cond_map = {
        'machine_name': ...
        'machine_ip': ...
    }

    return True: sucess
           False: fail
    '''
    # do update record
    table = table_struct.T_MACHINE_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.update(table, new_cond_map, old_cond_map)
    if succ is False:
        logger.error('Update machine info fail.')
        return False
    return True

def delete_machine_info(cond_map):
    '''
    delete machine info record

    @cond_map = {
        user_id: xxx
        ...
    }

    return True: sucess
           False: fail
    '''
    # do delete record
    table = table_struct.T_MACHINE_INFO
    mysql = mysql_wrapper.MysqlWrapper()
    succ = mysql.delete(table, cond_map)
    if succ is False:
        logger.error('Delete machine info fail.')
        return False
    return True

if __name__ == '__main__':
    pass
