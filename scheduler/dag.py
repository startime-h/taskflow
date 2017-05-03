#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import logging
import threading
import sys_path

import status
from common import logging_config
from common import config_parser
from db import table_struct
from db.interface import dag_info
from db.interface import task_info
from db.interface import task_pending_queue

logger = logging_config.schedulerLogger()
logger.setLevel(logging.INFO)

class Dag(threading.Thread):
    def __init__(self, dag_row, retry_times=3, interval=5):
        super(Dag, self).__init__()
        self.dag_row = dag_row
        self.retry_times = retry_times
        self.interval = interval
        # dag
        self.dag_id = dag_row[table_struct.DagInfo.ID]
        self.dag_name = dag_row[table_struct.DagInfo.DagName]
        self.dag_json = dag_row[table_struct.DagInfo.DagJson]
        # init
        self.stop = False
        self.terminated = False
        self.running_tasks = list()
        self._init_dag_json_()

    def _init_dag_json_(self):
        self.dag_json = json.loads(str(self.dag_json))
        self._calc_in_out_degree_()

    def _calc_in_out_degree_(self):
        self.task_map = dict()
        for task_id, next_task_list in self.dag_json.items():
            if task_id not in self.task_map:
                self.task_map[task_id] = dict()
                self.task_map[task_id]['in'] = 0
                self.task_map[task_id]['out'] = 0
            # set in
            for next_task in next_task_list:
                next_task = str(next_task)
                if next_task not in self.task_map:
                    self.task_map[next_task] = dict()
                    self.task_map[next_task]['in'] = 0
                    self.task_map[next_task]['out'] = 0
                self.task_map[next_task]['in'] += 1
            # set out
            self.task_map[task_id]['out'] += len(next_task_list)

    def _reset_dag_all_tasks_(self):
        retry_times = self.retry_times
        while retry_times:
            succ = task_info.update_dag_all_tasks_status(self.dag_id, status.TASK_NOT_RUNNING)
            if succ: break
            retry_times -= 1

    def _get_in_tasks_(self):
        # get in tasks
        in_tasks = list()
        for task_id, in_out_degree_map in self.task_map.items():
            if in_out_degree_map['in'] == 0:
                in_tasks.append(int(task_id))
        # modify dag json
        for in_task in in_tasks:
            self.dag_json.pop(str(in_task))
        for in_task in in_tasks:
            for task_id, next_task_list in self.dag_json.items():
                if in_task in next_task_list:
                    next_task_list.remove(in_task)
        # calculate in and out degree
        self._calc_in_out_degree_()
        return in_tasks

    def _add_pending_tasks_(self):
        for task_id in self.running_tasks:
            machine_ip = task_info.get_task_run_machine(task_id)
            if machine_ip is None:
                logger.error('Select task:[%d] run machine fail.' % task_id)
                self.stop = True
            # add to task_pending_queue
            succ = task_pending_queue.add_pending_task(task_id, machine_ip)
            if not succ:
                logger.error('Add pending task:[%d] fail.' % task_id)
                self.stop = True

    def _check_once_(self):
        if len(self.dag_json.keys()) == 0 and len(self.running_tasks) == 0:
            self.stop = True
            self.terminated = True
            return
        # check running tasks
        terminated_tasks = list()
        for task_id in self.running_tasks:
            row = task_info.select_task_by_id(task_id)
            if row[table_struct.TaskInfo.TaskStatus] == status.TASK_FAILED:
                self.stop = True
                return
            elif row[table_struct.TaskInfo.TaskStatus] == status.TASK_TERMINATED:
                terminated_tasks.append(task_id)
        # delete terminated task
        for task_id in terminated_tasks:
            self.running_tasks.remove(task_id)

    def _update_dag_status_(self):
        new_status = status.DAG_TERMINATED
        if not self.terminated:
            new_status = status.DAG_FAILED
        retry_times = self.retry_times
        while retry_times:
            succ = dag_info.update_dag_status(self.dag_id, new_status)
            if succ: break
            retry_times -= 1

    def run(self):
        logger.info('Start run dag:[%s]' % self.dag_name)
        # reset dag all task status: NotRunning
        self._reset_dag_all_tasks_()
        while not self.stop:
            if len(self.running_tasks) == 0:
                self.running_tasks = self._get_in_tasks_()
                self._add_pending_tasks_()
            time.sleep(self.interval)
            self._check_once_()
        # set dag status to Terminated
        self._update_dag_status_()
        logger.info('Success run dag:[%s]' % self.dag_name)
